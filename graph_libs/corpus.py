import inspect
import os
import pickle
import traceback
from os import listdir
from os.path import isfile, join
from typing import Generator, Set, IO

from settings import CORPUS_DIR, IGNORE_TAGS_FILE


def read_corpus(corpus_path: str = CORPUS_DIR) -> Generator[dict, None, None]:
    files = [f for f in listdir(corpus_path) if isfile(join(corpus_path, f))]

    for _file in files:
        with open(join(corpus_path, _file), 'rb') as out_file:
            for out in pickle.load(out_file):
                yield out


def clear_corpus(corpus_path: str = CORPUS_DIR):
    """
    Remove all files in corpus dir
    """
    if os.path.exists(CORPUS_DIR):
        for f in [f for f in os.listdir(corpus_path)]:
            os.remove(os.path.join(corpus_path, f))


def read_large_file(file_object: IO) -> Generator[str, None, None]:
    """
    Uses a generator to read a large file lazily
    """
    while True:
        data = file_object.readline()
        if not data:
            break
        yield data


def read_ignore_tags(ignore_tags_file: str = IGNORE_TAGS_FILE, default: set = None) -> Set[str]:
    try:
        with open(ignore_tags_file, "r") as out_file:
            return set(i.lower().strip() for i in out_file.readlines())
    except Exception as e:
        print("Error trying to read file: \n{}: ".format(inspect.currentframe().f_code.co_name), e)
        traceback.print_exc()
        return set if default is None else default
