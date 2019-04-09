# -*- coding: utf-8 -*-


def make_dict(keys, kwargs):
    result = dict()
    for key in kwargs.keys():
        if key in keys:
            result.update({key: kwargs[key]})
    return result


if __name__ == '__main__':

    def test_make_dict(keys, **kwargs):
        return make_dict(keys=keys, kwargs=kwargs)

    keys = ['a', 'c']
    print(test_make_dict(keys=keys, a=1, b=2, c=3, d=4))
