#include<stdio.h>
#include<unistd.h>
#define N 3

int main() {
    for (int i=0;i<N;i++) {
        fork();
        printf("Hello from process %d\n", getpid());
        fork();
    }
    
    return 0;
}

