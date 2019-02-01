#!/usr/bin/env python3

import sys
import types
import socket
import selectors
import logging


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler('server.log', encoding='utf-8')],
    datefmt='%d-%m-%Y %H:%M:%S',
    format='[%(asctime)s] [%(levelname)s]: %(message)s',
)


class ServerSocket(object):
    """A server that Handling Multiple Connections."""

    def __init__(self, host='', port=65400):
        self.HOST = host  # Symbolic name meaning all available interfaces
        self.PORT = port  # Arbitrary non-privileged port
        self.is_listening = False

        self._socket = None
        self._logger = logging.getLogger()
        self._slt = selectors.DefaultSelector()

    def listen(self):
        """Create a new socket using the given address family,
        socket type. And registers the socket to be monitored."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self.HOST, self.PORT))  # Bind the socket to address
        self._socket.listen(1)
        self._socket.setblocking(False)  # Configure the socket in non-blocking mode.
        self._slt.register(self._socket, selectors.EVENT_READ, data=None)
        self.is_listening = True
        msg = 'Server Listening on %s:%s' % (self.HOST, self.PORT)
        print(msg)
        logging.debug(msg)
        self._run_daemon()

    def close(self):
        """Close connection"""
        self._slt.close()
        self._socket.close()
        self._socket = None
        self.is_listening = False

    def set_debug(self, debug):
        """Set Debug"""
        self._logger.disabled = not debug

    def _accept_wrapper(self, sock):
        """Accept Wrapper"""
        conn, addr = sock.accept()  # Should be ready to read
        logging.debug("Accepted Connection From %s:%s" % addr)
        conn.setblocking(False)

        # We’ll use data to keep track of what’s been sent and received on the socket.
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self._slt.register(conn, events, data=data)

    def _service_connection(self, key, mask):
        """Read the data sent by the client process it and return it."""
        sock = key.fileobj  # The socket object
        data = key.data
        recv_data = None
        if mask & selectors.EVENT_READ:
            try:
                recv_data = sock.recv(1024)  # Should be ready to read
            except ConnectionResetError:
                pass
            finally:
                if recv_data:
                    data.outb = recv_data
                else:
                    # This means that the client has closed their socket, so the server should too.
                    logging.debug("Closing Connection To %s:%s" % data.addr)
                    self._slt.unregister(sock)
                    sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                response = self.echo(data.outb)
                sock.send(response)  # Should be ready to write
                data.outb = b''  # The bytes sent are then removed from the send buffer:

    @staticmethod
    def echo(data):
        """Overwrite this method to modify the data."""
        return data

    def _run_daemon(self):
        """Run Daemon"""
        try:
            while True:
                events = self._slt.select(timeout=None)  # Blocks until there are sockets ready for I/O.
                for key, mask in events:
                    if key.data is None:
                        self._accept_wrapper(key.fileobj)
                    else:
                        self._service_connection(key, mask)
        except KeyboardInterrupt:
            logging.debug("Caught keyboard interrupt, exiting")
        finally:
            self.close()


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("usage:", sys.argv[0], "<host> <port>")
        sys.exit(1)

    server = ServerSocket(sys.argv[1], int(sys.argv[2]))
    server.listen()
