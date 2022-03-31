from flask import Flask
from flask import request
from flask import Response
import pymysql
import xlwt
import os
import mimetypes


db_url = "10.0.0.151"  # 连接地址
db_username = "root"  # 用户名
db_password = "123456"  # 连接密码
db_database = "zentao"  # 数据库名
db_port = 3306
file_name = "report.xls"


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return {
        "msg": "success",
        "data": "welcome to use ltd"
    }


@app.route('/rep', methods=['GET', 'POST'])
def all_report():
    s_date = request.args.get("s")
    e_date = request.args.get("s")

    sql = "SELECT u.account ,u.realname , p.name , 	tt.consumed , tt.date  \
    FROM  zt_taskestimate tt LEFT JOIN zt_user u ON u.account = tt.account 	LEFT JOIN zt_task t on t.id=tt.task \
	LEFT JOIN zt_project p on p.id=t.project  WHERE date BETWEEN '{}' AND '{}'  \
    AND tt.consumed > 0 ORDER BY tt.account".format(s_date, e_date)

    results = db_query(sql)
    file_name = write_excel(list(results))
    # 下载文件
    response = Response(file_iterator(file_name))
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers["Content-Disposition"] = 'attachment;filename="{}"'.format(file_name)
    return response

    return {
        "msg": "success",
        "data": response
    }


def write_excel(result):
    # 创建excel对象
    f = xlwt.Workbook()
    task_sheet = f.add_sheet('工时明细', cell_overwrite_ok=True)
    # 列字段
    column_names = ['工号', '姓名', '项目', '工时', '日期']
    # 写第一行，也就是列所在的行
    for i in range(0, len(column_names)):
        task_sheet.write(0, i, column_names[i])

    # 写入多行
    num = 0  # 计数器
    for i in result:
        task_sheet.write(num + 1, 0, i[0])
        task_sheet.write(num + 1, 1, i[1])
        task_sheet.write(num + 1, 2, i[2])
        task_sheet.write(num + 1, 3, i[3])
        task_sheet.write(num + 1, 4, i[4])
        # 日期转换为字符串
        value = i[4].strftime('%Y-%m-%d')
        task_sheet.write(num + 1, 4, value)

        num += 1  # 自增1

    # 删除已存在的文件
    if os.path.exists(file_name):
        os.remove(file_name)
    # 保存文件
    f.save(file_name)

    return file_name


def file_iterator(file_path, chunk_size=512):
    """
        文件读取迭代器
    :param file_path:文件路径
    :param chunk_size: 每次读取流大小
    :return:
    """
    with open(file_path, 'rb') as target_file:
        while True:
            chunk = target_file.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break

# 连接数据库


def conn_db():
    # 连接数据库
    db = pymysql.Connect(
        host=db_url,
        user=db_username,
        passwd=db_password,
        db=db_database,
        port=db_port,
        charset='utf8'
    )
    cursor = db.cursor()
    return cursor


def db_query(sql: str):
    db_cursor = conn_db()
    try:
        db_cursor.execute(sql)
        results = db_cursor.fetchall()
        return results
    except Exception as e:
        print('SQL执行失败: : % s' % str(sql))
        print(e)
    db_cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
