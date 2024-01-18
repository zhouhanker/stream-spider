from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from com.zh.label.config import config
from http.cookies import SimpleCookie


def get_selenium_driver():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument(config.chrome_user_data_dir)
	# 浏览器与进程进行分离
	chrome_options.add_experimental_option('detach', True)
	# 是否启用无头浏览器
	# chrome_options.add_argument('--headless')

	chrome_options.add_argument(f'user-agent={config.base_user_agent}')
	chrome_options.add_argument('window-size=1920x3000')
	chrome_options.add_argument(f'Accept={config.base_accept}')
	chrome_options.add_argument(f'Accept-Encoding={config.base_accept_encoding}')
	chrome_options.add_argument(f'Cache-Control={config.base_cache_control}')
	chrome_options.add_argument(f'Accept-Language={config.base_accept_language}')
	chrome_options.add_argument(f'Sec-Ch-Ua={config.base_sec_ch_ua}')
	chrome_options.add_argument(f'Sec-Ch-Ua-Mobile={config.base_sec_ch_Ua_mobile}')
	chrome_options.add_argument(f'Sec-Ch-Ua-Platform={config.base_sec_ch_ua_platform}')
	chrome_options.add_argument(f'Sec-Fetch-Site={config.base_sec_fetch_site}')
	chrome_options.add_argument(f'Sec-Fetch-Mode={config.base_sec_fetch_mode}')
	chrome_options.add_argument(f'Sec-Fetch-User={config.base_sec_fetch_user}')
	chrome_options.add_argument(f'Sec-Fetch-Dest={config.base_sec_fetch_dest}')
	chrome_options.add_argument(f'Upgrade-Insecure-Requests={config.base_upgrade_insecure_requests}')
	chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

	# 忽略 SSL 证书错误，允许访问使用无效证书的网站
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
	driver.implicitly_wait(config.over_time)
	driver.maximize_window()

	# cookie_list = [item.split('=') for item in cookie_str.split('; ')]
	# cookie_dict_list = [{'name': pair[0], 'value': pair[1]} for pair in cookie_list]
	# for cookie in cookie_dict_list:
	# 	driver.add_cookie(cookie)
	return driver


def get_chrome_cookie_dict(str_cookie):
	cookie = SimpleCookie()
	cookie.load(str_cookie)
	cookie_dict = {key: morsel.value for key, morsel in cookie.items()}
	return cookie_dict



