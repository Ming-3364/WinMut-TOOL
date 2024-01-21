// 测试携带多个变异的子进程再次 fork 的输出
// 1 => 2
// 0 => 1 [2]

#include <stdio.h>
extern int HOLDER[1024];

FILE *file;

__attribute__((noinline))
int Test3(int a, int b)
{
    int sum = a - b;

    printf("stdout : Test3 : [%d : %d]\n", HOLDER[0], sum);
    fprintf(file, "file : Test3 : [%d : %d]\n", HOLDER[0], sum);
    
    return sum;
}

int main(){
    file = fopen("example.txt", "w");

    printf("stdout : output begin! From : %d\n", HOLDER[0]);
    fprintf(file, "file : output begin! From : %d\n", HOLDER[0]);

    int c = Test3(5, 1);
    int d = Test3(5, 5);

    printf("stdout : output end!   From : %d\n", HOLDER[0]);
    fprintf(file, "file : output end!   From : %d\n", HOLDER[0]);

    fclose(file);

    return c + d;
}