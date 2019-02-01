# Python Socket Test

This project is oriented to client server through socket. Where the server accepts multiple connections processing each data sent by the client and responding back.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

```python
python setup.py install
```

### How to Test

This test creates a local server on port 55430. Then a client is created that connects to this port to send the data in the file "utils/operations.txt". The server evaluating each data sent by the client using the "evaluate" method in "utils/evaluate.py" and responds to the client. The client saves each response in a file "test/result.txt". In addition, the logs "server.log" and "client.log" are created too.

```python
python setup.py test
```

### How to Use

* First create a file "my_server.py" and add the following:

```python
from py_socket_test.core.server import ServerSocket

def custom_echo(data):
    """Modify the data sent by the client."""
    return data + b'!!!'

host = '127.0.0.1'
port = 3500  # Arbitrary non-privileged port
server = ServerSocket(host, port)
server.echo = custom_echo
server.listen()
```

Run the script and you'll see a message that says:
Server Listening on 127.0.0.1:3500

* Second Create a file "my_client.py" and add the following:

```python
from py_socket_test.core.client import ClientSocket

host = '127.0.0.1'  # The remote host
port = 3500  # The same port as used by the server
client = ClientSocket(host, port)
client.connect()
result = client.send(b'Hello World')
print(result)
client.close()
```

Run the script and the modified message will be shown:

```python
"Hello World!!!"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
