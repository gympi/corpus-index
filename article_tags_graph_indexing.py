import pickle
import igraph
import itertools

from igraph import Graph

from graph_libs.corpus import read_corpus, read_ignore_tags
from graph_libs.utils import timing
from settings import ARTICLE_TAGS_GRAPH_FILE


@timing
def create_graph():
    ignored_tags = read_ignore_tags()

    corpus = list(read_corpus())
    corpus_dict = {item['id']: item for item in corpus}

    # Create graph
    g: Graph = igraph.Graph(directed=False)

    # Add 5 vertices
    g.add_vertices(len(corpus))

    # Add ids and labels to vertices
    for idx, item in enumerate(corpus):
        g.vs[idx]["id"] = item['id']

    all_tags = list(set(tag for item in corpus for tag in item['tags'] if tag not in ignored_tags))

    tags_corpus_index = {tag: set() for tag in all_tags}

    for idx, item in enumerate(corpus):
        for tag in item['tags']:
            tag in tags_corpus_index and tags_corpus_index[tag].add(item['id'])

    combinations = set()

    tags_corpus_index = {k: v for k, v in tags_corpus_index.items() if len(v) > 1}

    for items_idx in tags_corpus_index.values():
        sources = g.vs.select(id_in=items_idx)
        combinations.update(itertools.combinations([source.index for source in sources], 2))

    g.add_edges(combinations)
    print(g.vcount())
    print(g.ecount())
    print(g.es[g.ecount()-1])
    return g


@timing
def create_graph2():
    ignored_tags = read_ignore_tags()

    corpus = list(read_corpus())
    corpus_dict = {item['id']: item for item in corpus}

    # Соберем все возможные теги
    all_tags = list(set(tag for item in corpus for tag in item['tags'] if tag not in ignored_tags))

    # Индекс {тег} => [статья, ...]
    tags_corpus_index = {tag: set() for tag in all_tags}
    for idx, item in enumerate(corpus):
        for tag in item['tags']:
            tag in tags_corpus_index and tags_corpus_index[tag].add(item['id'])

    # Удалим теги с всего одной статьей
    tags_corpus_index = {k: v for k, v in tags_corpus_index.items() if len(v) > 1}

    combinations = dict()

    for items_idx in tags_corpus_index.values():
        for _combination in [tuple(sorted(i)) for i in itertools.combinations(items_idx, 2)]:
            if _combination in combinations:
                combinations[_combination] += 1
            else:
                combinations[_combination] = 1

    a = [(*k, v) for k, v in combinations.items()]
    # Create graph
    g: Graph = igraph.Graph.TupleList(a, vertex_name_attr='id', directed=False, weights=True)
    print(g.vcount())
    print(g.ecount())

    # es = g.es.find(weight_gt=2)
    # print([tag for tag in corpus_dict[g.vs[es.source]['id']]['tags'] if tag not in ignored_tags])
    # print([tag for tag in corpus_dict[g.vs[es.target]['id']]['tags'] if tag not in ignored_tags])
    # # print(g.es.find(weight_gt=2))
    return g


@timing
def save_graph_index(graph: Graph):
    graph.write_pickle(fname='article_tags_graph.pickle')
    # with open('article_graph.pickle', 'wb') as in_file:
    #     pickle.dump(graph, in_file)


if __name__ == '__main__':
    save_graph_index(create_graph2())
