import os.path
import time
import timeit

import requests
import re
import csv
import pandas as pd
from colorama import Fore
from lxml import html
from pyspark.python.pyspark.shell import sc

from com.zh.label.config import config
from com.zh.utils.FileUtils import get_user_agent
from datetime import datetime
from pyspark.sql import session, SparkSession
from com.zh.utils.SeleniumUtils import seleniumUtils

user_agent_path = '../../resource/agents.txt'
# explicitly changed encoding to utf-8
os.system('chcp 65001')


# 获取ethscanCloud中的所有标签 只获取account标签和token标签
def get_ethscan_all_label():
	ethscan_cloud_url = f'{config.ethscan_label_base_url}{"/labelcloud"}'
	headers = {
		'User-Agent': get_user_agent(user_agent_path),
		'Accept': config.base_accept,
		'cookie': "etherscan_offset_datetime=+8; __stripe_mid=2284c985-abe9-47bc-a3dc-f6dd186fc50be372c7; etherscan_pwd=4792:Qdxb:ZQoxE7hwxuZ8IpB6V/Xg8t0SlBUyo6OYxvYH8fDRMes=; etherscan_userid=zhouhan; etherscan_autologin=True; __cflb=0H28vPcoRrcznZcNZSuFrvaNdHwh858XnsnowBrTHkg; _gid=GA1.2.310546296.1705468157; cf_clearance=PdguUBeWn1Sn1tw15OKm7ZbL0QJJZAHIgtyL7p2zxqU-1705470525-1-ATSdy4t/5ezAXkitP/R93VBYUbO3CxCKXqokYv6+LcDUBZPaWg0GBMwmJyrV76nq7ffaIObbRSRVeUNeL3hm8Wk=; cf_chl_rc_ni=7; cf_chl_3=be16dc3cc6971e3; ASP.NET_SessionId=u5w4xt52ozihhnocoohpqlwk; _ga_T1JC9RNQXV=GS1.1.1705482596.4.1.1705484391.59.0.0; _ga=GA1.2.1989122975.1705296681; _gat_gtag_UA_46998878_6=1"
	}
	eth_root_label_result_list = []
	label_resp = requests.get(ethscan_cloud_url, headers=headers).text
	eth_root = html.fromstring(label_resp)
	select_div = eth_root.xpath("//div[@class='col-md-4 col-lg-3 mb-3 secondary-container']")
	for div in select_div:
		origin_name = div.xpath(".//span")[0].text_content().strip()
		cnt = origin_name.split(' ')[-1]
		label_name = re.sub(r'\s*\d+$', '', origin_name)
		# 获取li里面a标签的href值
		href_values = div.xpath(".//li/a/@href")
		data = {
			'label_name': label_name,
			'url': href_values,
			'cnt': cnt,
			'is_read': 0
		}
		eth_root_label_result_list.append(data)

	for label in eth_root_label_result_list:
		for url in label['url']:
			if url.startswith('/accounts'):
				label['account_url'] = f'{config.ethscan_label_base_url}{url}'
			if url.startswith('/tokens'):
				label['token_url'] = f'{config.ethscan_label_base_url}{url}'
		del label['url']

	return eth_root_label_result_list


def get_time():
	return datetime.now().strftime('%Y-%m-%d')


def write_label_to_csv(label_list, label_path):
	if not os.path.exists(label_path):
		with open(label_path, mode='w', newline='') as f:
			column_name = label_list[0].keys()
			writer = csv.DictWriter(f, fieldnames=column_name)
			writer.writeheader()
			[writer.writerow(row) for row in label_list]
		print(f'label list write to csv -> {label_path}')
	else:
		print(f'{label_path}{"is exists !"}')


def change_df_style(wait_df):
	pd.set_option('display.max_columns', None)
	df_to_string = wait_df.to_string(index=False, line_width=2000)
	return df_to_string


def get_address_label_detail(current_file_path):
	current_df = pd.read_csv(current_file_path)
	select_column = ['label_name', 'account_url', 'token_url']
	account_df = current_df[select_column].dropna(subset=['account_url'])
	web_driver = seleniumUtils.get_selenium_chrome_driver()
	web_driver.get("https://etherscan.io/labelcloud")
	time.sleep(5)
	web_driver.get('https://etherscan.io/accounts/label/0x-protocol-ecosystem')
	input(Fore.LIGHTRED_EX+"Have you entered the first page? Please enter any character: \n"+Fore.RESET)
	for i in account_df.index:
		label_name = account_df.loc[i, 'label_name']
		account_url = account_df.loc[i, 'account_url']
		print(account_url)
		web_driver.get(account_url)
		time.sleep(4)
		source_doc = html.fromstring(web_driver.page_source)
		tr_elements = source_doc.xpath("//tbody/tr")
		for tr in tr_elements:
			address = tr.xpath(".//td[1]/span/span/a/@href")[0].split('/')[2]
			name_tag = tr.xpath(".//td[2]/text()")[0]
			data = {
				'label_name': label_name,
				'address_type': "address",
				'address': address,
				'name_tag': name_tag,
				'chain_code': 'ETH'
			}

			print(data)


def get_label_diff_list(current_file_path, old_file_path):
	spark = SparkSession.builder.config("spark.driver.extraJavaOptions", "-Dfile.encoding=UTF-8").appName("readCsv").getOrCreate()
	sc.setLogLevel("WARN")

	spark.read.csv(current_file_path, header=True, inferSchema=True).createOrReplaceTempView("current_label")
	spark.read.csv(old_file_path, header=True, inferSchema=True).createOrReplaceTempView("old_label")
	result_label = spark.sql("""
			select t1.label_name,
				   t1.current_cnt,
				   t1.old_cnt,
				   (t1.current_cnt - t1.old_cnt) as cnt_diff,
				   t1.account_url,
				   t1.token_url
			from (
				select current_label.label_name,
					   current_label.cnt as current_cnt,
					   old_label.cnt as old_cnt,
					   current_label.is_read,
					   current_label.account_url,
					   current_label.token_url	
			from current_label
			left join old_label on current_label.label_name = old_label.label_name
			where current_label.cnt > old_label.cnt
			) as t1
			where t1.account_url is not null and t1.token_url is not null 
		""")
	result_label.coalesce(1).toPandas().to_csv(f'./csvFile/{get_time()}-diff-label.csv', mode='w', header=result_label.columns, index=False)
	spark.stop()
	print(Fore.RED + 'Get_label_diff_list() method execute complete', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + Fore.RESET)


if __name__ == '__main__':
	write_to_label_csv_path = f'./csvFile/{get_time()}{"-label"}'
	ethscan_all_label = get_ethscan_all_label()
	print(f'GET Ethscan.io take time: {timeit.timeit(get_ethscan_all_label, number=1)} s')
	write_label_to_csv(ethscan_all_label, write_to_label_csv_path)
	get_label_diff_list(write_to_label_csv_path, 'csvFile/init_label.csv')
	
	# current_csv_pd = pd.read_csv('./csvFile/2024-02-05-label')
	# init_csv_pd = pd.read_csv('./csvFile/init_label.csv')
	
	
	

	# get_address_label_detail('./csvFile/2024-01-29-label')
	# read_csv_df = pd.read_csv(write_to_label_csv_path)
	# select_column = ['label_name', 'cnt', 'is_read', 'account_url']
	# account_df = read_csv_df[select_column].dropna(subset=['account_url'])
	# for i in account_df.index:
	# 	labelName = account_df.loc[i, 'label_name']
	# 	cnt = account_df.loc[i, 'cnt']
	# 	is_read = account_df.loc[i, 'is_read']
	# 	account_url = account_df.loc[i, 'account_url']
	# 	print(i, labelName, cnt, is_read, account_url)
	# 	time.sleep(0.5 + random.random())
	# 	web_driver.get(account_url)
	# 	time.sleep(3)
