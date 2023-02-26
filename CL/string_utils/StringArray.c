#include <string.h>
#include "StringArray.h"


StringArray getResponseRowFrom_stringArray(StringArray array, int row)
{
    StringArray response_row;
    response_row.size = 0;

    if (row >= 0 && row < array.size) {
        String str = array.values[row];

        // Replace ':' with ','
        char *colon_pos = strchr(str.text, ':');
        while (colon_pos != NULL) {
            *colon_pos = ',';
            colon_pos = strchr(colon_pos, ':');
        }

        // Split the string into substrings separated by commas
        char *substr = strtok(str.text, ",");
        while (substr != NULL) {
            String value = { .text = substr, .length = strlen(substr) };
            response_row.values[response_row.size++] = value;
            substr = strtok(NULL, ",");
        }
    }

    return response_row;
}
int findIndexIn_StringArray(StringArray array, const char *element)
{
    for (size_t i = 0; i < array.size; i++)
    {
        if (strcmp(array.values[i].text, element) == 0)
        {
            return i;
        }
    }
    return ELEMENT_NOT_FOUND;
}
