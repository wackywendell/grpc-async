import time
from concurrent import futures

import pb.sleepservice_pb2_grpc as pbss

import grpc


class SleepServer(pbss.SleepTaskerServicer):
    def Sleep(self, request, context):
        time.sleep(request.sleepSeconds)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pbss.add_SleepTaskerServicer_to_server(SleepServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()