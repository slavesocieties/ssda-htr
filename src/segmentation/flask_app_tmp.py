from flask import Flask, request, json
import requests
import os
import threading
import uuid
import time
from driver import driver
app = Flask(__name__)

worker_status = dict()

@app.route('/segmentation', methods = ['POST'])
def segmentatation_post():
    global worker_status
    data = request.json
    id = uuid.uuid1()
    thread = threading.Thread(target=thread_worker_segmentation, args=(data,id))
    thread.start()
    worker_status[id] = {
        'status': 'started',
        'message': 'Segmentation started, please use the /segmentation GET endpoint and the provided uuid to check the status.',
        'count': 0,
        'uuid': id
    }
    resp = app.response_class(
        response=json.dumps(worker_status[id]),
        status=200,
        mimetype='application/json'
    )
    return resp

@app.route('/segmentation', methods = ['GET'])
def segmentatation_get():
    global worker_status
    data = request.json
    if 'uuid' not in data or data['uuid'] not in worker_status:
        resp = app.response_class(
            response=json.dumps({
                'status': 'error',
                'message': 'uuid not found'
            }),
            status=200,
            mimetype='application/json'
        )
    else:
        resp = app.response_class(
            response=json.dumps(worker_status[data['uuid']]),
            status=200,
            mimetype='application/json'
        )
    return resp

def thread_worker_segmentation(data, id):
    global worker_status
    try:
        vol = data["vol"]
        img = data["img"]
        str_im = '0' * (4 - len(str(img))) + str(img)
        obj_key = str(vol) + '-' + str(str_im) + '.jpg'
        url = 'https://zoqdygikb2.execute-api.us-east-1.amazonaws.com/v1/ssda-production-jpgs/' + obj_key
        response = requests.get(url)
        filename = obj_key
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
        count = driver(filename[:-4])
        worker_status[id] = {
            'status': 'completed',
            'message': 'Segmentation successfully completed, please check AWS S3 to confirm.',
            'count': count
        }
        # cleanup
        os.remove(filename)
    except Exception as e:
        worker_status[id] = {
            'status': 'error',
            'message': f'{e.__repr__()}',
            'count': 0
        }
    return

def thread_resource_cleanup():
    global worker_status
    while True:
        worker_status = dict()
        # cleanup every 24 hours
        time.sleep(86400)


if __name__ == "__main__":
    thread = threading.Thread(target=thread_resource_cleanup, args=())
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug = True)