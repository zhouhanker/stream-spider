import getpass


class config:
    # 本地计算机名称,需要调用本地的浏览器进行访问
    local_user_name: str = f'{getpass.getuser()}'
    # 初始url
    ethscan_label_base_url: str = 'https://etherscan.io'
    bscscan_label_base_url: str = 'https://bscscan.com'
    btc_label_url: str = 'https://www.walletexplorer.com'
    # Accept 头信息
    base_accept: str = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    base_accept_encoding: str = 'gzip, deflate, br'
    base_user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    base_cache_control: str = 'max-age=0'
    base_accept_language: str = 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    base_sec_ch_ua: str = 'Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120'
    base_sec_ch_Ua_mobile: str = "?0"
    base_sec_ch_ua_platform: str = 'Windows'
    base_Sec_Ch_Ua_Arc: str = 'x86'
    base_sec_fetch_dest: str = 'document'
    base_sec_fetch_mode: str = 'navigate'
    base_sec_fetch_user: str = '?1'
    base_upgrade_insecure_requests: str = '1'
    base_sec_fetch_site: str = 'none'
    # 本地浏览器路径
    chrome_user_data_dir: str = rf"user-data-dir=C:\Users\{local_user_name}\AppData\Local\Google\Chrome\User Data"
    edge_user_data_dir: str = rf"user-data-dir=C:\Users\{local_user_name}\AppData\Local\Microsoft\Edge\User Data"
    # 间隔时间
    over_time: int = 5
    
    remote_user_name: str = 'root'
    remote_user_password: str = 'root'
    
    dingtalk_robot_access_token: str = ''
