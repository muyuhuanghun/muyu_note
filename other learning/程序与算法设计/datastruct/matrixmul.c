#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#define MaxSize 1000000
#include "matrixx.h"

int main()
{
    system("chcp 65001 > nul");
    SetConsoleOutputCP(CP_UTF8);
    tsmatrix *M = (tsmatrix*)malloc(sizeof(tsmatrix));
    tsmatrix *N = (tsmatrix*)malloc(sizeof(tsmatrix));
    if(M == NULL || N == NULL)
    {
        printf("内存申请失败。\n");
        free(M);
        free(N);
        return 0;
    }

    printf("请输入第一个矩阵的 行数 列数 非零元素个数：\n");
    scanf("%d %d %d", &M->m, &M->n, &M->len);
    if(M->len > MaxSize)
    {
        printf("第一个矩阵非零元素个数超过上限 %d。\n", MaxSize);
        free(M);
        free(N);
        return 0;
    }
    printf("请输入第一个矩阵的非零元素（行 列 值）：\n");
    for(int i=0;i<M->len;i++)
    {
        scanf("%d %d %d", &M->data[i].row, &M->data[i].col, &M->data[i].data);
    }

    printf("请输入第二个矩阵的 行数 列数 非零元素个数：\n");
    scanf("%d %d %d", &N->m, &N->n, &N->len);
    if(N->len > MaxSize)
    {
        printf("第二个矩阵非零元素个数超过上限 %d。\n", MaxSize);
        free(M);
        free(N);
        return 0;
    }
    printf("请输入第二个矩阵的非零元素（行 列 值）：\n");
    for(int i=0;i<N->len;i++)
    {
        scanf("%d %d %d", &N->data[i].row, &N->data[i].col, &N->data[i].data);
    }

    tsmatrix * result_mul = matrixmul(M, N);
    if(result_mul == NULL)
    {
        printf("\n矩阵无法相乘（列行不匹配）或结果超过最大存储上限 %d。\n", MaxSize);
        free(M);
        free(N);
        return 0;
    }

    printf("\n矩阵相乘结果：\n");
    for(int i=0;i<result_mul->m;i++)
    {
        for(int j=0;j<result_mul->n;j++)
        {
            int k;
            for(k=0;k<result_mul->len;k++)
            {
                if(result_mul->data[k].row==i && result_mul->data[k].col==j)
                {
                    printf("%d ",result_mul->data[k].data);
                    break;
                }
            }
            if(k==result_mul->len)
            {
                printf("0 ");
            }
        }
        printf("\n");
    }

    free(result_mul);
    free(M);
    free(N);
    return 0;
}
