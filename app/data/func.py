# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Module of functions."""

from operator import itemgetter
from itertools import groupby


def stime_to_decimal(s):
    """Lololo."""
    return s.hour + s.minute / 60


def group_time(records):
    """Lololo."""
    records.sort(key=itemgetter(6, 1))
    result = [
        [stime_to_decimal(time), *[item[0] for item in group]]
        for time, group in groupby(records, key=itemgetter(6))
    ]
    return result


def group_sensor(records):
    """Lololo."""
    records.sort(key=itemgetter(1))
    result = ['X', *[key[1] for key, _ in groupby(
        records, key=itemgetter(1, 2))]]
    return result


def group_category(records):
    """Lololo."""
    records.sort(key=itemgetter(3))
    result = [{
        'id': key[0],
        'name': key[1],
        'measure': key[2],
        'data': [*[item for item in group]],
    } for key, group in groupby(records, key=itemgetter(3, 4, 5))]

    for item in result:
        item['rows'] = group_time(item['data'])
        item['cols'] = group_sensor(item['data'])
        item.pop('data')

    return result

# [
#   {
#     "cols": [
#       "X", 
#       "Sens 1", 
#       "Sens 2"
#     ], 
#     "id": 1, 
#     "measure": "AAA", 
#     "name": "Cat 1", 
#     "rows": [
#       [
#         10.916666666666666, 
#         17.0, 
#         14.0
#       ]
#     ]
#   }, 
#   {
#     "cols": [
#       "X", 
#       "Sens 3"
#     ], 
#     "id": 2, 
#     "measure": "AAA", 
#     "name": "Cat 2", 
#     "rows": [
#       [
#         10.916666666666666, 
#         13.0
#       ]
#     ]
#   }
# ]