from socketserver import BaseServer
import http.server
import socket
import sctp


class SctpServer(BaseServer):
    request_queue_size = 5

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        BaseServer.__init__(self, server_address, RequestHandlerClass)
        self.socket = sctp.sctpsocket_tcp(socket.AF_INET)

        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def server_activate(self):
        self.socket.listen(self.request_queue_size)

    def server_close(self):
        self.socket.close()

    def fileno(self):
        return self.socket.fileno()

    def get_request(self):
        return self.socket.accept()

    def shutdown_request(self, request):
        try:
            request.shutdown(socket.SHUT_WR)
        except OSError:
            self.close_request(request)

    def close_request(self, request):
        request.close()


if __name__ == "__main__":
    Handler = http.server.SimpleHTTPRequestHandler

    with SctpServer(("", 8000), Handler) as httpd:
        print("serving at port", 8000)
        httpd.serve_forever()
