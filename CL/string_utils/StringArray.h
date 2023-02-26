#ifndef STRING_ARRAY_H
#define STRING_ARRAY_H

#include "AtString.h"
#include "../constants.h"


typedef struct
{
    String values[MAX_STRING_ARRAY_ELEMENTS];
    int size;
} StringArray;
StringArray getResponseRowFrom_stringArray(StringArray array, int row);
int findIndexIn_StringArray(StringArray array, const char *element);
#endif //STRING_ARRAY_H
