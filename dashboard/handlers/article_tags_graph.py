import random

from graph_libs.article_tags_graph import ArticleTagsGraphSearch
from dashboard.handlers.base import BaseHandler


class ArticleTagsGraphHandler(BaseHandler):
    def initialize(self, corpus, graph, ignored_tags):
        self.corpus = corpus
        self.graph = graph
        self.ignored_tags = ignored_tags

    def get(self, idx=None):
        try:
            searched_article = self.corpus[int(idx)]
        except:
            searched_article = random.choice(self.corpus)

        searcher = ArticleTagsGraphSearch(self.graph)

        target_articles = searcher.find_articles2(searched_article)

        found_articles = []
        for found_article in target_articles[:10]:
            _source = {tag for tag in searched_article['tags'] if tag not in self.ignored_tags}
            _target = {tag for tag in self.corpus[found_article['id']]['tags'] if tag not in self.ignored_tags}

            found_articles.append({'find_tags': list(_source & _target), **self.corpus[found_article['id']]})

        self.on_write_page('article_tags_graph.html', {
            'searched_article': searched_article,
            'found_articles': found_articles,
            'count_founds': len(target_articles)
        })
