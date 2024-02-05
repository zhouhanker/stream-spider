import time

import requests
import paramiko
import pandas as pd
from colorama import Fore
from curl_cffi import requests
from com.zh.utils.SeleniumUtils import seleniumUtils
from com.zh.label.config import config
import httpx
from com.zh.utils.RemoteHostUtils import RemoteHostUtils


# url = "http://192.168.213.138:8191/v1"
# headers = {"Content-Type": "application/json"}
# data = {
#     "cmd": "request.get",
#     "url": "https://etherscan.io/labelcloud",
#     "maxTimeout": 60000
# }
# response = requests.post(url, headers=headers, json=data)
# print(response.text)


if __name__ == '__main__':
	remote_path = '/root'
	host = '192.168.213.138'
	directory = RemoteHostUtils.inspect_remote_file(host, remote_path)
	for item in directory:
		print(item)
