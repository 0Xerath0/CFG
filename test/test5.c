#include<stdio.h>
int main ()
{
    int i, j;
    i = 20;
    if(i > 0){
        i = i + 10;
        j = i * 10;
        if(i > 15){
            i--;
            j = i + 10;
        }
    }
    else{
        int x;
        x = j + 10;
        i = i - 20;
        if(j > 100){
            j = j - 50;
            i++;
        }
        else{
            int y;
            x = i + 10;
        }
    }
    j = j + 200;
    while(j < 500){
        j = i + j;
        i++;
    }
    return j;
}
