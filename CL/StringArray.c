//
// Created by Suz on 07-Jan-23.
//

#include "StringArray.h"
#include <stdlib.h>


StringArray * createNewStringArray(int size) {
    StringArray * strArr = malloc(sizeof(StringArray));
    strArr->arr = malloc(sizeof(char*) * size);
    strArr->size = size;
    return strArr;
}
StringArray * createStringArray(char ** arr, int size) {
    StringArray * strArr = malloc(sizeof(StringArray));
    strArr->arr = arr;
    strArr->size = size;
    return strArr;
}
void destroyStringArray(StringArray * strArr) {
    for (int i = 0; i < strArr->size; i++) {
        free(strArr->arr[i]);
    }
    free(strArr->arr);
    free(strArr);
}