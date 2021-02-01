from flask import Flask, request, send_file
import style_transfer_hub

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        main.transferStyle(data['stylePath'], data['contentPath'])
        return send_file('result.jpg', mimetype='image/jpg')
    if request.method == 'GET':
        main.transferStyle()
        return send_file('result.jpg', mimetype='image/jpg')