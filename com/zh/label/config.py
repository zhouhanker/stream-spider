class config:
    # 本地计算机名称,需要调用本地的浏览器进行访问
    local_user_name: str = '朝菌'
    # 初始url
    ethscan_label_base_url: str = 'https://etherscan.io'
    # Accept 头信息
    base_accept: str = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    base_accept_encoding: str = 'gzip, deflate, br'
    base_user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    base_cache_control: str = 'max-age=0'
    base_accept_language: str = 'zh-CN,zh;q=0.9'
    base_sec_ch_ua: str = 'Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120'
    base_sec_ch_Ua_mobile: str = "?0"
    base_sec_ch_ua_platform: str = 'Windows'
    base_sec_fetch_dest: str = 'document'
    base_sec_fetch_mode: str = 'navigate'
    base_sec_fetch_user: str = '?1'
    base_upgrade_insecure_requests: str = '1'
    base_sec_fetch_site: str = 'none'
    cookie_str: str = 'cf_chl_3=a0b59cb37a18034; ASP.NET_SessionId=q4p2pxlkt041pos5sygj0aev; __cflb=0H28vPcoRrcznZcNZSuFrvaNdHwh857Fv6zRowoCAyz; etherscan_offset_datetime=+8; cf_clearance=eV7hacYddkDUdKxnIoTcbZWbzL1wPlriYwjR0LNB_iE-1705547802-1-ATsrtKqtzTqcCONWXx0dqyErC8sa5RTB71YBrJnTCyunbROcJK2Kc1uSu60eGmlwr/SKKkzi3sWKEAoky/ncNLs=; _gid=GA1.2.1638554359.1705547803; _gat_gtag_UA_46998878_6=1; __stripe_mid=e8742611-9a79-43a5-8f1e-bd62eb19e0b3c2e448; __stripe_sid=019e9b90-a8de-4374-8e0e-1bb540be6c21a12807; etherscan_pwd=4792:Qdxb:ZQoxE7hwxuZ8IpB6V/Xg8t0SlBUyo6OYxvYH8fDRMes=; etherscan_userid=zhouhan; etherscan_autologin=True; _ga_T1JC9RNQXV=GS1.1.1705547801.1.1.1705547823.38.0.0; _ga=GA1.2.36811765.1705547802'
    # 本地浏览器路径
    chrome_user_data_dir: str = rf"user-data-dir=C:\Users\{local_user_name}\AppData\Local\Google\Chrome\User Data"
    # 间隔时间
    over_time: int = 5
