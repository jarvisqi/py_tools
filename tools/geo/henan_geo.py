import requests
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36)"}

api_url = "https://geo.datav.aliyun.com/areas_v2/bound/{0}_full.json"

dv_list = {410100,
           410200,
           410300,
           410400,
           410500,
           410600,
           410700,
           410800,
           410900,
           411000,
           411100,
           411200,
           411300,
           411400,
           411500,
           411600,
           411700,
           41900100}


def main():

    for dv in dv_list:
        full_url = api_url.format(dv)
        r_json = requests.get(full_url, headers=headers).text
        with open("./henan/"+str(dv)+".json", "w", encoding="utf-8") as f:
            f.write(r_json)


if __name__ == '__main__':
    main()
