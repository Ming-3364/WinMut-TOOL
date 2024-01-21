#include <stdio.h>
#include <string.h>

__attribute__((noinline))
void reverseString(char str[]) {
    int start = 0;
    int end = strlen(str) - 1;

    while (start < end) {
        // 交换字符
        char temp = str[start];
        str[start] = str[end];
        str[end] = temp;

        start++;
        end--;
    }
}

int main(int argc, char *argv[]) {
    char* str;
    if (argc == 2)
        str = argv[1];
    else
        str = "";
    
    printf("Original string: %s\n", str);

    reverseString(str);

    printf("Reversed string: %s\n", str);

    return 0;
}
