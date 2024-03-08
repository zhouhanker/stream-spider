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
	web_driver = seleniumUtils.get_selenium_chrome_driver()
	web_driver.get('https://bot.sannysoft.com/')
	input(Fore.LIGHTRED_EX + "Have you entered the first page? Please enter any character: \n" + Fore.RESET)
	print(web_driver.page_source)
