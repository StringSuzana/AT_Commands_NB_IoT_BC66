#include "ArrayUtils.h"

int find_index(const char *array[], const char *element, const size_t arr_len)
{
    for (size_t i = 0; i < arr_len; i++)
    {
        if (strcmp(array[i], element) == 0)
        {
            return i;
        }
    }
    return ELEMENT_NOT_FOUND;
}

/*
 * This does not work :)
int size_of_array(char *arr[])
{
    int num_elements = sizeof(arr)/sizeof(char*);
    return num_elements;
}
*/

