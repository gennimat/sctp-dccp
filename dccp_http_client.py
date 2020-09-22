import http.client
import socket
import argparse


socket.DCCP_SOCKOPT_PACKET_SIZE = 1
socket.DCCP_SOCKOPT_SERVICE = 2
socket.SOCK_DCCP = 6
socket.IPROTO_DCCP = 33
socket.SOL_DCCP = 269
packet_size = 512


class DccpHttpConnection(http.client.HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DCCP, socket.IPROTO_DCCP)
        self.sock.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_PACKET_SIZE, packet_size)
        self.sock.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_SERVICE, True)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.connect((self.host, self.port))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DCCP http test client.')
    parser.add_argument('host', help='the host to connect to (default 127.0.0.1)')

    args = parser.parse_args()

    conn = DccpHttpConnection(args.host + ':8000')
    conn.request("HEAD", "/")
    res = conn.getresponse()

    print(res.status, res.reason)
