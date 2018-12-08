def str_join(*args):
    return ''.join(map(str, args))


def neighbours(i, j, size):
    x = range(max(0, i - 1), min(i + 2, size))
    y = range(max(0, j - 1), min(j + 2, size))

    neighbours_list = [(xc, yc) for xc in x for yc in y]
    try:
        neighbours_list.remove((i, j))
    except ValueError:
        pass

    return neighbours_list
