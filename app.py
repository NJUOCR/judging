from flask import Flask, request, jsonify, render_template, Response
from logics.judging_graph import JudgingGraph
import utils.unet as unet
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test')
def testupload():
    return render_template("fileinput.html")


@app.route('/config-graph')
def config_graph():
    return render_template('graph_config.html')


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
