import tornado

from dashboard.server import make_app

if __name__ == "__main__":
    app = make_app()
    app.listen(8095)
    tornado.ioloop.IOLoop.current().start()
