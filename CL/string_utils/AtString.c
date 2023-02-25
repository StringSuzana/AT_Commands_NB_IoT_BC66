
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

