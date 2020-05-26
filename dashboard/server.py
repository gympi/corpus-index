from urllib.parse import urlunsplit, urlsplit, parse_qs

import tornado.ioloop
import tornado.web
import tornado.httpserver

from . import ui_modules
from .handlers.article_tags_graph import ArticleTagsGraphHandler
from .handlers.base import BaseHandler
from .handlers.twin_tags_graph import TwinTagsGraphHandler
from graph_libs.article_tags_graph import read_graph
from graph_libs.corpus import read_corpus, read_ignore_tags
from graph_libs.twin_tags_graph import read_twin_tags_index

corpus = {item['id']: item for item in read_corpus()}
twin_tags_index = read_twin_tags_index()

settings = {
    "ui_modules": ui_modules,
}


class IndexRedirectHandler(BaseHandler):
    def get(self):
        base_url = urlsplit(self.request.full_url())
        location = urlunsplit((base_url.scheme, base_url.netloc, '/article-tags-graph/', '', ''))
        self.set_header('X-VF-Staging-Redirect', location)
        self.redirect(location)


def make_app():
    return tornado.web.Application([
        (r"/", IndexRedirectHandler),
        (r"/twin-tags-graph/(\d+)?", TwinTagsGraphHandler,
         dict(corpus=corpus, index=twin_tags_index)),

        (r"/article-tags-graph/(\d+)?", ArticleTagsGraphHandler,
         dict(corpus=corpus, graph=read_graph(), ignored_tags=read_ignore_tags())),
    ], **settings)
