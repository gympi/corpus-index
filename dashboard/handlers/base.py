import tornado


class BaseHandler(tornado.web.RequestHandler):
    def on_write_page(self, template: str, params: dict = None, templates_path: str = None, ):
        if templates_path is None:
            templates_path = './dashboard/templates'

        if params is None:
            params = dict()

        loader = tornado.template.Loader(templates_path)
        self.write(loader.load(template).generate(**params))
