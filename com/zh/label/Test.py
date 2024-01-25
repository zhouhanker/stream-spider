import requests

url = "http://192.168.213.138:8191/v1"
headers = {"Content-Type": "application/json"}
data = {
	"cmd": "request.get",
	"url": "https://www.baidu.com",
	"maxTimeout": 1000
}
response = requests.post(url, headers=headers, json=data)
print(response)
print(response.text)




