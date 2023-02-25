#include "CharPtrArray.h"
#include <stdlib.h>


CharPtrArray * createNewStringArray(int size) {
    CharPtrArray * strArr = malloc(sizeof(CharPtrArray));
    strArr->arr = malloc(sizeof(char*) * size);
    strArr->size = size;
    return strArr;
}
CharPtrArray * createStringArray(char ** arr, int size) {
    CharPtrArray * strArr = malloc(sizeof(CharPtrArray));
    strArr->arr = arr;
    strArr->size = size;
    return strArr;
}
void destroyStringArray(CharPtrArray * charPtrArray) {
    for (int i = 0; i < charPtrArray->size; i++) {
        free(charPtrArray->arr[i]);
    }
    free(charPtrArray->arr);
    free(charPtrArray);
}