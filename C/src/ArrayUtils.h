#ifndef ARRAY_UTILS_H
#define ARRAY_UTILS_H

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "Param.h"

#define NOT_FOUND -1

int findIndex(const char *arr[], const char *element, size_t arr_len);
Param findParamInArray(const char *param, const Param *arr, size_t arr_len);
#endif
