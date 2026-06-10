#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#define MaxSize 1000

int LCAIndex(int i, int j)
{
    if(i <= 0 || j <= 0)
    {
        return -1;
    }

    while(i != j)
    {
        if(i > j)
        {
            i = i / 2;
        }
        else
        {
            j = j / 2;
        }
    }
    return i;
}

int main()
{
    system("chcp 65001 > nul");
    SetConsoleOutputCP(CP_UTF8);
    int A[MaxSize + 1];
    int n, i, j;

    printf("请输入顺序存储数组长度 n(1~%d)：\n", MaxSize);
    scanf("%d", &n);
    if(n <= 0 || n > MaxSize)
    {
        printf("n 不合法。\n");
        return 0;
    }

    printf("请输入 A[1]~A[%d]（空节点可用 0 表示）：\n", n);
    for(int k = 1; k <= n; k++)
    {
        scanf("%d", &A[k]);
    }

    printf("请输入两个节点下标 i j：\n");
    scanf("%d %d", &i, &j);

    if(i < 1 || i > n || j < 1 || j > n)
    {
        printf("下标越界。\n");
        return 0;
    }
    if(A[i] == 0 || A[j] == 0)
    {
        printf("i 或 j 对应空节点，不存在最近公共祖先。\n");
        return 0;
    }

    int ans = LCAIndex(i, j);
    if(ans == -1 || ans > n || A[ans] == 0)
    {
        printf("不存在最近公共祖先。\n");
    }
    else
    {
        printf("最近公共祖先节点下标为：%d\n", ans);
    }

    return 0;
}