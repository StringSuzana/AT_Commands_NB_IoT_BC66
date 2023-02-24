#include "ArrayUtils.h"

int find_index(const char* arr[], const char* element, const size_t arr_len)
{
    for (size_t i = 0; i < arr_len; i++)
    {
        if (strcmp(arr[i], element) == 0)
        {
            return i;
        }
    }
    return ELEMENT_NOT_FOUND;
}

