import os
import xlwt
from datetime import datetime

station_list = [57290, 57298, 57077, 53898, 54817, 57088, 57084, 57090, 57396, 58004, 58007, 57192, 58017, 57180, 53998, 57171, 57186, 57083,
                57197, 57099, 57087, 58208, 58104, 57273, 57281, 53978, 57178, 57195, 57390, 53989, 58101, 54902, 57183, 53985, 57085, 54903,
                53993, 57271, 53991, 54901, 57189, 57188, 57294, 57081, 53990, 57089, 58100, 53992, 57095, 57098, 57191, 53994, 57196, 53974,
                58301, 57175, 53972, 53889, 57169, 57078, 57065, 57184, 53983, 57091, 57080, 57181, 57063, 57185, 57079, 58205, 57295, 57072,
                57292, 57093, 57274, 58005, 57094, 57086, 57296, 58207, 57176, 57066, 57074, 58111, 57076, 53984, 57162, 53987, 57075, 57096,
                54900, 57198, 53988, 57051, 57194, 58001, 57285, 57293, 57299, 57156, 57067, 57179, 58006, 58008, 57182, 57071, 53997, 53995, 
                57187, 57177, 57070, 53986, 53979, 53982, 57173, 57056, 57261, 57190]
target_stations = ''.join(str(x) for x in station_list)

folder_path = 'D:\\henan\\data\\'  # 文件夹路径
target_hour = '08'  # 目标小时数

def parse_data():
    wb_book = xlwt.Workbook(encoding='utf-8')  # 新建excel文件
    wb_sheet = wb_book.add_sheet('data')  # 添加
    row = 0
    for filename in os.listdir(folder_path):
        time_str = filename.split('.')[0]  # 提取文件名中的日期时间信息
        time_h = time_str[-2:]
        if target_hour == time_h:
            with open(folder_path+filename, 'r') as f:
                for line in f:
                    arr_line = line.split('\t')
                    first_col = arr_line[0]
                    if first_col in target_stations:
                        col = 0
                        for i in range(len(arr_line)):
                            wb_sheet.write(row, i, arr_line[i])
                        row += 1
    # 保存文件
    wb_book.save("data.xls")


if __name__ == '__main__':
    parse_data()