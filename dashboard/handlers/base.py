import os

import tornado

from settings import BASE_DIR


class BaseHandler(tornado.web.RequestHandler):
    def on_write_page(self, template: str, params: dict = None, templates_path: str = None, ):
        if templates_path is None:
            templates_path = 'dashboard/templates'

        if params is None:
            params = dict()

        # loader = tornado.template.Loader(templates_path)
        self.render(os.path.join(BASE_DIR, templates_path, template), **params)


class PaginationHandlerMixin:
    _pagination = None

    @property
    def pagination(self):
        if self._pagination is None:
            self._pagination = Pagination(request=self)

        return self._pagination


class Pagination:
    _page_name = 'page'
    _page = 1
    _page_size = 10

    def __init__(self, *args, request=None, url=None, default_kwargs=None, **kwargs):
        if default_kwargs is None:
            default_kwargs = dict()

        if request is not None:
            self._prepared_tornado_request(request, default_kwargs)
        elif url is not None:
            pass
        else:
            raise

    @property
    def limit(self):
        return self.page_size

    @property
    def offset(self):
        return (self._page - 1) * self.page_size

    def _prepared_url(self, url):
        """Detail parameters remark.

           **url**: current request url
           **page_name**: arg name for page, default is `page`
           **page**: current page
        """
        from urllib.parse import urlsplit, parse_qs
        url_kwargs = parse_qs(urlsplit(url).query)

        self.page_name = url_kwargs.get('page_name', self._page_name)
        self.page = url_kwargs.get(self.page_name, self._page)

        self.page_size = url_kwargs.get('page_size', self._page_size)

    def _prepared_tornado_request(self, handler, default_kwargs):
        self.page_name = handler.get_argument('page_name', self._page_name)

        try:
            self.page = abs(int(handler.get_argument(self.page_name, self._page)))

            if self.page == 0:
                raise
        except:
            self.page = self._page

        try:
            self.page_size = abs(int(handler.get_argument('page_size', self._page_size)))

            if self.page == 0:
                raise
        except:
            self.page_size = self._page_size