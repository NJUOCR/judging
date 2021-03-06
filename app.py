import json
import os
from typing import Tuple, List
from flask import Flask, request, jsonify, render_template, Response, send_file
from werkzeug.datastructures import FileStorage
from logics.indexing import match_index
import utils.unet as unet
from logics.judging_case import JudgingCase
from logics.judging_graph import JudgingGraph
from service_invoker.service_invoke import ServiceInvoker

app = Flask(__name__)


@app.route('/index')
def main_config():
    # return send_file('static/html/main_config2.html')
    return render_template("index.html")


@app.route('/get-case')
def get_case():
    """
    获取案件或者新建案件
    :return:
    """
    args = request.args
    if 'graph_name' in args.keys():
        case = JudgingCase(args['case_id'], graph_name=args['graph_name'])
    else:
        case = JudgingCase(args['case_id'])

    return Response(json.dumps(case.get_data(lang='en')),
                    mimetype='application/json') if case.exists() else jsonify(error='指定案件不存在')


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


@app.route('/main')
def config_graph():
    args = {**request.args}
    case_id = args['case-id'][0] if 'case-id' in args else ''
    return render_template('main.html', case_id=case_id)
    # return redirect('static/html/graph_config2.html')


@app.route('/upload-graph', methods=['POST'])
def upload_graph():
    """
    接受一个`multiple`形式的文件上传请求，允许客户端一次上传多个链式证据模板配置文件
    :return:
    """
    if request.method == 'POST':
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
                return json.dumps({
                    'result': 'ok'
                })
            else:
                error_files.append(file_tuple[0])
        if len(error_files) != 0:
            return json.dumps({
                'result': 'error',
                'msg': '配置文件格式验证失败\n[%s]' % ', '.join(error_files),
            }, ensure_ascii=False, indent=2)
    else:
        return jsonify(result='error', msg='method should be post')


@app.route('/remove-graph')
def remove_graph():
    """
    删除案由
    :return:
    """
    args = request.args
    graph_name = args['graph-name']
    return jsonify(result='ok') if JudgingGraph.remove_graph(graph_name) else json.dumps({
        'result': 'error',
        'msg': '指定案由不存在'
    })


@app.route('/update-case', methods=['POST'])
def update_case():
    """
    更新一个新的案件
    :return:
    """
    if request.method == 'POST':
        case_data = request.json['case_data']
        if case_data is None:
            return jsonify(result='error', msg='uploaded data is empty')
        case_id = case_data['_id']
        case = JudgingCase(case_id)
        if case.update_case(case_data):
            return jsonify(result='ok')
        else:
            return jsonify(result='error', msg='update failed')
    else:
        return jsonify(result='error', msg='method should be post')


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
    tree = category  # 媒体资源存储的子目录
    media_name = category[-1]  # 媒体资源的名称，不是文件名，而是前端编辑的媒体名称。注意它是存储路径中最后一个子目录
    case = JudgingCase(case_id)
    assert case is not None, '不能获取案件实例，这可能是由于 数据库中没有对应案件的记录且无法根据图名初始化一个新的案件记录'
    result = case.insert_media(tree, media_name, description, file_bundle)
    return jsonify(result='ok' if result else 'error', msg='')


@app.route('/media-remove', methods=['POST'])
def media_remove():
    category: list = request.json['category'].split('/')
    case_id = category[0]
    tree = category
    case = JudgingCase(case_id)
    case.remove_media(tree)
    return jsonify(result='ok')


@app.route('/ocr', methods=['POST'])
def ocr(imgs: list=None):
    service = ServiceInvoker.which('ocr')
    param_list = request.json['imgs'] if imgs is None else imgs
    results = []
    for param in param_list:
        result = service.invoke(param)
        results.append(result)
    return jsonify(results)


@app.route('/ocr-indexing', methods=['POST'])
def ocr_indexing():
    case_id = request.json['case_id']
    param_list = request.json['imgs']
    service = ServiceInvoker.which('ocr')
    # pred = [service.invoke(param).replace('\n', '') for param in param_list]
    preds = []
    for param in param_list:
        pred = service.invoke(param)
        if pred is False:
            return jsonify(result='error', msg='ocr subsystem offline')
        else:
            preds.append(pred.replace('\n', ''))
    headers = JudgingCase(case_id).get_headers()
    headers = match_index(headers, preds)

    return jsonify(headers=headers, texts=preds)


@app.route('/upload-document', methods=['POST'])
def upload_document():
    case_id = request.values['case_id']
    file_bundle: List[Tuple[str, FileStorage]] = list(request.files.items())
    case = JudgingCase(case_id)
    relative_paths = case.save_document(file_bundle)
    return jsonify(relative_paths)


@app.route('/get-document')
def get_document():
    args = request.args
    case_id = args['case_id']
    case = JudgingCase(case_id)
    urls = case.get_document_urls()
    return jsonify(urls)


@app.route('/get-headers')
def get_headers():
    args = request.args
    case_id = args['case_id']
    case = JudgingCase(case_id)
    return jsonify(case.get_headers())


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
