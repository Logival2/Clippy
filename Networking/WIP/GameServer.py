#!/usr/bin/env python3
import trio
from itertools import count

PORT = 8080
COUNTER = count()


class DebugTracer(trio.abc.Instrument):
    def before_run(self):
        print("!!! run started")

    def _print_with_task(self, msg, task):
        # repr(task) is perhaps more useful than task.name in general,
        # but in context of a tutorial the extra noise is unhelpful.
        print("{}: {}".format(msg, task.name))

    def task_spawned(self, task):
        self._print_with_task("### new task spawned", task)

    def task_scheduled(self, task):
        self._print_with_task("### task scheduled", task)

    def before_task_step(self, task):
        self._print_with_task(">>> about to run one step of task", task)

    def after_task_step(self, task):
        self._print_with_task("<<< task step finished", task)

    def task_exited(self, task):
        self._print_with_task("### task exited", task)

    def before_io_wait(self, timeout):
        if timeout:
            print("### waiting for I/O for up to {} seconds".format(timeout))
        else:
            print("### doing a quick check for I/O")
        self._sleep_time = trio.current_time()

    def after_io_wait(self, timeout):
        duration = trio.current_time() - self._sleep_time
        print("### finished I/O check (took {} seconds)".format(duration))

    def after_run(self):
        print("!!! run finished")


async def echo_server(stream):
    id = next(COUNTER)
    print(f"server n°{id} started")
    try:
        async for data in stream:
            print(f"server n°{id} received '{data!r}'")
            await stream.send_all(data)
        print(f"server n°{id} closed connection")
    except Exception as e:
        print(f"server n°{id} crashed: {e!r}")


class Server(object):
    """docstring for Server."""

    def __init__(self, addr, port):
        super(Server, self).__init__()
        self.bind_addr = addr
        self.port = port

    def run(self):
        trio.run(trio.serve_tcp, echo_server, PORT)
