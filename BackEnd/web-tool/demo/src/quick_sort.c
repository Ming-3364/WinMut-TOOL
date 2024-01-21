#include <stdio.h>
#include <stdlib.h>

// 交换数组中两个元素的值
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 在数组中选择一个基准元素，并将数组划分为两部分
int partition(int arr[], int low, int high) {
    int pivot = arr[high]; // 选择数组最后一个元素作为基准
    int i = low - 1;       // 初始化较小元素的索引

    for (int j = low; j < high; j++) {
        // 如果当前元素小于或等于基准元素，将其交换到较小元素的位置
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }

    // 将基准元素交换到正确的位置
    swap(&arr[i + 1], &arr[high]);

    return i + 1;
}

// 实现快速排序
void quickSort(int arr[], int low, int high) {
    if (low < high) {
        // 划分数组，获取基准元素的索引
        int pivotIndex = partition(arr, low, high);

        // 递归对基准元素左边的子数组进行排序
        quickSort(arr, low, pivotIndex - 1);

        // 递归对基准元素右边的子数组进行排序
        quickSort(arr, pivotIndex + 1, high);
    }
}

// 打印数组
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main(int argc, char *argv[]) {
    int array_size = argc - 1;
    int *myArray = (int *)malloc(array_size * sizeof(int));
    for (int i = 0; i < array_size; i++) {
        myArray[i] = atoi(argv[i + 1]);
    }

    printf("原始数组: ");
    printArray(myArray, array_size);

    // 调用快速排序算法
    quickSort(myArray, 0, array_size - 1);

    printf("排序后的数组: ");
    printArray(myArray, array_size);

    free(myArray);
    return 0;
}
