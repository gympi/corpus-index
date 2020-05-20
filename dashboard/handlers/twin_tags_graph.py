import random

from graph_libs.twin_tags_graph import TwinTagsGraphSearch
from .base import BaseHandler


class TwinTagsGraphHandler(BaseHandler):
    def initialize(self, corpus, index):
        self.corpus = corpus
        self.index = index

    def get(self, idx=None):
        try:
            searched_article = self.corpus[int(idx)]
        except:
            searched_article = random.choice(self.corpus)

        twt_graph_search = TwinTagsGraphSearch(self.index)

        found_articles = twt_graph_search.search2(self.corpus, searched_article)

        self.on_write_page('twin_tags_graph.html', {
            'searched_article': searched_article,
            'found_articles': found_articles
        })
