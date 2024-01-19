import os.path
import time
import timeit
import requests
import logging
import re
import csv
import pandas as pd
from lxml import html
from com.zh.label.config import config
from com.zh.utils.FileUtils import get_user_agent
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from com.zh.utils.SeleniumUtils import seleniumUtils

user_agent_path = '../../resource/agents.txt'


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


if __name__ == '__main__':
	write_to_label_csv_path = f'./csvFile/{get_time()}{"-label"}'
	# ethscan_all_label = get_ethscan_all_label()
	# print(f'GET Ethscan.io take time: {timeit.timeit(get_ethscan_all_label, number=1)} s')
	# write_label_to_csv(ethscan_all_label, write_to_label_csv_path)

	web_driver = seleniumUtils.get_selenium_chrome_driver()
	web_driver.get("https://etherscan.io/")
	time.sleep(5)
	web_driver.get('https://etherscan.io/accounts/label/0x-protocol-ecosystem')
	time.sleep(5)
	print(web_driver.page_source)

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


