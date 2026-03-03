#!/usr/bin/env python3
from __future__ import print_function
import sys
import time
import random
import base64
import grpc

import lab6_pb2
import lab6_pb2_grpc


def doAdd(stub, debug=False):
    resp = stub.Add(lab6_pb2.AddMsg(a=5, b=10))
    if debug:
        print({"sum": resp.sum})


def doRawImage(stub, debug=False):
    img = open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb").read()
    resp = stub.RawImage(lab6_pb2.RawImageMsg(img=img))
    if debug:
        print({"width": resp.width, "height": resp.height})


def doDotProduct(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    resp = stub.DotProduct(lab6_pb2.DotProductMsg(a=a, b=b))
    if debug:
        print({"dotproduct": resp.dotproduct})


def doJsonImage(stub, debug=False):
    img_bytes = open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb").read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    resp = stub.JsonImage(lab6_pb2.JsonImageMsg(img=img_b64))
    if debug:
        print({"width": resp.width, "height": resp.height})


if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print("where <cmd> is one of add, rawImage, dotProduct, jsonImage")
    sys.exit(1)

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

addr = f"{host}:50051"
print(f"Running {reps} reps against {addr}")

channel = grpc.insecure_channel(addr)
stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

if cmd == "add":
    start = time.perf_counter()
    for _ in range(reps):
        doAdd(stub)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")
elif cmd == "rawImage":
    start = time.perf_counter()
    for _ in range(reps):
        doRawImage(stub)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")
elif cmd == "dotProduct":
    start = time.perf_counter()
    for _ in range(reps):
        doDotProduct(stub)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")
elif cmd == "jsonImage":
    start = time.perf_counter()
    for _ in range(reps):
        doJsonImage(stub)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)
    sys.exit(1)

