import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(BASE_DIR, 'corpus')
IGNORE_TAGS_FILE = os.path.join(BASE_DIR, 'artifacts/tags_ignore.txt')

TWIN_TAGS_INDEX_FILE = os.path.join(BASE_DIR, 'twin_tags_index.pickle')

ARTICLE_TAGS_GRAPH_FILE = os.path.join(BASE_DIR, 'article_graph.pickle')
