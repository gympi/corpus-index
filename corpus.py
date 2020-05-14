#!/usr/bin/env python

import sys
from typing import IO, Generator
import json
import os
import argparse
from dateutil.relativedelta import relativedelta
import datetime
from os import listdir
from os.path import isfile, join


import pickle

# BEGIN Connection of the library with restrictions on the right to use
sys.path.append('../../tvzvezda/libs/')
try:
    from tvzvezdaru_corpus_entity import ObjectsIndexStorage, ObjectIndexSerializer
except:
    pass
# END


CORPUS_DIR = './corpus'

START_DATE = datetime.date(2020, 1, 1)
END_DATE = datetime.date.today()


def get_month_range(start_date: datetime.date, end_date: datetime.date) -> Generator[datetime.date, None, None]:
    """
    Build month range
        Generator['2020-01-01', '2020-02-01', '2020-03-01', ..., end_date]
    """
    end = end_date
    current = start_date

    while current <= end:
        yield current
        current += relativedelta(months=1)


def clear_corpus():
    """
    Remove all files in corpus dir
    """
    if os.path.exists(CORPUS_DIR):
        for f in [f for f in os.listdir(CORPUS_DIR)]:
            os.remove(os.path.join(CORPUS_DIR, f))


class ObjectIndexSerializerExtend(ObjectIndexSerializer):
    def tags(self):
        # Convert tags to lower case
        return [tag.lower() for tag in super().tags()]


def build_corpus():
    clear_corpus()

    objects_index_storage = ObjectsIndexStorage()

    for date in get_month_range(START_DATE, END_DATE):
        result = objects_index_storage.get_objects(date, date + relativedelta(months=1))

        if not os.path.exists(CORPUS_DIR):
            os.mkdir(CORPUS_DIR)

        # Serialize all list entities
        serialized_result = [ObjectIndexSerializerExtend(item).marshal() for item in result]

        # Save result to a pickle format
        with open(os.path.join(CORPUS_DIR, f'{date.strftime("%Y-%m-%d")}.pickle'), 'wb') as in_file:
            pickle.dump(serialized_result, in_file)


def read_large_file(file_object: IO) -> Generator[str, None, None]:
    """
    Uses a generator to read a large file lazily
    """
    while True:
        data = file_object.readline()
        if not data:
            break
        yield data


def read_corpus() -> Generator[dict, None, None]:
    files = [f for f in listdir(CORPUS_DIR) if isfile(join(CORPUS_DIR, f))]

    for _file in files:
        with open(join(CORPUS_DIR, _file), 'rb') as out_file:
            for out in pickle.load(out_file):
                yield out


def print_corpus(template: str):
    [print(template.format(**out)) for out in read_corpus()]


def main():
    class Actions:
        BUILD = 'build'
        READ = 'read'
        CLEAR = 'clear'

        @classmethod
        def actions(cls):
            return cls.BUILD, cls.READ, cls.CLEAR

    parser = argparse.ArgumentParser()
    parser.add_argument("action",
                        choices=Actions.actions(),
                        help="build - build corpus. read - read corpus; clear - clear corpus",
                        type=str)

    default_template = "Date create: {date_create}\nTitle: {title}\nAnons: {anons}\nTags: {tags}\n"

    parser.add_argument(
        '--read-out-template',
        default=default_template,
        help="Default template: {}".format(default_template.replace('\n', '\\n')))

    args = parser.parse_args()

    if args.action == Actions.BUILD:
        build_corpus()
    elif args.action == Actions.READ:
        print_corpus(args.read_out_template)
    elif args.action == Actions.CLEAR:
        clear_corpus()


if __name__ == '__main__':
    main()
