import zmq
import time
from multiprocessing import Process


def server():
    port="5556"
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    print("Running server on port: ", port)
    # serves only 5 request and dies
    for reqnum in range(5):
        # Wait for next request from client
        message = socket.recv()
        print("Received request #%s: %s" % (reqnum, message))
        socket.send_string("World from %s" % port)


def client():
    port="5556"
    context = zmq.Context()
    print("Connecting to server with port %s" % port)
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:%s" % port)
    for request in range(20):
        print("Sending request ", request, "...")
        socket.send_string("Hello")
        message = socket.recv()
        print("Received reply ", request, "[", message, "]")
        time.sleep(1)


if __name__ == "__main__":
    a = Process(target=server, name = 'server')
    b = Process(target=client, name='client')
    a.start()
    b.start()
    time.sleep(5)
    a.terminate()
    b.terminate()
