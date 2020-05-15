import tornado
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_unix_socket
from tornado.options import options, define

from dashboard.server import make_app

define('listen_address', group='webserver', default='127.0.0.1', help='Listen address')
define('listen_port', group='webserver', default=8095, help='Listen port')
define('unix_socket', group='webserver', default='/tmp/tags-graph.socket', help='Path to unix socket to bind')

if __name__ == "__main__":
    app = make_app()

    if options.unix_socket:
        server = HTTPServer(app)
        socket = bind_unix_socket(options.unix_socket)
        server.add_socket(socket)
    else:
        app.listen(options.listen_port, address=options.listen_address)

    tornado.ioloop.IOLoop.instance().start()
