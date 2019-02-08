def strip_split(s, *args, **kwargs):
    return list(map(lambda x: x.strip(), s.split(*args, **kwargs)))


def try_cast(tp, obj):
    try:
        tp(obj)
        return True
    except:
        return False


def get_true_value(x):
    if try_cast(int, x):
        return int(x)
    elif try_cast(float, x):
        return float(x)
    elif x.lower in ['true', 'false']:
        return bool(x)
    else:
        return x