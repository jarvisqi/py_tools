from flask import Flask, request, jsonify, render_template
from core.doc_vector_sim import DocVectSim

app = Flask(__name__)
# 返回值显示中文
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/text/querydocsim', methods=['POST'])
def query_docsim():
    """
    获取文档相似度
    POST
    {"keep_val":0.8,"sysno":103,"title":"计算相似度","content":"文档相似度参数说明"}
    :return: 相似文档的数据库系统编号
    """
    if request.data is None or len(request.data) == 0:
        return jsonify({"data": None, "success": False, "Message": "无效的参数"})

    data_dic = eval(request.data)
    if not isinstance(data_dic, dict) or len(data_dic) < 4:
        return jsonify({"data": None, "success": False, "Message": "参数格式不正确"})
    try:
        val = data_dic.get("keep_val")
        sysno = data_dic.get("sysno")
        title = data_dic.get("title")
        content = data_dic.get("content")
    except:
        return jsonify({"data": None, "success": False, "Message": "参数错误"})

    doc = DocVectSim(keep_val=val)
    title_ids = doc.similarity("title", sysno, title)
    content_ids = doc.similarity("content", sysno, content)

    data = {"title_ids": title_ids, "content_ids": content_ids}
    return jsonify({"data": data, "success": True, "Message": "ok"})


if __name__ == '__main__':
    app.run(port=9001, debug=True)
