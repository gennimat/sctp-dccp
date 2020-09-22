import http.client
import sctp
import socket
import argparse


class SctpHttpConnection(http.client.HTTPConnection):
    def connect(self):
        self.sock = sctp.sctpsocket_tcp(socket.AF_INET)
        self.sock.connect((self.host, self.port))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SCTP http test client.')
    parser.add_argument('host', help='the host to connect to (default 127.0.0.1)')

    args = parser.parse_args()

    conn = SctpHttpConnection(args.host + ':8000')
    conn.request("HEAD", "/")
    res = conn.getresponse()

    print(res.status, res.reason)
