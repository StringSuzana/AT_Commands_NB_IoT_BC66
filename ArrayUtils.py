def findIndex(arr, element):
    try:
        return arr.index(element)
    except ValueError:
        return -1
