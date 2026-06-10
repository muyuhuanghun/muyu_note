#ifndef  SORT_H
#define SORT_H

#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>


//===============堆排序================

static void sift(int a[],int k ,int m)
{
    a[0] = a[k];
    int j = 2*k;  bool done = false;
    while(j <= m && !done)
    {
        if(j < m && a[j] < a[j+1] ) j++;
        if(a[0] >= a[j]) done = true;
        else
        {
            a[k] = a[j];
            k = j; j = 2*k;
        }
    }
    a[k] = a[0];
}

static void create_heap(int a[],int n)
{
    for(int i = n/2; i > 0; i--)
        sift(a,i,n);
}

static void heap_sort(int a[],int n)
{
    create_heap(a,n);
    for(int i = n; i > 1; i--)
    {
        int temp = a[1];
        a[1] = a[i];
        a[i] = temp;
        sift(a,1,i-1);
    }
}

//===============堆排序================

//===============快速排序================

static void swap(int *a,int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}


static int partition(int a[],int low,int high)//划分函数,low为起始位置，high为结束位置
{
    int pivot = a[low];
    while(low < high)
    {
        while(low < high && a[high] >= pivot) high--;
        swap(&a[low],&a[high]);
        while(low < high && a[low] <= pivot) low++;
        swap(&a[low],&a[high]);
    }
    a[low] = pivot;
    return low;
}

static void quick_sort(int a[],int low,int high)//快速排序函数，low为起始位置，high为结束位置,递归调用
{
    if(low < high)
    {
        int pivot = partition(a,low,high);
        quick_sort(a,low,pivot-1);
        quick_sort(a,pivot+1,high);
    }
}

//===============快速排序================


//===============简单选择排序================

static void selection_sort(int a[],int n)
{
    for(int i = 0; i < n-1; i++)
    {
        int min_index = i;
        for(int j = i+1; j < n; j++)
            if(a[j] < a[min_index]) min_index = j;
        swap(&a[i],&a[min_index]);
    }
}

//===============简单选择排序================


#endif
