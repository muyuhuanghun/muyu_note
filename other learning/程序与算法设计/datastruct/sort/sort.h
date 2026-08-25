#ifndef  SORT_H
#define SORT_H

#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<math.h>
#include<string.h>
#include<math.h>


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


//===============并归排序===================

static void merge(int r1[],int low ,int mid ,int high ,int r[])//合并函数,low为起始位置，mid为中间位置，high为结束位置，r为合并后的数组
{
    int i = low , j = mid +1 , k = low;
    while ((i<=mid) && (j < high))//当左边和右边的元素都没有被合并完时，比较左边和右边的元素，将较小的元素放入合并后的数组中
    {
        if(r1[i]<=r1[j])
        {
            r[k]=r1[i];
            i++;
        }//如果左边的元素小于等于右边的元素，则将左边的元素放入合并后的数组中，并将左边的指针向右移动一位
        else
        {
            r[k]=r1[j];
            j++;
        }//如果右边的元素小于左边的元素，则将右边的元素放入合并后的数组中，并将右边的指针向右移动一位
        k++;
    }
    while(i<=mid)//当左边的元素还没有被合并完时，将左边的元素放入合并后的数组中
    {
        r[k]=r1[i];
        i++;
        k++;
    }
    while(j<=high) //当右边的元素还没有被合并完时，将右边的元素放入合并后的数组中
    {
        r[k]=r1[j];
        j++;
        k++;
    }
}

static void mergesort(int r1[], int low ,int high ,int r[])
{
    if(high == low)
    {
        r[low] = r1[low];
    }
    else
    {
        int * r2 = (int *)malloc((high + 1)*sizeof(int)); // 辅助数组需包含整个区间长度
        int mid = (low + high) / 2;
        mergesort(r1,low,mid,r2);
        mergesort(r1,mid+1,high,r2);
        merge(r2,low,mid,high,r); 
        free(r2);
    }
}


//===============并归排序===================


//===============多关键字排序===================

    //方法一：高位优先 MSD（Most Significant Digit first）排序
        /*
            MSD排序是一种基于比较的排序算法，它通过比较元素的最高位来进行排序。
            它首先将元素分成几个桶，每个桶对应一个可能的最高位值，然后递归地对每个桶中的元素进行排序，
            直到所有元素都被排序完成。MSD排序适用于字符串和整数等类型的数据。
        */




    //方法二：低位优先

        /*
            LSD排序是一种基于比较的排序算法，它通过比较元素的最低位来进行排序。
            它首先将元素分成几个桶，每个桶对应一个可能的最低位值，然后递归地对每个桶中的元素进行排序，
            直到所有元素都被排序完成。LSD排序适用于字符串和整数等类型的数据。
        */

    //方法三：基数排序

        /*
            基数排序是一种非比较的整数排序算法，它通过将整数分成不同的位来进行排序。
            它首先将整数分成几个桶，每个桶对应一个可能的位值，然后递归地对每个桶中的整数进行排序，
            直到所有整数都被排序完成。基数排序适用于整数类型的数据。
        */

    /*
        MSD和LSD排序的区别在于它们比较的位数不同，
        MSD排序比较最高位，而LSD排序比较最低位。基数排序则是通过将整数分成不同的位来进行排序，
        而不是通过比较来进行排序。
    */


//===============多关键字排序===================

//===============链式基数排序===================

typedef struct Node
{
    int data;
    struct Node * next;
}Node,TNode;

typedef struct 
{
    Node * front;
    Node * rear;
}Tpointer;

static TNode * build_list(int R[],int n)
{
    int i;
    TNode * P;
    TNode * ph = (TNode *)malloc(sizeof(TNode));
    ph->next = NULL;
    for(i = 0; i < n; i++)
    {
        P = (TNode *)malloc(sizeof(TNode));
        P->data = R[i];
        P->next = ph->next;
        ph->next = P;
    }
    return ph;
}

void radix_sort(int R[],int n, int d)
{
    int i,j,k;
    Tpointer Q[10];

    for(i = 1; i <= d; i++)
    {
        // 每一轮开始前需要清空队列
        for(j = 0; j < 10; j++)
        {
            Q[j].front = Q[j].rear = NULL;
        }

        for(j = 0; j < n; j++)
        {
            k = (R[j] / (int)pow(10,i-1)) % 10;
            Node * P = (Node *)malloc(sizeof(Node));
            P->data = R[j];
            P->next = NULL;
            if(Q[k].front == NULL)
            {
                Q[k].front = Q[k].rear = P;
            }
            else
            {
                Q[k].rear->next = P;
                Q[k].rear = P;
            }
        }
        int index = 0;
        for(j = 0; j < 10; j++)
        {
            Node * P = Q[j].front;
            while(P != NULL)
            {
                R[index++] = P->data;
                Node * temp = P;
                P = P->next;
                free(temp); // 释放节点避免内存泄漏
            }
        }
    }
}

void dispatch(Tpointer * ph ,Tpointer Q[], int d)
{
    int i,idx;
    TNode * P = NULL;
    for(i = 1; i <= d; i++)
    {
        while(ph->front != NULL)
        {
            idx = (ph->front->data / (int)pow(10,i-1)) % 10;
            Q[idx].rear->next = ph->front;
            Q[idx].rear = ph->front;
            ph->front = ph->front->next;
        }
    }
}


void collect(Tpointer * ph ,Tpointer Q[], int d)
{
    int i;
    TNode * P = NULL;
    for(i = 0; i < 10; i++)
    {
        if(Q[i].front != NULL)
        {
            if(ph->front == NULL)
            {
                ph->front = Q[i].front;
                ph->rear = Q[i].rear;
            }
            else
            {
                ph->rear->next = Q[i].front;
                ph->rear = Q[i].rear;
            }
        }
    }
}
 


//===============链式基数排序===================


#endif
