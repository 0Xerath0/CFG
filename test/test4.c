#include<stdio.h>
int main ()
{
    int i, j;
    i = 10;
    j = 3;
    while(j < 500){
        j = i + j;
        j = j + 10;
        i = i - j;
    }
    if(i > 13){
        i = i + 20;
        j = i * 100 + 50;
    }
    else{
        j = i * 200;
        int x, y;
        x = 1;
    }
    j = j + 200;
    return j;
}
