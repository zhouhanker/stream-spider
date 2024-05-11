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
	params = {
		'url': ethscan_cloud_url,
		'apikey': config.zenrows_key,
		'js_render': 'true',
		'js_instructions': """[{"click":".selector"},{"wait":500},{"fill":[".input","value"]},{"wait_for":".slow_selector"}]""",
	}
	eth_root_label_result_list = []
	label_resp = requests.get('https://api.zenrows.com/v1/', params=params).text
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
	write_to_label_csv_path = f'./csvFile/{get_time()}{"-label.csv"}'
	ethscan_all_label = get_ethscan_all_label()
	# print(f'GET Ethscan.io take time: {timeit.timeit(get_ethscan_all_label, number=1)} s')
	# write_label_to_csv(ethscan_all_label, write_to_label_csv_path)
	# get_label_diff_list(write_to_label_csv_path,"../eth/csvFile/init_label.csv")
	for i in ethscan_all_label:
		print(i)
	# current_csv_pd = pd.read_csv('./csvFile/2024-02-05-label')
	# init_csv_pd = pd.read_csv('./csvFile/init_label.csv')
	
	
