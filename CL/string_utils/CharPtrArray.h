//
// Created by Suz on 07-Jan-23.
//

#ifndef CL_CHARPTRARRAY_H
#define CL_CHARPTRARRAY_H

typedef struct{
    char ** arr;
    int size;
}CharPtrArray;
CharPtrArray * createNewStringArray(int size);
CharPtrArray * createStringArray(char ** arr, int size);
void destroyStringArray(CharPtrArray * charPtrArray);
#endif //CL_CHARPTRARRAY_H
