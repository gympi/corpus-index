import itertools
import pickle
import random

from terminaltables import AsciiTable

from corpus import read_corpus


class Corpus:
    def __init__(self):
        self.__corpus = None
        self.__corpus_tags_index = None

    @property
    def corpus(self):
        if self.__corpus is None:
            self.__corpus = list(read_corpus())

        return self.__corpus

    @property
    def corpus_tags_index(self):
        if self.__corpus_tags_index is None:
            with open('analysis.pickle', 'rb') as out_file:
                self.__corpus_tags_index = pickle.load(out_file)

        return self.__corpus_tags_index

    def search(self, tags):
        result = set()
        for tag1, tag2 in itertools.combinations(tags, 2):
            if (tag1, tag2) in self.corpus_tags_index.keys():

                for item_id in self.corpus_tags_index[(tag1, tag2)][1]:
                    result.add(item_id)

        return tuple(map(lambda index: self.corpus[index], result))


def print_ascii_table_result(search, found):
    template = "{date_create}\n{title}\n{tags}\n"
    view_data = [
        ('Found',),
    ] + [(template.format(**_found),) for _found in found]

    ascii_table = AsciiTable(view_data)
    print('\nSearch:')
    print(template.format(**search))
    print(ascii_table.table)


def main():
    corpus = Corpus()

    for _ in range(5):
        item = random.choice(corpus.corpus)

        found = corpus.search(item['tags'])

        print_ascii_table_result(item, found)


if __name__ == '__main__':
    main()
