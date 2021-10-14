from multiprocessing import Process, Pool
import zmq
from comms import Comms


if __name__ == "__main__":

    #Create my board
    myBoard = Comms()

    myBoard.startStream()