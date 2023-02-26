#ifndef STRING_ARRAY_H
#define STRING_ARRAY_H

#include "AtString.h"

#define MAX_STRING_ARRAY_ELEMENTS 10
#define ELEMENT_NOT_FOUND -1
typedef struct
{
    String values[MAX_STRING_ARRAY_ELEMENTS];
    int size;
} StringArray;
StringArray getResponseRowFrom_stringArray(StringArray array, int row);
int findIndexIn_StringArray(StringArray array, const char *element);
#endif //STRING_ARRAY_H
