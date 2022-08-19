# coding=utf-8
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36)"}
base_url = "https://www.geilicx.com/xzqh/index?k={0}"


def main():
    df_towns = pd.read_excel('./tools/towns.xlsx')
    full_divislons = list()
    error_towns = list()
    for index, row in df_towns.iterrows():
        code = row['code']
        longitude = row['longitude']
        latitude = row['latitude']
        full_url = base_url.format(code)
        r_html = requests.get(full_url, headers=headers).text
        soup = BeautifulSoup(r_html, "html.parser")
        p_text = soup.find_all("table")[0].find_all("p")

        if p_text is not None and len(p_text) > 0:
            province = p_text[0].find_all("b")[0].string
            city = p_text[0].find_all("b")[1].string
            district = p_text[0].find_all("b")[2].string
            if len(p_text[0].find_all("b")) > 3:
                town = p_text[0].find_all("b")[3].string
            else:
                town = town

            dict_divislons = {"province": province, "city": city,
                              "district": district, "town": town, "longitude": longitude, "latitude": latitude}
            full_divislons.append(dict_divislons)
        else:
            name = row['name']
            error_towns.append({"code": code, "name": name,
                               "longitude": longitude, "latitude": latitude})
            print(code)
        time.sleep(random.uniform(0.6, 2.3))

    df_divislons = DataFrame(full_divislons)
    df_divislons.columns = ["省", "市", "县/区", "乡/镇", "经度", "维度"]
    df_divislons.to_csv('divislons.csv', encoding='utf_8_sig')

    df_towns = DataFrame(error_towns)
    df_towns.columns = ["行政编码", "名称", "经度", "维度"]
    df_towns.to_csv("error_towns.csv", encoding='utf_8_sig')


api_url = "https://api.map.baidu.com/reverse_geocoding/v3/?ak=11111&output=json&location={0},{1}"


def baidu_api():
    df_towns = pd.read_excel('./tools/towns.xlsx')
    full_divislons = list()
    error_towns = list()
    for index, row in df_towns.iterrows():
        code = row['code']
        name = row['name']
        longitude = row['longitude']
        latitude = row['latitude']
        full_url = api_url.format(latitude, longitude)
        r_json = requests.get(full_url, headers=headers).json()
        addressComponent = r_json["result"]["addressComponent"]
        province = addressComponent["province"]
        city = addressComponent["city"]

        if "district" in addressComponent:
            district = addressComponent["district"]
        else:
            district = city
        dict_divislons = {"province": province, "city": city,
                              "district": district, "town": name, "longitude": longitude, "latitude": latitude}
        full_divislons.append(dict_divislons)
        
    df_divislons = DataFrame(full_divislons)
    df_divislons.columns = ["省", "市", "县/区", "乡/镇", "经度", "维度"]
    df_divislons.to_csv('divislons.csv', encoding='utf_8_sig')
    print("==================finished===================")

if __name__ == '__main__':
    # main()
    baidu_api()
