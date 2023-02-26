
#include <string.h>
#include <stdbool.h>
#include "AtString.h"

void removeCarriageReturn(char *str)
{
    int i, j;
    for (i = 0, j = 0; str[i] != '\0'; i++)
    {
        if (str[i] != '\r')
        {
            str[j++] = str[i];
        }
    }
    str[j] = '\0';
}

void removeCarriageReturnFromString(String *str)
{
    int i, j;
    for (i = 0, j = 0; str->text[i] != '\0'; i++)
    {
        if (str->text[i] != '\r')
        {
            str->text[j++] = str->text[i];
        }
    }
    str->text[j] = '\0';
}



// function to split a values into an array of strings based on newline characters
int splitString(char *str, char **arr, int max_arr_size)
{
    int arr_size = 0;
    char *token = strtok(str, "\n");
    while (token != NULL && arr_size < max_arr_size)
    {
        arr[arr_size++] = token;
        token = strtok(NULL, "\n");
    }
    return arr_size;
}

// function to remove a values from an array of strings at a given index
void removeString(char **arr, int index, int arr_size)
{
    for (int i = index; i < arr_size - 1; i++)
    {
        arr[i] = arr[i + 1];
    }
    arr[arr_size - 1] = NULL;
}
// function to check if a values starts with another values
bool startsWith(char *str, char *prefix)
{
    return strncmp(str, prefix, strlen(prefix)) == 0;
}
