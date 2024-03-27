import requests
import json

from com.zh.label.config import config


class DingTalkRobot:
    def __init__(self, access_token):
        self.url = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
        self.headers = {'Content-Type': 'application/json'}

    def send_text_message(self, content):
        payload = {
            'msgtype': 'text',
            'text': {
                'content': content
            }
        }
        return requests.post(self.url, headers=self.headers, data=json.dumps(payload)).json()


if __name__ == "__main__":
    token = config.dingtalk_robot_access_token
    dingtalk_robot = DingTalkRobot(token)
    response = dingtalk_robot.send_text_message("!TEST Bots Send Text Message!")
    print(response)
