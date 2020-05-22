# import pickle

from igraph import Graph

from graph_libs.utils import timing
from settings import ARTICLE_TAGS_GRAPH_FILE


@timing
def read_graph(path: str = ARTICLE_TAGS_GRAPH_FILE):
    return Graph.Read_Pickle(path)
    # with open(path, 'rb') as out_file:
    #     return pickle.load(out_file)


class ArticleTagsGraphSearch:
    def __init__(self, graph: Graph):
        self.graph = graph

    @timing
    def find_articles(self, corpus, source_item, ignored_tags=None):

        if ignored_tags is None:
            ignored_tags = []

        corpus_dict = {item['id']: item for item in corpus}
        source = self.graph.vs.find(id_eq=source_item['id'])
        targets = set(edge.target for edge in self.graph.es.select(_source_eq=source.index))

        targets_items = [corpus_dict[self.graph.vs[index]['id']] for index in targets]

        def sort_set(_target_item):
            _source = {tag for tag in source_item['tags'] if tag not in ignored_tags}
            _target = {tag for tag in _target_item['tags'] if tag not in ignored_tags}
            return len(_source & _target)

        targets_items.sort(key=sort_set, reverse=True)

        return targets_items

    @timing
    def find_articles2(self, source_item):
        source = self.graph.vs.find(id_eq=source_item['id'])

        edges = [edge for edge in source.all_edges()]

        edges.sort(key=lambda x: x['weight'], reverse=True)

        targets = []
        for edge in edges:
            vertex = edge.vertex_tuple[0] if edge.vertex_tuple[0] != source else edge.vertex_tuple[1]
            targets.append({'id': vertex['id'], 'weight': edge['weight']})

        return targets
