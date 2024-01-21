#include <stdio.h>
#include <stdlib.h>
__attribute__((noinline))
int fibonacci(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

int main(int argc, char *argv[]) {
    int n, i;

    n = atoi(argv[1]);
    printf("%d\n", n);
    printf("Fibonacci Series:\n");
    for (i = 0; i < n; i++) {
        printf("%d ", fibonacci(i));
    }

    return 0;
}
