#include<stdio.h>
int main ()
{
    int i, j;
    i = 10;
    if(i > 13){
        if(i > 15){
            i--;
            j = i + 10;
        } else {
            i = i * 2;
            j = 100;
        }
        i = i + 20;
        j = j * 100 + 50;
    }
    else{
        i = i - 20;
        j = i * 200;
    }
    j = j + 200;
    while(j < 500){
        j = i + j;
        i++;
    }
    return j;
}
