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


if __name__ == '__main__':
    app.run(debug=True)
