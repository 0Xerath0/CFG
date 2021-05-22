#include<stdio.h>
int main ()
{
    int i, j;
    i = 10;
    if(i > 13){
        i = i + 20;
        j = i * 100 + 50;
        if(i > 40){
            j++;
        }
        else {
            i = i + 20;
        }
    }
    else{
        j = i * 200;
        int x, y;
        x = 100;
        y = x + 1;
    }
    j = j + 200;
    while(j < 500){
        j = i + j;
        int x;
        x = 100;
    }
    while(i < 200){
        i = i + 50;
        j--;
    }
    return j;
}
