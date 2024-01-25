import requests

url = "http://114.24.76.50:8191/v1"
headers = {"Content-Type": "application/json"}
data = {
	"cmd": "request.get",
	"url": "https://etherscan.io/accounts/label/0x-protocol-ecosystem",
	"maxTimeout": 1000
}
response = requests.post(url, headers=headers, json=data)
print(response)
print(response.text)
