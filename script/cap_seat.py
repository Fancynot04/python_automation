import requests
import re
import datetime
import time 

" python中缩进统一使用四个空格 "
"""
    1. 预约时间,当天就用nowtime,明天就用lasttime
"""

# 公共参数池
# 请求头
headers = {
	"User-agent": "Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
# 时间相关参数
today = datetime.datetime.now()
nowtime = today.strftime("%Y-%m-%d") # 如2022-08-24
lasttime = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d") # 明天的时间
print("lasttime:{}".format(lasttime))
rommId = "3844" 
seatnum = "001"

def login(uname, password):
	"""
		登录函数
        return: 登录成功后的session
	"""
	login_api = "https://passport2.chaoxing.com/fanyalogin" # https://passport2.chaoxing.com/api/login
	data ={
		"uname": uname,
        "password": password,
        "fid": "-1",
        # "refer":refer,
        "t": "true",
	}
	session_login = requests.session()
	res_login = session_login.post(login_api, data=data, headers=headers)
	try:
		dict = res_login.json()
		print('dict: {}'.format(dict))
		if dict['status'] == True:
			print("【登录成功】.........................")
		else:
			print("【登录失败，请检查程序】....................")
	except:
		print('【登录返回参数解析错误】.........................')
	res_login.close()
	return session_login 


def capt_token(session):
    """
        模仿点击操作,对url请求按顺序获得token令牌
        return: 返回token
    """
    # 第一个token
    url_info = "http://office.chaoxing.com/front/third/apps/seat/index?fidEnc="
    res_info = session.get(url_info, headers=headers)
    # re正则预加载
    pagetoken_re = re.compile(r"'&pagetoken=' \+ '(?P<pagetoken>.*?)'", re.I|re.S)
    pagetoken = pagetoken_re.search(res_info.text)
    if pagetoken == None:
        print("pageToken missing in chaos...")
    else:
        pagetoken = pagetoken.group("pagetoken")
        # print("pagetoken: {}".format(pagetoken)) #测试
    
    # 第二个token
    param_select = {
        "id": rommId,
		"seatNum": seatnum,
		"day": lasttime,
		"backLevel": 1,
		"pageToken": pagetoken,
    }
    url_select = "http://office.chaoxing.com/front/third/apps/seat/select"
    # re正则预加载
    token_re = re.compile(r"token: '(?P<token>\w*?)'", re.I|re.S)
    # 获取带有token的html
    res_select = session.get(url_select, headers=headers, params=param_select) 
    token = token_re.search(res_select.text)
    if token == None:
        print("token don't found in text")
    else:
        token = token.group("token")
        print("token: {}".format(token))
    return token 

def get_seat(session, token, starttime, endtime):
    """
        正式预约座位,对单个时间段(<=4h)的座位预约
        return: 座位预约信息
    """
    param_seat = {
        "roomId": rommId,
		"startTime": starttime,
		"endTime": endtime,
		"day": lasttime,
		"seatNum": seatnum,
		"captcha":"", 
		"token": token,
    }
    url_submit = "http://office.chaoxing.com/data/apps/seat/submit"
    res_submit = session.get(url_submit, headers=headers, params=param_seat)
    # 对预约结果进行判断
    res_submit_dict = res_submit.json()
    if res_submit_dict['success'] == True:
        print("时间段:{} --> {}预约成功".format(starttime, endtime))
    else:
        print("预约失败")
        print("submit-ke_girlfriend-信息: {}".format(res_submit.json()['msg']))


if __name__ == "__main__":
    # 记录时间开始
    tic = time.time()
    iphone = "188****9799"
    pwd = "d9368d52f10ebdb75e0c96c184bc799b"

    session = login(iphone, pwd)
    token = capt_token(session)
    get_seat(session, token, "7:00", "11:00")
    print("【分隔线-1】----------------------------------------------------------------------------")
    token = capt_token(session)
    get_seat(session, token, "11:00", "15:00")
    print("【分隔线-2】----------------------------------------------------------------------------")
    token = capt_token(session)
    get_seat(session, token, "15:00", "19:00")
    print("【分隔线-3】----------------------------------------------------------------------------")
    # 刻意推迟时间
    # time.sleep(0.1)
    token = capt_token(session)
    get_seat(session, token, "19:00", "22:00")
    print("【分隔线-4】----------------------------------------------------------------------------")
    # 记录时间结束
    toc = time.time()
    print("此次预约总用时: {}".format(toc-tic))



