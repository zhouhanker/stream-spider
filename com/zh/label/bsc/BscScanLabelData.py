import math
import os.path
import random
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
from tqdm.autonotebook import tqdm

user_agent_path = '../../resource/agents.txt'
# explicitly changed encoding to utf-8
os.system('chcp 65001')


# 获取bscScanCloud中的所有标签 只获取account标签和token标签
def get_bsc_scan_all_label():
	bscscan_cloud_url = f'{config.bscscan_label_base_url}{"/labelcloud"}'
	headers = {
		'User-Agent': get_user_agent(user_agent_path),
		'Accept': config.base_accept
	}
	bsc_root_label_result_list = []
	label_resp = requests.get(bscscan_cloud_url, headers=headers).text
	bsc_root = html.fromstring(label_resp)
	select_div = bsc_root.xpath("//div[@class='col-md-4 col-lg-3 mb-3 secondary-container']")
	for div in select_div:
		origin_name = div.xpath(".//span")[0].text_content().strip()
		cnt = origin_name.split(' ')[-1]
		label_name = re.sub(r'\s*\d+$', '', origin_name)
		# 获取li里面a标签的href值
		href_values = div.xpath(".//li/a/@href")
		detail_cnt = div.xpath(".//ul/li/a/text()")
		data = {
			'label_name': label_name,
			'url': href_values,
			'cnt': cnt,
			'detail_cnt': detail_cnt,
			'is_read': 0
		}
		bsc_root_label_result_list.append(data)
	
	for label in bsc_root_label_result_list:
		for url in label['url']:
			if url.startswith('/accounts'):
				label['account_url'] = f'{config.bscscan_label_base_url}{url}'
			if url.startswith('/tokens'):
				label['token_url'] = f'{config.bscscan_label_base_url}{url}'
		del label['url']
	
	for label in bsc_root_label_result_list:
		for j in label['detail_cnt']:
			if j.startswith('Accounts'):
				label['account_cnt'] = j.split(' ')[-1].strip('()')
			if j.startswith('Tokens'):
				label['token_cnt'] = j.split(' ')[-1].strip('()')
		del label['detail_cnt']
	return bsc_root_label_result_list


def get_time():
	return datetime.now().strftime('%Y-%m-%d')


def write_label_to_csv(label_list, label_path):
	if not os.path.exists(label_path):
		with open(label_path, mode='w', newline='') as f:
			column_name = ['label_name', 'cnt', 'is_read', 'account_url', 'token_url', 'account_cnt', 'token_cnt']
			writer = csv.DictWriter(f, fieldnames=column_name)
			writer.writeheader()
			tq = tqdm(label_list, desc='write to csv', ncols=100, ascii=True)
			for i in tq:
				writer.writerow(i)
				tq.set_postfix({'label_name': i['label_name']})
		print(Fore.RED+f'label list write to csv -> {label_path}'+Fore.RESET)
	else:
		print(f'{label_path}{"is exists !"}')


def write_dict_2_csv(dict_list, csv_path):
	os_path_exists = os.path.exists(csv_path)
	filed_name = dict_list.keys()
	with open(csv_path, 'a', newline='', encoding='utf-8') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=filed_name)
		if not os_path_exists:
			writer.writeheader()
		writer.writerow(dict_list)


def change_df_style(wait_df):
	pd.set_option('display.max_columns', None)
	df_to_string = wait_df.to_string(index=False, line_width=2000)
	return df_to_string


def get_address_label_detail(current_file_path):
	current_df = pd.read_csv(current_file_path)
	select_column = ['label_name', 'account_url', 'token_url', 'account_cnt', 'token_cnt']
	account_df = current_df[select_column].dropna(subset=['account_url'])
	web_driver = seleniumUtils.get_selenium_chrome_driver()
	web_driver.get("https://bscscan.com/labelcloud")
	time.sleep(5)
	web_driver.get('https://bscscan.com/accounts/label/bzx')
	input(Fore.LIGHTRED_EX + "Have you entered the first page? Please enter any character: \n" + Fore.RESET)
	time.sleep(2)
	# account 类型
	for i in account_df.index:
		label_name = account_df.loc[i, 'label_name']
		account_url = account_df.loc[i, 'account_url']
		account_cnt = account_df.loc[i, 'account_cnt']
		if account_cnt <= 50:
			print("---50acc----> "+account_url)
			time.sleep(0.5 + random.random())
			web_driver.get(account_url + f'?subcatid=undefined&size=50&start={0}&col=1&order=asc')
			time.sleep(3 + random.random())
			source_doc = html.fromstring(web_driver.page_source)
			tr_elements = source_doc.xpath("//tbody/tr")
			for tr in tr_elements:
				address = ''
				name_tag = ''
				if tr.xpath(".//td[1]/span/span/a/@href"):
					address = tr.xpath(".//td[1]/span/span/a/@href")[0].split('/')[2]
				if tr.xpath(".//td[2]"):
					name_tag = tr.xpath(".//td[2]")[0].text_content()
				data = {
					'label_name': label_name,
					'address': address,
					'address_type': "address",
					'name_tag': name_tag,
					'chain_code': 'BSC'
				}
				print(data)
				write_dict_2_csv(data, f"./csvFile/{get_time()}-detail.csv")
		if account_cnt > 50:
			page_cnt = math.ceil(account_cnt / 100)
			limit = 100
			for page in range(1, page_cnt + 1):
				time.sleep(0.4 + random.random())
				print("---大于acc50----> " + account_url)
				parse_url = account_url + f'?subcatid=undefined&size=100&start={limit}&col=1&order=asc'
				web_driver.get(parse_url)
				print(parse_url)
				time.sleep(3 + random.random())
				source_doc = html.fromstring(web_driver.page_source)
				tr_elements = source_doc.xpath("//tbody/tr")
				if tr_elements is not None:
					for tr in tr_elements:
						address = ''
						name_tag = ''
						if tr.xpath(".//td[1]/span/span/a/@href"):
							address = tr.xpath(".//td[1]/span/span/a/@href")[0].split('/')[2]
						if tr.xpath(".//td[2]"):
							name_tag = tr.xpath(".//td[2]")[0].text_content()
						data = {
							'label_name': label_name,
							'address': address,
							'address_type': "address",
							'name_tag': name_tag,
							'chain_code': 'BSC'
						}
						print(data)
						write_dict_2_csv(data, f"./csvFile/{get_time()}-detail.csv")
					limit += 100
					
	# token 类型
	token_df = current_df[select_column].dropna(subset=['token_url'])
	for i in token_df.index:
		label_name = token_df.loc[i, 'label_name']
		token_url = token_df.loc[i, 'token_url']
		token_cnt = token_df.loc[i, 'token_cnt']
		
		if token_cnt <= 50:
			time.sleep(0.5 + random.random())
			parse_url = token_url + f'?subcatid=0&size=50&start={0}&col=3&order=desc'
			web_driver.get(parse_url)
			print(parse_url)
			time.sleep(3 + random.random())
			source_doc = html.fromstring(web_driver.page_source)
			tr_elements = source_doc.xpath("//tbody/tr")
			for tr in tr_elements:
				address = ''
				name_tag = ''
				if tr.xpath(".//td/a/@href"):
					address = tr.xpath(".//td/a/@href")[0].split('/')[2]
				if tr.xpath(".//td/a/div/span/text()"):
					name_tag = tr.xpath(".//td/a/div/span/text()")
				name_tag = ''.join(name_tag)
				data = {
					'label_name': label_name,
					'address': address,
					'address_type': "token",
					'name_tag': name_tag,
					'chain_code': 'BSC'
				}
				write_dict_2_csv(data, f"./csvFile/{get_time()}-detail.csv")
		
		if token_cnt > 50:
			page_cnt = math.ceil(token_cnt / 100)
			limit = 100
			for page in range(1, page_cnt + 1):
				time.sleep(0.4 + random.random())
				parse_url = token_url + f'?subcatid=0&size=100&start={limit}&col=3&order=desc'
				web_driver.get(parse_url)
				print(parse_url)
				limit += 100
				time.sleep(3 + random.random())
				source_doc = html.fromstring(web_driver.page_source)
				tr_elements = source_doc.xpath("//tbody/tr")
				for tr in tr_elements:
					address = ''
					name_tag = ''
					if tr.xpath(".//td/a/@href"):
						address = tr.xpath(".//td/a/@href")[0].split('/')[2]
					if tr.xpath(".//td/a/div/span/text()"):
						name_tag = tr.xpath(".//td/a/div/span/text()")
					name_tag = ''.join(name_tag)
					data = {
						'label_name': label_name,
						'address': address,
						'address_type': "token",
						'name_tag': name_tag,
						'chain_code': 'BSC'
					}
					write_dict_2_csv(data, f"./csvFile/{get_time()}-detail.csv")


def get_label_diff_list(current_file_path, old_file_path):
	spark = SparkSession.builder.config("spark.driver.extraJavaOptions", "-Dfile.encoding=UTF-8").appName(
		"readCsv").getOrCreate()
	sc.setLogLevel("WARN")
	
	spark.read.csv(current_file_path, header=True, inferSchema=True).createOrReplaceTempView("current_label")
	spark.read.csv(old_file_path, header=True, inferSchema=True).createOrReplaceTempView("old_label")
	result_label = spark.sql("""-- noinspection SqlResolveForFile
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
	result_label.coalesce(1).toPandas().to_csv(f'./csvFile/{get_time()}-diff-label.csv', mode='w',
											   header=result_label.columns, index=False)
	spark.stop()
	print(Fore.RED + 'Get_label_diff_list() method execute complete',
		  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + Fore.RESET)
	
	
def main():
	write_to_label_csv_path = f'./csvFile/{get_time()}{"-label.csv"}'
	bscscan_all_label = get_bsc_scan_all_label()
	print(f'GET BscScanCloud.io take time: {timeit.timeit(get_bsc_scan_all_label, number=1)} s')
	write_label_to_csv(bscscan_all_label, write_to_label_csv_path)
	get_address_label_detail(f'./csvFile/{get_time()}-label.csv')
	print('bscScanCloudLabel execute complete !')


if __name__ == '__main__':
	
	main()
