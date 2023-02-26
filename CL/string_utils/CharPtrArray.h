#ifndef CHAR_PTR_ARRAY_H
#define CHAR_PTR_ARRAY_H

typedef struct
{
    char **arr;
    int size;
} CharPtrArray;

CharPtrArray *createNewCharPtrArray(int size);

CharPtrArray *createCharPtrArray(char **arr, int size);

void destroyCharPtrArray(CharPtrArray *charPtrArray);

CharPtrArray *getResponseRowFrom_charArray(char *arr[], int row);

#endif //CHAR_PTR_ARRAY_H
