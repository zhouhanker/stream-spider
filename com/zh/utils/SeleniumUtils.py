from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from com.zh.label.config import config
from http.cookies import SimpleCookie


class seleniumUtils:
	@staticmethod
	def get_selenium_chrome_driver():
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument(config.chrome_user_data_dir)
		# 浏览器与进程进行分离
		chrome_options.add_experimental_option('detach', True)
		# 是否启用无头浏览器
		# chrome_options.add_argument('--headless')
		# 关闭自动化测试显示
		chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

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

		# 忽略 SSL 证书错误，允许访问使用无效证书的网站
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_argument('--disable-gpu')
		chrome_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
		chrome_driver.implicitly_wait(config.over_time)
		chrome_driver.maximize_window()

		return chrome_driver

	@staticmethod
	def get_selenium_edge_driver():
		edge_options = webdriver.EdgeOptions()
		edge_options.add_argument(config.edge_user_data_dir)
		edge_options.add_experimental_option('detach', True)
		edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])

		edge_options.add_argument(f'user-agent={config.base_user_agent}')
		edge_options.add_argument('window-size=1920x3000')
		edge_options.add_argument(f'Accept={config.base_accept}')
		edge_options.add_argument(f'Accept-Encoding={config.base_accept_encoding}')
		edge_options.add_argument(f'Cache-Control={config.base_cache_control}')
		edge_options.add_argument(f'Accept-Language={config.base_accept_language}')
		edge_options.add_argument(f'Sec-Ch-Ua={config.base_sec_ch_ua}')
		edge_options.add_argument(f'Sec-Ch-Ua-Mobile={config.base_sec_ch_Ua_mobile}')
		edge_options.add_argument(f'Sec-Ch-Ua-Platform={config.base_sec_ch_ua_platform}')
		edge_options.add_argument(f'Sec-Fetch-Site={config.base_sec_fetch_site}')
		edge_options.add_argument(f'Sec-Fetch-Mode={config.base_sec_fetch_mode}')
		edge_options.add_argument(f'Sec-Fetch-User={config.base_sec_fetch_user}')
		edge_options.add_argument(f'Sec-Fetch-Dest={config.base_sec_fetch_dest}')
		edge_options.add_argument(f'Upgrade-Insecure-Requests={config.base_upgrade_insecure_requests}')

		# 忽略 SSL 证书错误，允许访问使用无效证书的网站
		edge_options.add_argument('--ignore-certificate-errors')
		edge_options.add_argument('--disable-gpu')
		edge_driver = webdriver.Edge(options=edge_options)
		edge_driver.implicitly_wait(config.over_time)
		edge_driver.maximize_window()

		return edge_driver

	@staticmethod
	def get_chrome_cookie_dict(str_cookie):
		cookie = SimpleCookie()
		cookie.load(str_cookie)
		cookie_dict = {key: morsel.value for key, morsel in cookie.items()}
		return cookie_dict



