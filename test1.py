import logging
import time
from multiprocessing import Process, Pool
import zmq
from comms import Comms


def initBoard():
    myBoard = Comms(enableDevLogger=False)
    myBoard.startStream()
    print("[Comms] sleeping for 10 seconds")
    time.sleep(10)  # based department

    # open zmq socket
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)

    while True:
        message = socket.recv()
        print("[Comms] Received Request, sending current data chunk ")
        current_time = str(time.time())
        print(f"[Comms] Sending Current Data at {current_time}")
        cD = myBoard.getCurrentData(numSamples=450000) # NOTE: Ring Buffer must be full before sending out!

        socket.send(cD)

        print("[Comms] Message sent successfully at " + str(time.time()))


def initSignalRelay():
    port = "5556"
    context = zmq.Context()
    print("[SCR] Connecting to server with port %s" % port)
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:%s" % port)
    print("[SCR] Sending Request...")
    while True:
        socket.send_string("Are you there?")
        message = socket.recv()
        # socket.recv()
        print(f"[SCR] Received data {message}, running one cycle ")


if __name__ == "__main__":
    a = Process(target=initBoard, name='server')
    b = Process(target=initSignalRelay, name='client')
    b.start()
    a.start()
    print("Timer start")
    time.sleep(30)
    a.terminate()
    b.terminate()
