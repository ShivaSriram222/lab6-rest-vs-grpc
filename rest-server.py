#!/usr/bin/env python3

##
## Sample Flask REST server implementing methods for Lab6
##
from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import base64
import io
import logging

# Initialize the Flask application
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)
        response = {'width': img.size[0], 'height': img.size[1]}
    except Exception as e:
        response = {'error': str(e), 'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    try:
        data = request.get_json(force=True)
        a = data.get("a", [])
        b = data.get("b", [])

        if len(a) != len(b):
            response = {"error": "Vectors must be same length", "dotproduct": 0.0}
            response_pickled = jsonpickle.encode(response)
            return Response(response=response_pickled, status=400, mimetype="application/json")

        dp = 0.0
        for i in range(len(a)):
            dp += float(a[i]) * float(b[i])

        response = {"dotproduct": dp}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")

    except Exception as e:
        response = {"error": str(e), "dotproduct": 0.0}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=400, mimetype="application/json")

@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    try:
        data = request.get_json(force=True)
        img_b64 = data.get("image", "")

        img_bytes = base64.b64decode(img_b64)
        ioBuffer = io.BytesIO(img_bytes)
        img = Image.open(ioBuffer)

        response = {"width": img.size[0], "height": img.size[1]}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")

    except Exception as e:
        response = {"error": str(e), "width": 0, "height": 0}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=400, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=5000)
