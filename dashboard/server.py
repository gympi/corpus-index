#!/usr/bin/env python
import itertools
import pickle
import random
from os import listdir
from os.path import isfile, join
from typing import Generator

import tornado.ioloop
import tornado.web
import tornado.httpserver


CORPUS_DIR = './corpus'


def read_corpus() -> Generator[dict, None, None]:
    files = [f for f in listdir(CORPUS_DIR) if isfile(join(CORPUS_DIR, f))]

    for _file in files:
        with open(join(CORPUS_DIR, _file), 'rb') as out_file:
            for out in pickle.load(out_file):
                yield out


def search(corpus, tags_index, searched_item):
    result = list()
    for tag1, tag2 in itertools.combinations(searched_item['tags'], 2):
        if (tag1, tag2) in tags_index.keys():
            for item_id in tags_index[(tag1, tag2)][1]:
                result.append({'id': item_id, 'find_tags': (tag1, tag2)})

    found_result = []
    for item in result:
        found_result.append({'find_tags': item['find_tags'], **corpus[item['id']]})

    return {v['id']: v for v in found_result if v['id'] != searched_item['id']}.values()


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, corpus, tags_index):
        self.corpus = corpus
        self.tags_index = tags_index

    def get(self, idx=None):
        try:
            searched_article = self.corpus[int(idx)]
        except:
            searched_article = random.choice(self.corpus)

        found_articles = search(self.corpus, self.tags_index, searched_article)

        self.on_write_page('index.html', {
            'searched_article': searched_article,
            'found_articles': found_articles
        })

    def on_write_page(self, template: str, params: dict = None, templates_path: str = None, ):
        if templates_path is None:
            templates_path = './dashboard'

        if params is None:
            params = dict()

        loader = tornado.template.Loader(templates_path)
        self.write(loader.load(template).generate(**params))


def read_tags_index():
    with open('./index.pickle', 'rb') as out_file:
        return pickle.load(out_file)


def make_app():
    return tornado.web.Application([
        (r"/(\d+)?", IndexHandler, dict(corpus={item['id']: item for item in read_corpus()}, tags_index=read_tags_index())),
    ])
