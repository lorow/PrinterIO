from itertools import chain


def flatten_list(list_to_flatten):
    return list(chain.from_iterable(list_to_flatten))


def validate_build_volume(build_volume):

    if not build_volume:
        return False

    axis = build_volume.split('x')

    if len(axis) > 3 or len(axis) < 3:
        return False

    try:
        for dimension in axis:
            int(dimension)
    except ValueError:
        return False

    return True
