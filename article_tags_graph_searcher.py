import random

from graph_libs.article_tags_graph import ArticleTagsGraphSearch, read_graph
from graph_libs.corpus import read_corpus, read_ignore_tags


if __name__ == '__main__':
    ignored_tags = read_ignore_tags()

    corpus = list(read_corpus())
    corpus_dict = {item['id']: item for item in corpus}

    item = random.choice(corpus)

    graph_search = ArticleTagsGraphSearch(read_graph())

    print(item['title'])
    print([tag for tag in item['tags'] if tag not in ignored_tags])
    target_items = graph_search.find_articles2(item)

    for target_item in target_items[:5]:
        item = corpus_dict[target_item['id']]
        print(item['id'])
        print(item['title'])
        print([tag for tag in item['tags'] if tag not in ignored_tags])
