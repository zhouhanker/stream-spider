from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from com.zh.label.config import *
from com.zh.utils.FileUtils import *


def get_selenium_driver(agent_path):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument(chrome_user_data_dir)
	# 浏览器与进程进行分离
	chrome_options.add_experimental_option('detach', True)
	chrome_options.add_argument(f'user-agent={get_user_agent(agent_path)}')
	chrome_options.add_argument('window-size=1920x3000')
	# 忽略 SSL 证书错误，允许访问使用无效证书的网站
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
	driver.implicitly_wait(over_time)
	driver.maximize_window()
	return driver



