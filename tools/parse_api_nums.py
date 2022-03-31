# coding=utf-8
import os
import json
import requests
import re
import xlwt
from xlwt import Pattern

fname = '/tools/api_doc_nums.xls'

urls = {
    'customer_svc': 'https://cloud.xinyilian.com/customer/v2/api-docs',
    'product_svc':  'https://cloud.xinyilian.com/product/v2/api-docs',
    'order_svc': 'https://cloud.xinyilian.com/order/v2/api-docs',
    'rbac_svc':  'https://cloud.xinyilian.com/rbac/v2/api-docs',
    'pay_svc':  'https://cloud.xinyilian.com/pay/v2/api-docs',
    'cms_svc':  'https://cloud.xinyilian.com/cms/v2/api-docs',
    'industrial_svc':  'https://cloud.xinyilian.com/industrial/v2/api-docs',
    'wms-collaboration_svc':  'https://cloud.xinyilian.com/wms-collaboration/v2/api-docs',
    'mmt_svc':  'https://cloud.xinyilian.com/mmt/v2/api-docs',
    'im_svc':  'https://cloud.xinyilian.com/im/v2/api-docs',
    'oms_svc': 'https://cloud.xinyilian.com/oms/v2/api-docs'
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36)"}


class Api:
    def __init__(self, name, url):
        self.name = name
        self.url = url

# 生成API


def gen_apidoc():

    svc_list = dict()
    for svc_name, url in urls.items():
        print("---------------------------------------------------------------")
        response = requests.get(url, headers=headers).text
        # 转化为字符串
        json_str = json.loads(response)
        svc_path = json_str['paths']

        api_list = list()
        for svc, data in svc_path.items():
            print(svc)
            req = data.get('post')
            req_method = 'post'
            summary = ""
            if req == '' or req is None:
                req = data.get('get')
            if req == '' or req is None:
                req = data.get('put')
            if req == '' or req is None:
                req = data.get('delete')
            if req is not None:
                summary = req.get('summary')

            print(svc, summary)

            api = Api(summary, svc)
            api_list.append(api)

        svc_list[svc_name] = api_list

    return svc_list


# 设置格式

def set_style(name, height, bg_Color=0, bold=False):
    # 设置字体
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    # 设置边框
    borders = xlwt.Borders()
    # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
    # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style.borders = borders

    if bg_Color != 0:
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = bg_Color  # 设置单元格背景色为黄色
        style.pattern = pattern

    return style

# 写Excel


def write_excel(wb, sheet_name, api_list):
    font_size = 200
    font_name = 'Microsoft YaHei UI'

    f_sheet = wb.add_sheet(sheet_name, cell_overwrite_ok=True)
    f_sheet.col(0).width = 256*20
    f_sheet.col(1).width = 256*40

    f_sheet.write(0, 0, "接口名称", set_style(font_name, font_size))
    f_sheet.write(0, 1, "URL", set_style(font_name, font_size))
    dex = 1
    for api in api_list:
        #name, url
        f_sheet.write(dex, 0, api.name,
                      set_style(font_name, font_size))
        f_sheet.write(dex, 1, api.url,
                      set_style(font_name, font_size))
        dex = dex+1


# 生成数据库文档

def sava_doc():
    svc_list = gen_apidoc()
    nums = 0
    wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
    for svc_name, api_list in svc_list.items():

        nums = nums+len(api_list)

        print("start generating......")
        write_excel(wb, svc_name, api_list)
        print("finished", "\n=========================================================")

        f_path = os.path.join(os.getcwd()+fname)
        if os.path.exists(f_path):
            os.remove(f_path)
        wb.save(f_path)

        print("Document has been generated")

    print(nums)

if __name__ == "__main__":

    sava_doc()
