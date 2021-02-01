from flask import Flask, request, send_file
import style_transfer_hub as modelStyleTransfer

app = Flask(__name__)

@app.route('/transferStyle', methods=['POST', 'GET'])
def transfer_style_route():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        modelStyleTransfer.transferStyle(data['stylePath'], data['contentPath'])
        return send_file('result.jpg', mimetype='image/jpg')
    if request.method == 'GET':
        modelStyleTransfer.transferStyle()
        return send_file('result.jpg', mimetype='image/jpg')

@app.route('/', methods=['GET'])
def index():


app.run()