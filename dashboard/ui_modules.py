import math
from urllib.parse import urlsplit, parse_qs, urlencode, urlunsplit

import tornado.web


def update_querystring(url, **kwargs):
    base_url = urlsplit(url)
    query_args = parse_qs(base_url.query)
    query_args.update(kwargs)
    for arg_name, arg_value in kwargs.items():
        if arg_value is None:
            if arg_name in query_args:
                del query_args[arg_name]

    query_string = urlencode(query_args, True)
    return urlunsplit((base_url.scheme, base_url.netloc,
                       base_url.path, query_string, base_url.fragment))


class Paginator(tornado.web.UIModule):
    """Pagination links display."""

    def render(self, page, page_size, results_count):
        pages = int(math.ceil(results_count / page_size)) if results_count else 0

        def get_page_url(_page):
            # don't allow ?page=1
            if _page <= 1:
                _page = None
            return update_querystring(self.request.uri, page=_page)

        _next = page + 1 if page < pages else None
        previous = page - 1 if page > 1 else None

        return self.render_string('templates/uimodules/pagination.html', page=page, pages=pages, next=_next,
                                  previous=previous, get_page_url=get_page_url)
