import itertools
import pickle

from graph_libs.utils import timing
from settings import TWIN_TAGS_INDEX_FILE


@timing
def read_twin_tags_index(path: str = TWIN_TAGS_INDEX_FILE):
    with open(path, 'rb') as out_file:
        return pickle.load(out_file)


class TwinTagsGraphSearch:
    def __init__(self, index):
        self.__index = index

    @timing
    def search(self, tags):
        result = set()
        for tag1, tag2 in itertools.combinations(tags, 2):
            if (tag1, tag2) in self.__corpus_tags_index.keys():

                for item_id in self.__corpus_tags_index[(tag1, tag2)][1]:
                    result.add(item_id)

        return tuple(map(lambda index: self.__corpus_tags_index[index], result))

    @timing
    def search2(self, corpus, searched_item):
        result = list()
        for tag1, tag2 in itertools.combinations(searched_item['tags'], 2):
            if (tag1, tag2) in self.__index.keys():
                for item_id in self.__index[(tag1, tag2)][1]:
                    result.append({'id': item_id, 'find_tags': (tag1, tag2)})

        found_result = []
        for item in result:
            found_result.append({'find_tags': item['find_tags'], **corpus[item['id']]})

        return {v['id']: v for v in found_result if v['id'] != searched_item['id']}.values()
