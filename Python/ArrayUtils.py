from AtResponse import Param
import re


def findIndex(arr, element):
    try:
        return arr.index(element)
    except ValueError:
        return -1


def containsStatus(status: str, array: []):
    pattern = rf'\b{re.escape(status)}\b'
    return any(re.search(pattern, item, re.IGNORECASE) for item in array)


def findParamInArray(param: str, arr: []) -> Param:
    res = next(filter(lambda p: p.name == param, arr))
    return res


def findParamInArrayByRow(param: str, arr: [Param], row: int) -> Param:
    res = next(filter(lambda p: (p.name == param and p.response_row == row), arr))
    return res


def findParamInArrayByValue(param: str, arr: [Param], param_value: str):
    res = next(filter(lambda p: (p.name == param and p.value == param_value), arr))
    return res


def findParamsInArray(param: str, arr: []):
    res = filter(lambda p: p.name == param, arr)
    return list(res)


def findFirstActivePdpContextInParams(wanted_params: [Param]) -> Param:
    for param in wanted_params:
        if param.name == "<state>" and param.value == "1":
            return param
