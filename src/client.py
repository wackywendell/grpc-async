import asyncio
from argparse import ArgumentParser
from contextlib import contextmanager
from datetime import datetime
import sys

from ipatch import FutureWrapper, AsyncStream

import pb.sleepservice_pb2 as pbss
import pb.sleepservice_pb2_grpc as pbssg

import grpc

parser = ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser')

single_parser = subparsers.add_parser('single')
single_parser.add_argument(
    '-t', '--time', default=1.0, type=float, help="time to sleep (seconds)")

multi_parser = subparsers.add_parser('multi')
multi_parser.add_argument(
    'times', nargs='+', type=float, help="time to sleep (seconds)")

multi_parser = subparsers.add_parser('stream')
multi_parser.add_argument(
    '-t', '--time', default=1.0, type=float, help="time to sleep (seconds)")
multi_parser.add_argument('-n', '--count', default=3, type=int, help="Count")

multi_parser = subparsers.add_parser('astream')
multi_parser.add_argument(
    '-t', '--time', default=1.0, type=float, help="time to sleep (seconds)")
multi_parser.add_argument('-n', '--count', default=3, type=int, help="Count")


@contextmanager
def time_printer():
    s = datetime.now()
    yield
    e = datetime.now()
    print("Finished after", e - s)


def simple_sleep(stub, args):
    with time_printer():
        req = pbss.SleepTask(name='single', sleepSeconds=2.0)
        resp = stub.Sleep(req)
        print(resp.id, resp.message)


async def sleep_task(stub, n):
    req = pbss.SleepTask(name='multi', sleepSeconds=n)
    Sleep = FutureWrapper(stub.Sleep)
    resp = await Sleep(req)
    # await asyncio.sleep(n)
    print(resp.id, resp.message)


def async_run(task):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    loop.close()


def multi_sleep(stub, args):
    with time_printer():
        tasks = [sleep_task(stub, n) for n in args.times]
        gathered = asyncio.gather(*tasks)
        async_run(gathered)


def stream_sleep(stub, args):
    with time_printer():
        req = pbss.SleepTasks(
            name='stream', sleepSeconds=args.time, count=args.count)
        stream = stub.SleepStream(req)

        for resp in stream:
            print(resp.id, resp.message)


async def consume(stream):
    async for resp in stream:
        print(resp.id, resp.message)


def async_stream_sleep(stub, args):
    with time_printer():
        streamer = AsyncStreamer(stub.SleepStream)
        reqs = [
            pbss.SleepTasks(
                name='stream-%s' % c, sleepSeconds=args.time, count=args.count)
            for c in 'ABC'
        ]
        streams = [consume(streamer(r)) for r in reqs]
        task = asyncio.gather(*streams)
        async_run(task)


class AsyncStreamer:
    def __init__(self, func):
        self.func = func

    def __call__(self, req):
        stream = self.func(req)
        return AsyncStream(stream)


def run():
    args = parser.parse_args()

    channel = grpc.insecure_channel('localhost:50051')
    stub = pbssg.SleepTaskerStub(channel)
    if args.subparser == 'single':
        simple_sleep(stub, args)
    elif args.subparser == 'multi':
        multi_sleep(stub, args)
    elif args.subparser == 'stream':
        stream_sleep(stub, args)
    elif args.subparser == 'astream':
        async_stream_sleep(stub, args)
    else:
        raise NotImplemented()


if __name__ == '__main__':
    try:
        run()
    except grpc.RpcError as e:
        print("GRPC RpcError {code}: {desc}".format(
            code=e.code(), desc=e.details()))
    except KeyboardInterrupt:
        print("Interrupted.")
        sys.exit(1)