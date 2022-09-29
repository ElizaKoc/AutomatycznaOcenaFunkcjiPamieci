def sort(dict_list):
    dict_list = sorted(dict_list, key=lambda x: x['start'])
    return dict_list


def find_max_idx(dict_list):
    indices = []
    for idx, x in enumerate(dict_list):
        indices.append(x[1])

    max_idx = max(indices)
    return max_idx
