def tuple_to_dict(col_header, tuples):
    result = []
    for k in tuples.items:
        row_dict = dict(zip(col_header, k))
        result.append(row_dict)
    return result