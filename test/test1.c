#include <stdio.h>

int main ()
{
    int i;
    int j;
    int k;

    i = 5;
    j = 6;
    k = 12;

    if (i > 13)
    {
        int x,y;
        j = 10;
        k = 0;
    }
    else
    {
        j = 11;
        k = -10;
    }
    while (k < 5)
    {
        k = i + j;
        i++;
    }

    return j;
}
