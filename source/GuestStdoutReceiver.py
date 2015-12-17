import threading
import socket

class GuestStdoutReceiver:
    _stop = False
    _ip = None
    _port = None
    _socket = None
    _thread = None

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._thread = threading.Thread(target=self.entryPoint)
        self._thread.daemon = True # thread dies at least when main thread exits
        self._thread.start()

    def entryPoint(self):
        # print("GuestStdOutReceiver::entryPoint()")
        self._socket.bind((self._ip, self._port))
        self._socket.listen(1)
        try:
            while (self._stop is not True):
                # print("GuestStdOutReceiver waiting for a client...")
                (clientSocket, clientAddress) = self._socket.accept()
                # print("GuestStdOutReceiver client connected!")
                print("Guest compilation log:\n")
                stopRecv = False
                while (self._stop is not True and stopRecv is not True):
                    data = clientSocket.recv(2048)
                    if (len(data) > 0):
                        print(data.decode("utf-8"))
                    else:
                        stopRecv = True
        except OSError:
            a = 42 # do nothing

    def stop(self):
        self._stop = True
        self._socket.shutdown(0)
        self._socket.close()
        self._thread.join() # exchange them
        self._socket = None # try to
