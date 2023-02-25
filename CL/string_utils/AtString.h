#ifndef AT_STRING_H
#define AT_STRING_H

typedef struct
{
    char *text;
    int length;
} String;
void removeCarriageReturn(char *str);
void removeCarriageReturnFromString(String *str);
#endif //AT_STRING_H
