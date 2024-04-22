from typing import List

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


def findParamInArray(param_name: str, arr: List[Param]) -> Param:
    for param in arr:
        if param.name == param_name:
            return param


def findParamInArrayByRow(param: str, arr: List[Param], row: int) -> Param:
    res = next(filter(lambda p: (p.name == param and p.response_row == row), arr))
    return res


def findParamInArrayByValue(param_name: str, arr: List[Param], param_value: str):
    for param in arr:
        if param.name == param_name and param_value == param.value:
            return param


def findParamsInArray(param: str, arr: []):
    res = filter(lambda p: p.name == param, arr)
    return list(res)


def findFirstActivePdpContextInParams(wanted_params: List[Param]) -> Param:
    for param in wanted_params:
        if param.name == "<state>" and param.value == "1":
            return param
