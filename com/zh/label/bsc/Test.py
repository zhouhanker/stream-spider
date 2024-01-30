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

os.system('chcp 65001')
user_agent_path = '../../resource/agents.txt'

bscscan_cloud_url = f'{config.bscscan_label_base_url}{"/labelcloud"}'
headers = {
	'User-Agent': get_user_agent(user_agent_path),
	'Accept': config.base_accept
}
bsc_root_label_result_list = []
label_resp = requests.get(bscscan_cloud_url, headers=headers).text
bsc_root = html.fromstring(label_resp)
div_elements = bsc_root.xpath("//div[@class='row mb-3']/div")

# 遍历每个元素并打印其HTML源代码
# for i in div_elements:
# 	res = {}
# 	label = i.text_content()
# 	match_label_name = re.match(r"(\D+)\d", label)
# 	if match_label_name:
# 		label_name = match_label_name.group(1).strip()
# 		match_accounts = re.search(r'Accounts \((\d+)\)', label)
# 		match_tokens = re.search(r'Tokens \((\d+)\)', label)
# 		res['label_name'] = label_name
# 		if match_accounts:
# 			res['Accounts'] = int(match_accounts.group(1))
# 		if match_tokens:
# 			res['Tokens'] = int(match_tokens.group(1))
# 		print(res)

for div in div_elements:
	url = div.xpath(".//ul/li/a/@href")
	print(div.xpath(".//ul/li/a/text()"))


