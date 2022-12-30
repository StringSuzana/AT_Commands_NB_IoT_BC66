#include "ArrayUtils.h"

int findIndex(const char *arr[], const char *element, size_t arr_len)
{
    for (size_t i = 0; i < arr_len; i++)
    {
        if (strcmp(arr[i], element) == 0)
        {
            return i;
        }
    }
    return NOT_FOUND;
}

Param findParamInArray(const char *param, const Param *arr, size_t arr_len)
{
    for (size_t i = 0; i < arr_len; i++)
    {
        if (strcmp(arr[i].name, param) == 0)
        {
            return arr[i];
        }
    }
    // Return an empty Param if not found
    Param result = {.name = "",
                    .value = "",
                    .response_row = 0};
    return result;
}
