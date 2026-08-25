#ifndef HUFFMANTREE_H
#define HUFFMANTREE_H


#include<stdio.h>
#include<stdlib.h>
#include<string.h>


#ifndef MaxSize
#define MaxSize 1000
#endif


typedef struct huffnode
{
    char data;
    int weight;
    int parent;
    int lchild;
    int rchild;
} HuffNode;


static void creatht(HuffNode ht[], int n)
{
    int i, k, lnode, rnode;
    double min1, min2;

    // 初始化所有结点的双亲和孩子下标为 -1（表示不存在）
    // 哈夫曼树总节点数是 2*n-1
    for (i = 0; i < 2 * n - 1; i++)
    {
        ht[i].parent = -1;
        ht[i].lchild = -1;
        ht[i].rchild = -1;
    }

    // 从第 n 个结点开始逐步构造非叶子结点
    // 注意：前 n 个结点通常是已知权值的叶子结点
    for (i = n; i < 2 * n - 1; i++)
    {
        // 每一轮都要在 [0, i-1] 中找两个 parent==-1 的最小权值结点
        min1 = min2 = 32767;
        lnode = rnode = -1;

        for (k = 0; k < i; k++)
        {
            // 只在“还没被合并”的结点里选最小值
            if (ht[k].parent == -1)
            {
                if (ht[k].weight < min1)
                {
                    // 当前最小值下沉为第二小
                    min2 = min1;
                    rnode = lnode;

                    // 更新最小值
                    min1 = ht[k].weight;
                    lnode = k;
                }
                else if (ht[k].weight < min2)
                {
                    // 更新第二小值
                    min2 = ht[k].weight;
                    rnode = k;
                }
            }
        }

        // 用两个最小结点合并出新结点 i
        ht[i].weight = ht[lnode].weight + ht[rnode].weight;
        ht[i].lchild = lnode;
        ht[i].rchild = rnode;

        // 标记这两个孩子已被合并，双亲为 i
        ht[lnode].parent = i;
        ht[rnode].parent = i;
    }
}



















#endif
