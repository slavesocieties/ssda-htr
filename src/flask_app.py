from flask import Flask, request, jsonify
import requests
import os
from driver import driver
app = Flask(__name__)


@app.route('/segmentation', methods = ['POST'])
def segmentatation():
    data = request.json
    print(request)
    vol = data["vol"]
    img = data["img"]
    str_im = '0' * (4 - len(str(img))) + str(img)
    obj_key = vol + '-' + str_im + '.jpg'
    url = 'https://zoqdygikb2.execute-api.us-east-1.amazonaws.com/v1/ssda-production-jpgs/' + obj_key
    response = requests.get(url)
    filename = f'{obj_key}_temp.jpg'
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    count = driver(filename)
    # cleanup
    os.remove(filename)
    resp = jsonify({'count': count}, status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)