# coding=utf-8
import os
import json
import requests
import re
import xlwt
from xlwt import Pattern


fname = 'api_doc.xls'
urls = {
    'pay_svc': 'http://XXX.com/pay/v2/api-docs',
    'index_svc': 'http://XXX.com/index-microservice/v2/api-docs',
    'workflow_svc': 'http://XXX.com/bizWorkflow/v2/api-docs'
}


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36)"}


file_name = "scv.csv"


class Api:

    def __init__(self, name, url, req_method, req_type, resp_type, parameter_items, resp_result):
        self.name = name
        self.url = url
        self.req_method = req_method
        self.req_type = req_type
        self.resp_type = resp_type
        self.parameter_items = parameter_items
        self.resp_result = resp_result

    def out(self):
        print(self.name, "--", self.url, "--", self.req_method, "--",
              self.req_type, "--", self.resp_type, "--", self.parameter_items, self.resp_result)


class Parameter:

    def __init__(self, name, type, required, desc):
        self.name = name
        self.type = type
        self.required = required
        self.desc = desc
    def out(self):
        print(self.name, "--", self.type, "--", self.required, "--", self.desc)


class Result:

    def __init__(self, code, msg, success, data):
        self.code = code
        self.msg = msg
        self.success = success
        self.data = data
    def out(self):
        print(self.code, "--", self.msg, "--", self.success, "--", self.data)


# 生成API


def obj_extract_def(svc_definitions, cls_name):

    fileds = svc_definitions[cls_name]["properties"]
    for name, _ in fileds.items():

        if name == "orderBy":

            parameter = Parameter(

                name, fileds[name]["type"], "False", "排序字段")

        elif name == "pageIndex":

            parameter = Parameter(

                name, fileds[name]["type"], "False", "页数")

        elif name == "pageSize":

            parameter = Parameter(

                name, fileds[name]["type"], "False", "每页大小")

        else:
            desc = ""

            if "description" in fileds[name]:

                desc = fileds[name]["description"]

            parameter = Parameter(

                name, fileds[name]["type"], "False", desc)

    return parameter


def param_extract_def(data,  method_name):
    parameter_list = list()
    if "parameters" in data.get(method_name):
        params = data.get(method_name)["parameters"]
        # 参数是数组
        for p in params:
            if "schema" in p:
                parameter = Parameter(
                    p["name"],  "array", p["required"], p["description"])
                parameter_list.append(parameter)
            else:
                if "description" in p:
                    parameter = Parameter(
                        p["name"], p["type"], p["required"], p["description"])
                else:
                    parameter = Parameter(
                        p["name"], p["type"], p["required"], "")
                parameter_list.append(parameter)
    return parameter_list


def gen_apidoc():
    
    svc_dic_list = dict()
    for svc_name, url in urls.items():
        print(url)
        api_list = list()
        response = requests.get(url, headers=headers).text
        # 转化为字符串
        json_str = json.loads(response)
        # url和参数信息
        svc_path = json_str['paths']
        svc_definitions = json_str['definitions']
        for svc, data in svc_path.items():
            # 排除其他的
            req = data.get('post')
            req_method = 'post'
            summary = ""
            if req == '' or req is None:
                req = data.get('get')
                req_method = 'get'
            if req == '' or req is None:
                req = data.get('put')
                req_method = 'put'
            if req == '' or req is None:
                req = data.get('delete')
                req_method = 'delete'
            if req is not None:
                summary = req.get('summary')
            # 参数列表
            parameter_list = list()
            # post请求
            if req_method == "post":
                if "parameters" not in data.get("post"):
                    parameter = Parameter("", "", "", "")
                    parameter_list.append(parameter)
                    continue
                params = data.get("post")["parameters"]
                response_result = data.get("post")["responses"]
                schema = False
                obj = None
                for cdict in params:
                    if cdict.get("schema") != None:
                        schema = True
                        obj = cdict["schema"]
                if schema:
                    # 参数是数组
                    if "items" in obj:
                        if "$ref" in obj["items"]:
                            cls_name = obj["items"]["$ref"].split("/")[2]
                            parameter = obj_extract_def(
                                svc_definitions, cls_name)
                        else:
                            parameter = Parameter(
                                parm["name"], parm["type"], parm["required"], parm["description"])
                    # 参数是对象
                    else:
                        cls_name = obj["$ref"].split("/")[2]
                        parameter = obj_extract_def(svc_definitions, cls_name)
                    parameter_list.append(parameter)

                else:
                    for parm in params:
                        if "description" in parm:
                            parameter = Parameter(
                                parm["name"], parm["type"], parm["required"], parm["description"])
                        else:
                            parameter = Parameter(
                                parm["name"], parm["type"], parm["required"], "")
                        parameter_list.append(parameter)

            elif req_method == "delete":
                # delete请求
                response_result = data.get("delete")["responses"]
                parameter_list = param_extract_def(data, "delete")
            elif req_method == "put":
                # delete请求
                response_result = data.get("put")["responses"]
                parameter_list = param_extract_def(data, "put")
            else:
                # get请求
                response_result = data.get("get")["responses"]
                parameter_list = param_extract_def(data, "get")
            result_str = "CommonResult"
            if "schema" in response_result["200"]:
                if "$ref" in response_result["200"]["schema"]:
                    result_str = response_result["200"]["schema"]["$ref"].split("/")[2]
            # 返回类型
            result = pase_response(result_str, svc_definitions)
            api = Api(summary, svc, req_method, "application/json","json", parameter_list, result)
            api_list.append(api)
            
        svc_dic_list[svc_name] = api_list

    return svc_dic_list


def pase_cls(cls_name, svc_definitions):
    fileds = svc_definitions[cls_name]["properties"]
    for name, _ in fileds.items():
        if name == "orderBy":
            parameter = Parameter(
                name, fileds[name]["type"], "False", "排序字段")
        elif name == "pageIndex":
            parameter = Parameter(
                name, fileds[name]["type"], "False", "页数")
        elif name == "pageSize":
            parameter = Parameter(name, fileds[name]["type"], "False", "每页大小")
        else:
            if "description" in fileds[name]:
                parameter = Parameter(
                    name, fileds[name]["type"], "False", fileds[name]["description"])
            else:
                parameter = Parameter(name, fileds[name]["type"], "False", "")

    return parameter


def pase_response(result_cls, svc_definitions):
    if result_cls == "CommonResult":
        parameter = Parameter("data", "null", "False", "null")
        result = Result("200", "ok", "true", parameter)
        return result
    elif result_cls == "ObjectNode":
        parameter = Parameter("data", "ObjectNode", "False", "null")
        result = Result("200", "ok", "true", parameter)
        return result
    if result_cls.count("«") > 1:
        cls_name = result_cls.split("«")[2][:-2]
    else:
        cls_name = result_cls.split("«")[1][:-1]

    if cls_name == "bigdecimal" or cls_name == "integer" or cls_name == "long" or cls_name == "int" or cls_name == "float":
        parameter = Parameter("data", cls_name, "False", " ")
        result = Result("200", "ok", "true", parameter)
    elif cls_name == "boolean":
        parameter = Parameter("data", cls_name, "False", " ")
        result = Result("200", "ok", "true", parameter)
    elif cls_name == "string":
        parameter = Parameter("data", cls_name, "False", " ")
        result = Result("200", "ok", "true", parameter)
    elif cls_name == "object":
        parameter = Parameter("data", cls_name, "False", " ")
        result = Result("200", "ok", "true", parameter)
    elif cls_name == "Void":
        parameter = Parameter("data", cls_name, "False", " ")
        result = Result("200", "ok", "true", parameter)
    elif "properties" in svc_definitions[cls_name]:
        fileds = svc_definitions[cls_name]["properties"]
        parameter_list = list()
        for name, _ in fileds.items():
            if name == "orderBy":
                parameter = Parameter(
                    name, fileds[name]["type"], "False", "排序字段")
            elif name == "pageIndex":
                parameter = Parameter(
                    name, fileds[name]["type"], "False", "页数")
            elif name == "pageSize":
                parameter = Parameter(
                    name, fileds[name]["type"], "False", "每页大小")
            elif fileds[name]["type"] == "array":
                cls_name = fileds[name]["items"]["$ref"].split("/")[2]
                parameter = pase_cls(cls_name, svc_definitions)
            else:
                try:
                    parameter = Parameter(
                        name, fileds[name]["type"], "False", fileds[name]["description"])
                except:
                    continue
            parameter_list.append(parameter)
        result = Result("200", "ok", "true", parameter_list)
    else:
        parameter = Parameter(cls_name, "object", "false", "")
        result = Result("200", "ok", "true", parameter)

    return result


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
    f_sheet.col(2).width = 256*20
    f_sheet.col(3).width = 256*20
    f_sheet.col(4).width = 256*60

    dex = 0

    for api in api_list:
        #name, url, req_method, req_type, resp_type, parameter_items
        for t in range(5):
            f_sheet.write_merge(dex, dex+0, 0, 3, api.name,
                                set_style(font_name, 240, 57, True))

            f_sheet.write(1+dex, 0, "接口名称",
                          set_style(font_name, font_size))

            f_sheet.write_merge(1+dex, dex+1, 1, 3, api.name,
                                set_style(font_name, font_size))

            f_sheet.write(2+dex, 0, "URL", set_style(font_name, font_size))

            f_sheet.write_merge(2+dex, dex+2, 1, 3, api.url,
                                set_style(font_name, font_size))

            f_sheet.write(3+dex, 0,  "请求方式", set_style(font_name, font_size))

            f_sheet.write_merge(3+dex, dex+3, 1, 3, api.req_method,
                                set_style(font_name, font_size))

            f_sheet.write(4+dex, 0, "请求类型", set_style(font_name, font_size))

            f_sheet.write_merge(4+dex, dex+4, 1, 3,  api.req_type,
                                set_style(font_name, font_size))

            f_sheet.write(5+dex, 0, "返回类型", set_style(font_name, font_size))

            f_sheet.write_merge(5+dex, dex+5, 1, 3, api.resp_type,
                                set_style(font_name, font_size))

            f_sheet.write_merge(6+dex, dex+6, 0, 3, "请求参数",
                                set_style(font_name, font_size, 21, True))

            # 参数
            f_sheet.write(dex+7, 0, "参数名称",
                          set_style(font_name, font_size, 0, True))

            f_sheet.write(dex+7, 1, "数据类型",
                          set_style(font_name, font_size, 0, True))

            f_sheet.write(dex+7, 2, "是否必填",
                          set_style(font_name, font_size, 0, True))

            f_sheet.write(dex+7, 3, "参数说明",
                          set_style(font_name, font_size, 0, True))

            # 参数信息

            sub_dex = dex+8
            for sub in api.parameter_items:
                #name, type, required, desc
                required = "True"
                if sub.required == "FALSE":
                    required = "False"
                f_sheet.write(sub_dex, 0, sub.name,
                              set_style(font_name, font_size))

                f_sheet.write(sub_dex, 1, sub.type,
                              set_style(font_name, font_size))

                f_sheet.write(sub_dex, 2,  required,
                              set_style(font_name, font_size))

                f_sheet.write(sub_dex, 3, sub.desc,
                              set_style(font_name, font_size))

                sub_dex = sub_dex+1
        dex = sub_dex
        f_sheet.write_merge(dex, dex, 0, 3, "响应参数",
                            set_style(font_name, font_size, 57, True))

        # 返回参数

        f_sheet.write(1+dex, 0, "参数名称",
                      set_style(font_name, font_size, 0, True))

        f_sheet.write(1+dex, 1, "数据类型",
                      set_style(font_name, font_size, 0, True))

        f_sheet.write_merge(1+dex, 1+dex, 2, 3, "参数说明",
                            set_style(font_name, font_size, 0, True))

        cls_type = str(type(api.resp_result.data))

        print(cls_type, "---------", api.url)

        resp_dex = dex+2

        if isinstance(api.resp_result.data, list):
            for sub in api.resp_result.data:
                f_sheet.write(resp_dex, 0, sub.name,
                              set_style(font_name, font_size))
                f_sheet.write(resp_dex, 1, sub.type,
                              set_style(font_name, font_size))
                f_sheet.write_merge(resp_dex, resp_dex, 2, 3, sub.desc,
                                    set_style(font_name, font_size))
                resp_dex = resp_dex+1
        else:
            print(api.resp_result.data)
            sub = api.resp_result.data
            f_sheet.write(resp_dex, 0, sub.name,
                          set_style(font_name, font_size))
            f_sheet.write(resp_dex, 1, sub.type,
                          set_style(font_name, font_size))
            f_sheet.write_merge(resp_dex, resp_dex, 2, 3, sub.desc,
                                set_style(font_name, font_size))
            resp_dex = resp_dex+1
        dex = resp_dex+1


# 生成数据库文档


def sava_doc():
    svc_list = gen_apidoc()
    wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
    nums = 0
    for svc_name, api_list in svc_list.items():
        nums = nums+len(api_list)
        print("start generating......")
        write_excel(wb, svc_name, api_list)
        print("finished", "\n=========================================================")
        f_path = os.path.join(os.getcwd()+fname)
        if os.path.exists(f_path):
            os.remove(f_path)
        wb.save(f_path)
    if os.path.exists(fname):
        os.remove(fname)
    wb.save(fname)

    print("Document has been generated")


if __name__ == "__main__":

    sava_doc()