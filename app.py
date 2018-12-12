from flask import Flask, request, jsonify, render_template, Response, send_file
from logics.judging_graph import JudgingGraph
import json
import utils.unet as unet
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get-graph')
def get_graph():
    """
    获取图的详细定义
    :return:
    """
    # 从数据库获取一个图
    graph = JudgingGraph.from_db('默认')
    # 转化成英文
    response_json = JudgingGraph.translate_definition('en', graph.definition)
    response_json.pop("_id")
    print(response_json)
    # 返回
    return Response(json.dumps(response_json, ensure_ascii=False), content_type='application/json')


@app.route('/get-graph-list')
def get_graph_list():
    """
    获取图的列表，只取图的名字
    :return:
    """


@app.route('/test')
def test_upload():
    return render_template("fileinput.html")


@app.route('/config-graph')
def config_graph():
    # return render_template('graph_config.html')
    return send_file('static/html/graph_config2.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['input-img']
        # multi files, use 'request.files.getlist(name)'
        if file:
            filename = unet.secure_filename(file.filename)
            raw_path = os.path.join('./static/graph_configs', filename)
            file.save(raw_path)
            dic = JudgingGraph.from_file("static/graph_configs/"+filename)
            if dic.validate():
                dic.save()
                return jsonify("上传成功")
            else:
                return jsonify(error='json格式错误，请重新上传')
        else:
            return jsonify(error='no file is uploaded')
    else:
        return jsonify(error='method should be post')


@app.route('/favicon.ico')
def send_icon():
    return send_file('./favicon.ico')


@app.route('/media-upload')
def media_upload():
    """
    todo @熊 为媒体资源的上传提供后台接口
    前端会检查上传文件的类型，在某一次上传中，数据可以是：
    - 一个视频文件
    - 或一个音频文件
    - 或多个图片文件

    ** 注意将文件名中的空格替换成`_` **，*linux不允许文件名包含空格*

    文件存储位置：
    根目录为`static/resources/media`
    子目录根据前端传来的一个列表 `['{案号}', '{证据链节点名称}', '{查证事项节点名称}', '视听材料', '{材料名称}']`

    > 目前先不更新数据库
    :return:
    """

if __name__ == '__main__':
    app.run(debug=True)
