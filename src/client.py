import asyncio
from argparse import ArgumentParser
from datetime import datetime

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


def simple_sleep(stub, args):
    req = pbss.SleepTask(name='single', sleepSeconds=2.0)
    resp = stub.Sleep(req)
    print(resp.id, resp.message)


class FutureWrapper:
    # Inspired by https://github.com/grpc/grpc/issues/6046#issuecomment-319547191
    def __init__(self, func):
        self.func = func

    def _fwrap(self, future, grpc_future):
        try:
            future.set_result(grpc_future.result())
        except Exception as e:
            future.set_exception(e)

    def __call__(self, req, loop=None):
        grpc_future = self.func.future(req)
        future = asyncio.Future()
        loop = asyncio.get_event_loop() if loop is None else loop
        grpc_future.add_done_callback(
            lambda _: loop.call_soon_threadsafe(self._fwrap, future, grpc_future)
        )
        return future


async def sleep_task(stub, n):
    req = pbss.SleepTask(name='multi', sleepSeconds=n)
    Sleep = FutureWrapper(stub.Sleep)
    resp = await Sleep(req)
    # await asyncio.sleep(n)
    print(resp.id, resp.message)


def loop_run(task):
    s = datetime.now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    loop.close()
    e = datetime.now()

    print("Finished after", e - s)


def multi_sleep(stub, args):
    tasks = [sleep_task(stub, n) for n in args.times]
    gathered = asyncio.gather(*tasks)
    loop_run(gathered)


def stream_sleep(stub, args):
    s = datetime.now()
    req = pbss.SleepTasks(
        name='stream', sleepSeconds=args.time, count=args.count)
    stream = stub.SleepStream(req)
    print(dir(stream))
    stream.add_callback(lambda: print("callback"))
    stream.add_done_callback(lambda x: print("callback:", x))
    import pudb
    pu.db
    for resp in stream:
        print(resp.id, resp.message)

    e = datetime.now()
    print("Finished after", e - s)


def async_stream_sleep(stub, args):
    s = datetime.now()
    req = pbss.SleepTasks(
        name='stream', sleepSeconds=args.time, count=args.count)
    streamer = AsyncStreamer(stub.SleepStream)
    stream = streamer(req)
    print(dir(stream))
    #stream.add_callback(lambda: print("callback"))
    #stream.add_done_callback(lambda x: print("callback:", x))

    for resp in stream:
        print(resp.result())

    e = datetime.now()
    print("Finished after", e - s)


async def consume(stream):
    print("consume")
    async for resp in stream:
        print("consume in for")
        print(resp.id, resp.message)


def async_stream_sleep(stub, args):
    s = datetime.now()
    req = pbss.SleepTasks(
        name='stream', sleepSeconds=args.time, count=args.count)
    streamer = AsyncStreamer(stub.SleepStream)
    stream = streamer(req)

    loop_run(consume(stream))

    e = datetime.now()
    print("Finished after", e - s)


class AsyncStreamer:
    def __init__(self, func):
        self.func = func

    def __call__(self, req):
        stream = self.func(req)
        from ipatch import AsyncStream
        return AsyncStream(stream)

        # from ipatch import patch_iterator
        # patch_iterator(iter)

        #for fut in iter:
        #    try:
        #        thing = yield fut
        #    except StopIteration:
        #        break


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
    run()