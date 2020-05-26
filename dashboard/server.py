import tornado.ioloop
import tornado.web
import tornado.httpserver

from dashboard import ui_modules
from dashboard.handlers.article_tags_graph import ArticleTagsGraphHandler
from dashboard.handlers.twin_tags_graph import TwinTagsGraphHandler
from graph_libs.article_tags_graph import read_graph
from graph_libs.corpus import read_corpus, read_ignore_tags
from graph_libs.twin_tags_graph import read_twin_tags_index

corpus = {item['id']: item for item in read_corpus()}
twin_tags_index = read_twin_tags_index()

settings = {
    "ui_modules": ui_modules,
}


def make_app():
    return tornado.web.Application([
        (r"/", TwinTagsGraphHandler,
         dict(corpus=corpus, index=twin_tags_index)),
        (r"/twin-tags-graph/(\d+)?", TwinTagsGraphHandler,
         dict(corpus=corpus, index=twin_tags_index)),

        (r"/article-tags-graph/(\d+)?", ArticleTagsGraphHandler,
         dict(corpus=corpus, graph=read_graph(), ignored_tags=read_ignore_tags())),
    ], **settings)
