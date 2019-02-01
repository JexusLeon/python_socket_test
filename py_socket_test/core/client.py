#!/usr/bin/env python3

import sys
import socket
import logging

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler('client.log', encoding='utf-8')],
    datefmt='%d-%m-%Y %H:%M:%S',
    format='[%(asctime)s] [%(levelname)s]: %(message)s',
)


class ClientSocket(object):
    """Client Socket"""

    def __init__(self, host, port):
        self.HOST = host  # The remote host
        self.PORT = port  # The same port as used by the server
        self.is_connected = False

        self._file = None
        self._socket = None
        self._logger = logging.getLogger()

    def connect(self):
        """Connect to the server"""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._socket.connect((self.HOST, self.PORT))
        except ConnectionRefusedError as e:
            logging.error(e)
        else:
            self.is_connected = True

    def close(self):
        """Close connection"""
        self._socket.close()
        self._socket = None
        self.is_connected = False

    def send(self, str_bytes):
        """Send """
        result = b''
        try:
            self._socket.send(str_bytes)
            result = self._socket.recv(1024)
        except ConnectionResetError as e:
            logging.debug(e)
        return result

    def set_debug(self, debug):
        """Set Debug"""
        self._logger.disabled = not debug

    def send_file(self, send_file, result_file='result.txt'):
        """Send the data of a file to the server and save the response in a file."""
        with open(send_file, 'rb') as s_file:
            with open(result_file, 'wb') as r_file:
                for line in s_file:
                    line = line.strip()
                    result = self.send(line)
                    if result is not None:
                        logging.debug('%s %s' % (line, result))
                        r_file.write(result + b'\n')


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("usage:", sys.argv[0], "<host> <port> <send_file>")
        sys.exit(1)

    client = ClientSocket(sys.argv[1], int(sys.argv[2]))
    client.connect()
    if client.is_connected:
        client.send_file(sys.argv[3])
        client.close()
