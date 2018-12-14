from flask import Flask, request, jsonify, render_template, Response, send_file, make_response
from logics.judging_graph import JudgingGraph
import json
import utils.unet as unet
import os
import shutil

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
            dic = JudgingGraph.from_file("static/graph_configs/" + filename)
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


@app.route('/media-upload', methods=['POST'])
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
    print("accepted")
    video_list = ['avi', 'asf', 'asx', 'rm', 'rmvb', 'mpg', 'mpeg', 'mpe', '3gp', 'mov', 'mp4', 'm4v', 'dat', 'mkv',
                  'flv', 'vob']
    audio_list = ['mp3', 'aac', 'wav', 'wma', 'cda', 'flac', 'm4a', 'mid', 'mka', 'mp2', 'mpa', 'mpc', 'ape', 'ofr',
                  'ogg', 'ra', 'wv', 'tta', 'ac3', 'dts']
    image_list = ['jpg', 'bmp', 'eps', 'gif', 'mif', 'miff', 'png', 'tif', 'tiff', 'svg', 'wmf', 'jpe', 'jpeg', 'dib',
                  'ico', 'tga', 'cut', 'pic']

    if request.method == 'POST':
        sign = 0
        error_list = []
        files = request.form["filenames"].split(",")
        print(files)
        if len(files) == 0:
            return jsonify(error='no file is uploaded')
        elif len(files) == 1:
            filename = files[0]
            names = filename.split(".")
            post = names[-1]
            if post in video_list or post in audio_list:
                sign = 1
            elif post in image_list:
                sign = 2
            else:
                return jsonify(error=filename+'\' type can\'t be recognized')
        else:
            for file in files:
                filename = file
                print(filename)
                names = filename.split(".")
                post = names[len(names) - 1]
                if post not in image_list:
                    error_list.append(filename)
                    files.remove(file)
            sign = 2

        print(sign)
        print("here!")
        root = os.path.join("static", "resources", "media")
        subdir = request.values["category"]
        subdir = subdir.replace('[', '').replace(']', '').replace(" ", "_")
        print(subdir)
        dir_list = subdir.split(',')

        # multi files, use 'request.files.getlist(name)'
        if files:
            if sign == 1:
                filename = files[0]
                file = request.files[filename]
                raw_path = os.path.join(os.getcwd(), root, dir_list[0], dir_list[1], dir_list[2], '视听材料')
                if os.path.exists(raw_path) is False:
                    os.makedirs(raw_path)
                    print(raw_path)
                file.save(os.path.join(raw_path, filename))
            elif sign == 2:
                raw_path = os.path.join(os.getcwd(), root, dir_list[0], dir_list[1], dir_list[2], '视听材料', dir_list[4])
                if os.path.exists(raw_path) is False:
                    os.makedirs(raw_path)
                for filename in files:
                    file = request.files[filename]
                    file.save(os.path.join(raw_path, filename))
            if len(error_list) != 0:
                error_files = ""
                for file in error_list:
                    error_files = error_files + file + ','
                error_files.rstrip(',')
                return jsonify(error=error_files+'\'s type can\'t be recognized')
            # while appear cors problem
            # response_text = jsonify("true")
            # rst = make_response(response_text)
            # rst.headers['Access-Control-Allow-Origin'] = '*'
            return jsonify('true')
        else:
            return jsonify(error='no file is uploaded')
    else:
        return jsonify(error='method should be post')


if __name__ == '__main__':
    app.run(debug=True)
