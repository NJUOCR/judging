from flask import Flask, request, jsonify
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
            return {}
        else:
            return jsonify(error='no file is uploaded')
    else:
        return jsonify(error='method should be post')


if __name__ == '__main__':
    app.run()
