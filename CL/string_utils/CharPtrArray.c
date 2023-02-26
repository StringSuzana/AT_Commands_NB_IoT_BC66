#include "CharPtrArray.h"
#include "../array_utils/AtResponseArray.h"
#include <stdlib.h>
#include <string.h>


CharPtrArray * createNewCharPtrArray(int size) {
    CharPtrArray * strArr = malloc(sizeof(CharPtrArray));
    strArr->arr = malloc(sizeof(char*) * size);
    strArr->size = size;
    return strArr;
}
CharPtrArray * createCharPtrArray(char ** arr, int size) {
    CharPtrArray * strArr = malloc(sizeof(CharPtrArray));
    strArr->arr = arr;
    strArr->size = size;
    return strArr;
}
void destroyCharPtrArray(CharPtrArray * charPtrArray) {
    for (int i = 0; i < charPtrArray->size; i++) {
        free(charPtrArray->arr[i]);
    }
    free(charPtrArray->arr);
    free(charPtrArray);
}

CharPtrArray *getResponseRowFrom_charArray(char *arr[], int row)
{
    char delim[] = ":";
    char str[MAX_RESPONSE_ROW_SIZE * MAX_RESPONSE_LINES];
    strcpy(str, arr[row]);

    char *str_token = strtok(str, delim);

    char **response_array = calloc(0, sizeof(char *));
    int i = 0;
    while (str_token != NULL)
    {
        response_array = realloc(response_array, i + 1 * sizeof(char *));
        response_array[i] = calloc(MAX_RESPONSE_ROW_SIZE, sizeof(char *));
        response_array[i] = strdup(str_token);
        str_token = strtok(NULL, delim);
        i++;
    }
    CharPtrArray *stringArray = createCharPtrArray(response_array, i);
    return stringArray;
}