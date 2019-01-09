import json
import os
from typing import Tuple, List

from flask import Flask, request, jsonify, render_template, Response, send_file, redirect
from werkzeug.datastructures import FileStorage

import utils.unet as unet
from logics.judging_case import JudgingCase
from logics.judging_graph import JudgingGraph
from service_invoker.service_invoke import ServiceInvoker

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/main-graph')
def main_config():
    return send_file('static/html/main_config2.html')


@app.route('/get-case')
def get_case():
    """
    获取案件或者新建案件
    :return:
    """
    args = request.args
    if 'graph_name' in args.keys():
        case = JudgingCase(case_id=args['case_id'], graph_name=args['graph_name'])
    else:
        case = JudgingCase(case_id=args['case_id'])
    if case is None:
        return jsonify(error='指定案件不存在')
    _ = case.get_data(lang='en')
    return Response(json.dumps(case.get_data(lang='en')), mimetype='application/json')


@app.route('/get-cases')
def get_cases():
    """
    根据案由名称获得案件列表
    :return:
    """
    args = request.args
    graph_name = args['graph-name']
    return jsonify(JudgingCase.get_cases(graph_name))


@app.route('/remove-case')
def remove_case():
    """
    删除案件
    :return:
    """
    return jsonify('删除成功') if JudgingCase.remove_case(request.args['case_id']) else jsonify(error='指定案件不存在')


@app.route('/get-graph')
def get_graph():
    """
    获取图的详细定义
    :return:
    """
    # 从数据库获取一个图
    graph = JudgingGraph.from_db('默认')
    # 转化成英文
    response_json = graph.get_definition(lang='en')
    # 返回
    return Response(json.dumps(response_json, ensure_ascii=False), content_type='application/json')


@app.route('/get-graph-list')
def get_graph_list():
    """
    获取图的列表，只取图的名字
    :return:
    """
    return jsonify(JudgingGraph.get_graph_list())


@app.route('/test')
def test_upload():
    return render_template("fileinput.html")


@app.route('/config-graph')
def config_graph():
    args = {**request.args}
    case_id = args['case-id'][0] if 'case-id' in args else '测试案号123'
    return render_template('graph_config2.html', case_id=case_id)
    # return redirect('static/html/graph_config2.html')


@app.route('/remove-graph')
def remove_graph():
    """
    删除案由
    :return:
    """
    args = request.args
    print('123')
    graph_name = args['graph-name']
    return jsonify('删除成功') if JudgingGraph.remove_graph(graph_name) else jsonify(error='指定案由不存在')


@app.route('/update-case', methods=['POST'])
def update_case():
    """
    更新一个新的案件
    :return:
    """
    if request.method == 'POST':
        case_data = request.json['case_data']
        if case_data is None:
            return jsonify(error='no case data upload')
        case_id = case_data['_id']
        case = JudgingCase(case_id)
        if case.update_case(case_data):
            return jsonify('update success')
        else:
            return jsonify(error='update failed')
    else:
        return jsonify(error='method should be post')


@app.route('/upload', methods=['POST'])
def upload():
    """
    todo @杨关 因为我们的文件组件是 `multiple` 的，这边要改成多文件上传
    > 参考 `media-upload`
    使用多文件上传
    :return:
    """
    if request.method == 'POST':
        file = request.files['input-img']
        # multi files, use 'request.files.getlist(name)'
        file_bundle: List[Tuple[str, FileStorage]] = list(request.files.items())
        error_files = []
        for file_tuple in file_bundle:
            file = file_tuple[1]
            filename = unet.secure_filename(file.filename)
            raw_path = os.path.join('./static/graph_configs', filename)
            file.save(raw_path)
            dic = JudgingGraph.from_file("static/graph_configs/" + filename)
            if dic.validate():
                dic.save()
                return jsonify("上传成功")
            else:
                error_files.append(file_tuple[0])
        if len(error_files) != 0:
            return jsonify(error=str(error_files)+'json格式错误，请重新上传')
    else:
        return jsonify(error='method should be post')


@app.route('/favicon.ico')
def send_icon():
    return send_file('./favicon.ico')


@app.route('/media-upload', methods=['POST'])
def media_upload():
    """
    前端会检查上传文件的类型，在某一次上传中，数据可以是：
    - 一个视频文件
    - 或一个音频文件
    - 或多个图片文件

    ** 注意将文件名中的空格替换成`_` **，*linux不允许文件名包含空格*

    文件存储位置：
    根目录为`static/resources/media`
    子目录根据前端传来的一个列表 `['{案号}', '{证据链节点名称}', '{查证事项节点名称}', '视听材料', '{媒体名称}']`

    > 目前先不更新数据库
    :return:
    """
    category: list = request.values['category'].split('/')
    description = request.values['description']
    file_bundle: List[Tuple[str, FileStorage]] = list(request.files.items())

    if len(file_bundle) == 0:
        return jsonify(error='No file is uploaded.')

    case_id = category[0]  # 案号
    tree = category[1:]  # 媒体资源存储的子目录
    media_name = category[-1]  # 媒体资源的名称，不是文件名，而是前端编辑的媒体名称。注意它是存储路径中最后一个子目录
    case = JudgingCase(case_id)
    assert case is not None, '不能获取案件实例，这可能是由于 数据库中没有对应案件的记录且无法根据图名初始化一个新的案件记录'
    result = case.insert_media(tree, media_name, description, file_bundle)
    return jsonify(msg='ok' if result else 'duplicate media name found')


@app.route('/media-remove', methods=['POST'])
def media_remove():
    category: list = request.json['category'].split('/')
    case_id = category[0]
    tree = category[1:]
    case = JudgingCase(case_id)
    case.remove_media(tree)
    return jsonify(msg='ok')


@app.route('/ocr', methods=['POST'])
def ocr():
    service = ServiceInvoker.which('ocr')
    path = request.json['staticPath']
    result = service.invoke({
        'path': path
    })

    return jsonify(msg='error') if result is False else jsonify(txt=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
