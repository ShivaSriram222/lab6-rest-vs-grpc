#!/usr/bin/env python3
from concurrent import futures
import grpc
import time
import base64
import io
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6Service(lab6_pb2_grpc.Lab6ServiceServicer):
    def Add(self, request, context):
        return lab6_pb2.AddReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        try:
            io_buf = io.BytesIO(request.img)
            img = Image.open(io_buf)
            return lab6_pb2.ImageReply(width=img.size[0], height=img.size[1])
        except Exception:
            return lab6_pb2.ImageReply(width=0, height=0)

    def DotProduct(self, request, context):
        # request.a and request.b are repeated floats
        if len(request.a) != len(request.b):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Vectors must be same length")
            return lab6_pb2.DotProductReply(dotproduct=0.0)

        dp = 0.0
        for i in range(len(request.a)):
            dp += float(request.a[i]) * float(request.b[i])

        return lab6_pb2.DotProductReply(dotproduct=dp)

    def JsonImage(self, request, context):
        try:
            img_bytes = base64.b64decode(request.img)
            io_buf = io.BytesIO(img_bytes)
            img = Image.open(io_buf)
            return lab6_pb2.ImageReply(width=img.size[0], height=img.size[1])
        except Exception:
            return lab6_pb2.ImageReply(width=0, height=0)


def serve(port: int = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(Lab6Service(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC server running on 0.0.0.0:{port}")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
