import time

import requests
from curl_cffi import requests
from DrissionPage import ChromiumPage, ChromiumOptions


def create_task(url, proxy):
	data = {
		"clientKey": "92b07c31fce1eab8236afd9c99092727f55d0b0034215",
		"task": {
			"type": "CloudFlareTaskS1",
			"websiteURL": url,
			"proxy": proxy
		}
	}
	url = "https://api.yescaptcha.com/createTask"
	create_task_response = requests.post(url, json=data).json()
	return create_task_response


def get_task(task_id):
	url = "http://api.yescaptcha.com/getTaskResult"
	data = {
		# 填您自己的密钥
		"clientKey": "92b07c31fce1eab8236afd9c99092727f55d0b0034215",
		"taskId": task_id
	}
	get_task_response = requests.post(url, json=data).json()
	return get_task_response


def get_result(*args, **kwargs):
	uuid = create_task(*args, **kwargs)
	if not uuid or not uuid.get('taskId'):
		return uuid
	print("TaskID:", uuid)
	for i in range(30):
		time.sleep(3)
		result = get_task(uuid.get('taskId'))
		if result.get('status') == 'processing':
			continue
		elif result.get('status') == 'ready':
			return result
		else:
			print("Fail:", result)


if __name__ == '__main__':
	chrome_exe_path = f"C:\Program Files\Google\Chrome\Application\chrome.exe"
	co = ChromiumOptions().set_browser_path(chrome_exe_path)
	page = ChromiumPage(co)
	resp = page.get("https://etherscan.io/labelcloud")
	print(page.html)
	