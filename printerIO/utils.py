from itertools import chain


def flatten_list(list_to_flatten):
    return list(chain.from_iterable(list_to_flatten))