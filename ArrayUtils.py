from AtResponse import Param


def findIndex(arr, element):
    try:
        return arr.index(element)
    except ValueError:
        return -1


def findParamInArray(self, param: str, arr: []) -> Param:
    res = next(filter(lambda p: p.name == param, arr))
    return res
