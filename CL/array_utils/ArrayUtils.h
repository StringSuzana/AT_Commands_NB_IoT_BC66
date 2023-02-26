#ifndef ARRAY_UTILS_H
#define ARRAY_UTILS_H

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "../at_responses/Param.h"

#define ELEMENT_NOT_FOUND (-1)
/*This does not work as well #define ARRAY_SIZE(array) (sizeof(array)/sizeof(array[0]))*/
int find_index(const char* arr[], const char* element, size_t arr_len);
Param find_param_in_array(const char* param, Param arr[], size_t arr_len);
#endif
