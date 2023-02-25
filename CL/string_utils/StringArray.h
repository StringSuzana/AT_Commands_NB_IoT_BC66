#ifndef STRING_ARRAY_H
#define STRING_ARRAY_H

#include "AtString.h"

#define MAX_STRING_ARRAY_ELEMENTS 10

typedef struct
{
    String values[MAX_STRING_ARRAY_ELEMENTS];
    int array_size;
} StringArray;
#endif //STRING_ARRAY_H
