import asyncio
from asyncio import Future

import grpc
from grpc._cython import cygrpc
from grpc._channel import _handle_event, _EMPTY_FLAGS

import types


class AsyncStream:
    def __init__(self, stream, loop=None):
        self.stream = stream
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

    def handle_event(self, event, future):
        """
        Event handler called by grpc when a message is received
        (or any other event)
        """
        with self.stream._state.condition:
            callbacks = _handle_event(event, self.stream._state,
                                      self.stream._response_deserializer)
            self.stream._state.condition.notify_all()
            done = not self.stream._state.due
            self.loop.call_soon_threadsafe(
                self._process_future, future)  # this is the key patch point
        for callback in callbacks:
            callback()
        return self._stream._call if done else None

    def _process_future(self, future):
        print("_process_future")
        if self.stream._state.response is not None:
            response = self.stream._state.response
            self.stream._state.response = None
            print("set result on", future)
            future.set_result(response)
        elif cygrpc.OperationType.receive_message not in self.stream._state.due:
            if self.stream._state.code is grpc.StatusCode.OK:
                future.set_exception(StopIteration())
            elif self.stream._state.code is not None:
                future.set_exception(self)
        print("_process_future finished")

    # Similar to first part of grpc._channel._Rendevous._next
    def _next(self):
        """
        Returns a future for the next value in an iterator
        """
        # ensure there is only one outstanding request at any given time, or segfault happens
        if cygrpc.OperationType.receive_message in self.stream._state.due:
            raise ValueError("Prior future was not resolved")

        future = Future()
        print("Starting with future", future)
        # this method is the same as the first part of _Rendevous._next
        with self.stream._state.condition:
            if self.stream._state.code is None:
                event_handler = lambda event: self.handle_event(event, future)
                self.stream._call.start_client_batch(
                    (cygrpc.ReceiveMessageOperation(_EMPTY_FLAGS), ),
                    event_handler)
                self.stream._state.due.add(
                    cygrpc.OperationType.receive_message)
            elif self.stream._state.code is grpc.StatusCode.OK:
                future.set_exception(StopAsyncIteration())
            else:
                future.set_exception(self)
        print("Returning future", future)
        return future

    def __aiter__(self):
        return self

    async def __anext__(self):
        print("__anext__ awaiting")
        value = await self._next()
        print("__anext__ returning")
        return value


def patch_iterator(it, ioloop=None):
    '''Changes gRPC stream iterator to return futures instead of blocking'''

    if ioloop is None:
        ioloop = asyncio.get_event_loop()

    # mostly identical to grpc._channel._event_handler
    def _tornado_event_handler(state, call, response_deserializer, fut):
        def handle_event(event):
            print("Handle event", event)
            with state.condition:
                callbacks = _handle_event(event, state, response_deserializer)
                state.condition.notify_all()
                done = not state.due
                _process_future(state, fut)  # this is the key patch point
            for callback in callbacks:
                callback()
            return call if done else None

        return handle_event

    # mostly identical to last part of grpc._channel._Rendevous._next
    def _process_future(state, fut):
        if state.response is not None:
            response = state.response
            state.response = None
            fut.set_result(response)
        elif cygrpc.OperationType.receive_message not in state.due:
            if state.code is grpc.StatusCode.OK:
                fut.set_exception(StopIteration())
            elif state.code is not None:
                fut.set_exception(self)

    # mostly identical to first part of grpc._channel._Rendevous._next
    def _next(self):
        print('_next')
        # ensure there is only one outstanding request at any given time, or segfault happens
        if cygrpc.OperationType.receive_message in self._state.due:
            raise ValueError("Prior future was not resolved")

        # this method is the same as the first part of _Rendevous._next
        with self._state.condition:
            if self._state.code is None:
                fut = Future()
                event_handler = _tornado_event_handler(
                    self._state, self._call, self._response_deserializer, fut)
                self._call.start_client_batch(
                    (cygrpc.ReceiveMessageOperation(_EMPTY_FLAGS), ),
                    event_handler)
                self._state.due.add(cygrpc.OperationType.receive_message)
                return fut
            elif self._state.code is grpc.StatusCode.OK:
                raise StopIteration()
            else:
                raise self

    # patch the iterator
    it._next = types.MethodType(_next, it)
