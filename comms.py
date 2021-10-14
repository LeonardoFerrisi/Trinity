import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels


class Comms:
    """
    A class for communicating with an EEG capable board compatible with brainflow
    """

    def __init__(self, boardID: int = -1, serial: str = '', enableDevLogger: bool = False):
        """
        Runs when a Comms object is created
        :param boardID: By default, -1 for synthetic. Specifies the board we are using
        :param serial: The serial port being used, if applicable
        :param enableDevLogger: True if we want a logger, False if no
        """
        self.isAlive = False
        self.myBoardID = boardID  # By default, -1 ID is used for synthetic board
        if enableDevLogger:
            BoardShim.enable_dev_board_logger()
            self.logger = True
        else:
            self.logger = False
        self.params = BrainFlowInputParams()
        self.params.serial_port = serial

        # Create the internal BoardShim Object
        self.board = BoardShim(self.myBoardID, self.params)
        self.prepped = False

    def prepBoard(self):
        """
        Prepares a streaming session
        """
        self.board.prepare_session()
        self.prepped = True

    def releaseBoard(self):
        """
        Releases the board from a streaming session
        """
        self.board.release_session()
        self.prepped = False

    def startStream(self, numSamples: int = 450000, streamerParams: str = '', prep: bool = True):
        """
        Prepares a streaming session and then starts a stream of data
        :param numSamples: The amount of samples to cycle through in stream
        :param streamerParams: By default '', can change aspects of stream
        :param prep: True if we want to prepare the board with this method
        """

        if prep:
            self.prepBoard()
            self.prepped = True

        # Main code, only if session has been prepared
        if self.prepped:

            self.board.start_stream(numSamples, streamerParams)  # Start streaming data from board

            self.isAlive = True

            if self.logger:
                self.board.log_message(LogLevels.LEVEL_INFO, "Start sleeping in the main thread")

        else:
            print("[Trinity] Streaming Session was never prepared")

    def startOutStream(self):
        pass

    def stopStream(self, release: bool = True):
        """
        Stops the board from streaming
        and releases the streaming session
        if desired
        :param release: True if we want to release the session
        """

        if self.isAlive:
            if self.logger:
                print("[Trinity] Stopping Stream")
            self.board.stop_stream()
            if release:
                self.releaseBoard()
            self.isAlive = False

    def getData(self):
        """
        Gets the data from the board since the stream was started
        :return: The data from the board
        """
        return self.board.get_board_data()

    def getCurrentData(self, numSamples: int):
        """
        Gets the current board data in the form of
        an NDArray containing numSamples samples
        :param numSamples: The amount of samples our current data holds
        :return: The current board data
        """
        return self.board.get_current_board_data(numSamples)

    def getSamplingRate(self):
        """
        Gets the rate at which the board samples data per second (i.e: Muse samples at 256Hz)
        :return: The sampling rate of a specific board
        """
        return self.board.get_sampling_rate(self.myBoardID)

    def getEEGChannels(self):
        """
        Gets the EEG channels from the board being used
        :return: The amt of channels for streaming EEG on the board
        """
        return self.board.get_eeg_channels(self.myBoardID)

    def getEXGChannels(self):
        """
        Gets the EXG Channels from the board being used
        :return: The amt of total biosignal channels our board has
        """
        return self.board.get_exg_channels(self.myBoardID)

    def getBoardInfo(self, returnID: bool = True):
        """
        Lets us know what board we are using
        :return: The id of the board being used
        """
        if self.myBoardID == -1:
            print("Default Board is being used: SYNTHETIC")
        elif self.myBoardID == 0:
            print("OpenBCI Cyton is being used: CYTON")
        elif self.myBoardID == 22:
            print("Interaxon Muse 2 is being used: MUSE2")
        if returnID:
            return self.myBoardID


if __name__ == "__main__":
    myBoard = Comms(enableDevLogger=True)
    myBoard.startStream(outStream=True)
    time.sleep(10)
    myBoard.stopStream()
