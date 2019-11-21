import requests
import random
import time
import urllib3
urllib3.disable_warnings()

url = 'https://www.cii-contest.cn/api/common/vote/voteWorks.json'
param = 'ids=27'

cookie_vot = "05e2.dec197c92dc40.2e5e6f95-6cb7.206a2bea2-d9ba.58d29a8f-faef.909fc5f72-efca.21993ff08ca3b.d7be3cd82afb7.b1148cabf"
cookie_gy = "739b08a8-b979-4549-bd34-fe307612703d"

random_str = "abcdefghijklmnopqrstuvwxyz1234567890"


def get_header():

    f1 = random.randint(0, 35)
    v_f = random.randint(0, 100)
    vot_list = list(cookie_vot)
    rep_str1 = vot_list[v_f]
    if rep_str1 != "." and rep_str1 != "-":
        vot_list[v_f] = random_str[f1]
    vot_ssr = "".join(vot_list)
    rest_vot = "voteCookie="+vot_ssr+";"

    f2 = random.randint(0, 35)
    g_f = random.randint(0, 30)
    gy_list = list(cookie_gy)
    rep_str2 = gy_list[g_f]
    if rep_str2 != "." and rep_str2 != "-":
        gy_list[g_f] = random_str[f2]
    gy_ssr = "".join(gy_list)
    rest_gy = "GY_SESSION="+gy_ssr

    header_dict = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Origin': 'https://www.cii-contest.cn',
        'Host': 'www.cii-contest.cn',
        'Connection': 'keep-alive',
        'model': 'json',
        'Sec-Fetch-Site': 'same-origin',
        'Referer': 'https: // www.cii-contest.cn/vote_page.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.16 Safari/537.36 Edg/79.0.309.12',
        'Cookie': rest_vot+rest_gy
    }

    return header_dict


def vote():
    header_dict = get_header()
    count = 0
    while (True):
        r_time = random.randint(0, 20)
        if count > 300:
            break
        if count % 10 == 0:
            print("================",count,"=========================")
            header_dict = get_header()
        time.sleep(r_time)
        respon = requests.post(
            url, data=param, headers=header_dict, verify=False)
        print(respon.text)
        print(respon.status_code)
        count = count + 1


if __name__ == "__main__":
    vote()
