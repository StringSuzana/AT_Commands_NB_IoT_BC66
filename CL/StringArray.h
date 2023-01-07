//
// Created by Suz on 07-Jan-23.
//

#ifndef CL_STRINGARRAY_H
#define CL_STRINGARRAY_H
typedef struct{
    char ** arr;
    int size;
}StringArray;
StringArray * createNewStringArray(int size);
StringArray * createStringArray(char ** arr, int size);
void destroyStringArray(StringArray * strArr);
#endif //CL_STRINGARRAY_H
