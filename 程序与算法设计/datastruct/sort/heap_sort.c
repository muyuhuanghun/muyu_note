#include "sort.h"

static int heap_nomal[] = {0,48,62,36,77,65,14,35,99}; // a[0]空闲，数据从a[1]开始

int main()
{
    int n = sizeof(heap_nomal)/sizeof(heap_nomal[0]) - 1; // 减去a[0]的空闲位
    heap_sort(heap_nomal, n);
    for(int i = 1; i <= n; i++)
        printf("%d ", heap_nomal[i]);
    return 0;
}