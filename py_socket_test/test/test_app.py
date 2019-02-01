import os
import unittest
import threading

from py_socket_test.utils.evaluate import evaluate
from py_socket_test.core.server import ServerSocket
from py_socket_test.core.client import ClientSocket


class SocketConnectionTestCase(unittest.TestCase):
    """Socket Connection TestCase"""

    host = '127.0.0.1'
    port = 55430
    server = ServerSocket(host, port)
    client = ClientSocket(host, port)

    @classmethod
    def setUpClass(cls):
        cls.create_server()

    @classmethod
    def create_server(cls):
        """Create Server"""
        def echo(data):
            response = str(evaluate(data.decode())).encode()
            return response

        cls.server.echo = echo
        cls.server.set_debug(True)

        t = threading.Thread(target=cls.server.listen)
        t.daemon = True
        t.start()

    def test_server(self):
        """Test Server"""
        self.assertEqual(self.server.is_listening, True)

    def test_client(self):
        """Test Client"""
        app_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        file_name = os.path.join(app_path, 'utils', 'operations.txt')
        self.client.set_debug(True)
        self.client.connect()
        self.assertEqual(self.client.is_connected, True)
        self.client.send_file(file_name)
        self.client.close()
        self.assertEqual(self.client.is_connected, False)

    def test_evaluate(self):
        """Test Evaluate"""
        self.assertEqual(evaluate('74 - 36 - 96 + 32 + 2 + 26'), 2, 'Wrong Evaluation')
        self.assertEqual(evaluate('47 - 88 + 32 - 71 * 39 * 68'), -188301, 'Wrong Evaluation')
        self.assertEqual(evaluate('49 - 97 + 17 + 31 / 37 + 82'), 51.83783783783784, 'Wrong Evaluation')
        self.assertEqual(evaluate('59 + 59 + 3 - 28 / 41 + 84'), 204.3170731707317, 'Wrong Evaluation')
        self.assertEqual(evaluate('42 + 23 + 75 - 90'), 50, 'Wrong Evaluation')


if __name__ == '__main__':
    unittest.main()
