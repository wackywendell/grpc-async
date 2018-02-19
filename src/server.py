import time
from concurrent import futures

import pb.sleepservice_pb2 as pbss
import pb.sleepservice_pb2_grpc as pbssg

import grpc


class SleepServer(pbssg.SleepTaskerServicer):
    def __init__(self):
        self.last_id = 0

    def Sleep(self, request, context):
        time.sleep(request.sleepSeconds)
        id, self.last_id = self.last_id, self.last_id + 1
        message = f'response to {request.name}({request.sleepSeconds})'
        resp = pbss.SleepResponse(message=message, id=id)
        return resp

    def SleepStream(self, request, context):
        for n in range(request.count):
            time.sleep(request.sleepSeconds)
            id, self.last_id = self.last_id, self.last_id + 1
            message = f'response to {request.name}({request.sleepSeconds}, {request.count})'
            resp = pbss.SleepResponse(message=message, id=id)
            print("Responding:", resp)
            yield resp


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pbssg.add_SleepTaskerServicer_to_server(SleepServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()