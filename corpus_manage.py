#!/usr/bin/env python
import inspect
import sys
import traceback
from typing import Generator
import os
import argparse
from dateutil.relativedelta import relativedelta
import datetime

import pickle

# BEGIN Connection of the library with restrictions on the right to use
from graph_libs.corpus import read_corpus, clear_corpus
from settings import CORPUS_DIR

try:
    sys.path.append('../../tvzvezda/libs/')
    from tvzvezdaru_corpus_entity import ObjectsIndexStorage, ObjectIndexSerializer
except Exception as e:
    print("Error trying to read file: \n{}: ".format(inspect.currentframe().f_code.co_name), e)
    traceback.print_exc()
# END


START_DATE = datetime.date(2020, 3, 1)
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


class ObjectIndexSerializerExtend(ObjectIndexSerializer):
    def tags(self):
        # Convert tags to lower case
        return [tag.lower() for tag in super().tags()]


def build_corpus():
    """
    Build data corpus and saves it in files broken down by date
    """
    clear_corpus()

    objects_index_storage = ObjectsIndexStorage()

    index_start = 0

    for date in get_month_range(START_DATE, END_DATE):
        result = objects_index_storage.get_objects(date, date + relativedelta(months=1))

        if not os.path.exists(CORPUS_DIR):
            os.mkdir(CORPUS_DIR)

        # Serialize all list entities
        serialized_result = [
            {'id': idx, **ObjectIndexSerializerExtend(item).marshal()} for idx, item in enumerate(result, index_start)
        ]

        index_start += len(serialized_result)+1
        # Save result to a pickle format
        with open(os.path.join(CORPUS_DIR, f'{date.strftime("%Y-%m-%d")}.pickle'), 'wb') as in_file:
            pickle.dump(serialized_result, in_file)


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
