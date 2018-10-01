"""Lololo."""

from operator import itemgetter
from itertools import groupby
import json


mylist = [
    [
        30.0,
        "C",
        "Third",
        "0003",
        "First sensor",
        "Температура"
    ],
    [
        25.0,
        "C",
        "First",
        "0001",
        "First sensor",
        "Температура"
    ],
    [
        21.0,
        "Вт",
        "Second",
        "0002",
        "Second sensor",
        "Энергопотребление"
    ]
]


def group_category(records):
    """Lololo."""
    records.sort(key=itemgetter(5, 2))
    result = {
        key: [*group] for key, group in groupby(records, key=itemgetter(5))
    }

    return result


print(json.dumps(group_category(mylist), indent=2, ensure_ascii=False))
