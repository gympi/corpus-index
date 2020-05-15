import itertools
import pickle
from typing import Set

from corpus import read_corpus

IGNORE_TAGS_FILE = "./artifacts/tags_ignore.txt"


def get_ignore_tags() -> Set[str]:
    try:
        with open(IGNORE_TAGS_FILE, "r") as out_file:
            return set(i.lower().strip() for i in out_file.readlines())
    except:
        # TODO: handle the error
        return set()


def indexing(
        del_nodes_count=1,
        ignored_tags=None
):
    if not ignored_tags:
        ignored_tags = get_ignore_tags()

    # Build all tags list
    all_tags = [tag for item in read_corpus() for tag in item['tags'] if tag not in ignored_tags]

    # Build index tags
    # indexing_tags = tuple(set(all_tags))
    # all_tags = [indexing_tags.index(tag) for tag in all_tags]

    # counting words occurrences
    nodes_dict_all = {i: all_tags.count(i) for i in set(all_tags)}

    # filtering by occurrences count
    nodes_dict = {k: v for k, v in nodes_dict_all.items() if v > del_nodes_count}

    formatted_tags = {(tag1, tag2): [0, []] for tag1, tag2 in itertools.combinations(set(nodes_dict.keys()), 2)}
    print(len(formatted_tags))

    # count tags connection
    for item in read_corpus():
        for tag1, tag2 in itertools.combinations(item['tags'], 2):

            if (tag1, tag2) in formatted_tags.keys():
                formatted_tags[(tag1, tag2)][0] += 1
                formatted_tags[(tag1, tag2)][1].append(item['id'])

    # filtering pairs with zero count
    for k, v in formatted_tags.copy().items():
        if v[0] < 2:
            del formatted_tags[k]

    with open('index.pickle', 'wb') as in_file:
        pickle.dump(formatted_tags, in_file)


if __name__ == '__main__':
    indexing()
