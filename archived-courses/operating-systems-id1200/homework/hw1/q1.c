#include<stdio.h>
#include<unistd.h>
#define N 3

int main() {
    for (int i=0;i<N;i++) {
        fork();
        fork();
    }
    
    return 0;
}
