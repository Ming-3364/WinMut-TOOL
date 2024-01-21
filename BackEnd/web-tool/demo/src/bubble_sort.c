#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline))
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                // 交换元素
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

int main(int argc, char *argv[]) {

    int array_size = argc - 1;
    int *myArray = (int *)malloc(array_size * sizeof(int));
    for (int i = 0; i < array_size; i++) {
        myArray[i] = atoi(argv[i + 1]);
    }

    bubbleSort(myArray, array_size);

    printf("Sorted array: \n");
    for (int i=0; i < array_size; i++)
        printf("%d ", myArray[i]);
    
    free(myArray);
    return 0;
}
