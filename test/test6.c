#include<stdio.h>
int main ()
{
    int i, j;
    i = 20;
    while(i > 10){
        i = i - 2;
        j = 10;
    }
    if(i > 0){
        i = i + 10;
        j = i * 10;
    }
    else {
        int x;
        x = j + 10;
        i = i - 20;
        if(j > 100){
            j = j - 50;
            i++;
            if(j > 80){
                i = j;
            }
            else {
                j = j - 30;
            }
        }
        else{
            int y;
            x = i + 10;
        }
    }
    j = j + 200;
    return j;
}
