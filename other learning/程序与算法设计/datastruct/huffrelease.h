#ifndef HUFFRELEASE_H
#define HUFFRELEASE_H


#include "huffmantree.h"
#include "treedata.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


enum { HUF_CODE_LEN = 100 };

typedef struct
{
    char ch;
    char code[HUF_CODE_LEN];
    int lenth;
}Tcode;

static Tcode huffmanCode[HUF_CODE_LEN];//存储哈夫曼编码的数组

static void encoding(HuffNode ht[] , Tcode book[] , int n)
{
    char *str = (char *)malloc(n+1);
    str[n] = '\0';//编码字符串末尾添加结束符
    int i , j , idx , p;
    for(i = 0 ; i < n ; i++)
    {
        book[i].ch = ht[i].data; //保存字符
        idx = i;
        j = n;
        while((p = ht[idx].parent) >= 0)
        {
            if(ht[p].lchild == idx)
            {
                j--;
                str[j] = '0';
            }
            else
            {
                j--;
                str[j] = '1';
            }
            idx = p;
        }
        strcpy(book[i].code , &str[j]);//保存编码字符�??
        book[i].lenth = n - j; //保存编码长度
    }
    free(str);
}






















#endif
