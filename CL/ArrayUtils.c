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
    return NOT_FOUND;
}

Param find_param_in_array(const char* param, Param arr[], size_t arr_len)
{
    for (size_t i = 0; i < arr_len; i++)
    {
        if (strcmp(arr[i].name, param) == 0)
        {
            return arr[i];
        }
    }
    // Return an empty Param if not found
    const Param result = {
            .name = "",
            .value = "",
            .response_row = 0
    };
    return result;
}
