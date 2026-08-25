#define MaxSize 1000
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include "matrixx.h"

int main()
{
    system("chcp 65001 > nul");
    SetConsoleOutputCP(CP_UTF8);
    tsmatrix M;
    tsmatrix N;

    printf("请输入第一个矩阵的 行数 列数 非零元素个数：\n");
    scanf("%d %d %d", &M.m, &M.n, &M.len);
    printf("请输入第一个矩阵的非零元素（行 列 值）：\n");
    for(int i=0;i<M.len;i++)
    {
        scanf("%d %d %d", &M.data[i].row, &M.data[i].col, &M.data[i].data);
    }

    printf("请输入第二个矩阵的 行数 列数 非零元素个数：\n");
    scanf("%d %d %d", &N.m, &N.n, &N.len);
    printf("请输入第二个矩阵的非零元素（行 列 值）：\n");
    for(int i=0;i<N.len;i++)
    {
        scanf("%d %d %d", &N.data[i].row, &N.data[i].col, &N.data[i].data);
    }

    tsmatrix * result_add = matrixadd(&M,&N);

    printf("\n矩阵相加结果：\n");
    for(int i=0;i<result_add->m;i++)
    {
        for(int j=0;j<result_add->n;j++)
        {
            int k;
            for(k=0;k<result_add->len;k++)
            {
                if(result_add->data[k].row==i && result_add->data[k].col==j)
                {
                    printf("%d ",result_add->data[k].data);
                    break;
                }
            }
            if(k==result_add->len)
            {
                printf("0 ");
            }
        }
        printf("\n");
    }

    free(result_add);
    return 0;
}