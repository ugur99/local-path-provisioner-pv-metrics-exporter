


def convert_size_string_to_bytes(size):
    unit = size[-2:]
    sz = float(size[:-2])
    if unit == 'bi':
        return sz
    elif unit == 'Ki':
        return sz * 1024**1
    elif unit == 'Mi':
        return sz * 1024**2
    elif unit == 'Gi':
        return sz * 1024**3
    elif unit == 'Ti':
        return sz * 1024**4
    elif unit == 'Pi':
        return sz * 1024**5
    elif unit == 'Ei':
        return sz * 1024**6
    else:
        exit(1)