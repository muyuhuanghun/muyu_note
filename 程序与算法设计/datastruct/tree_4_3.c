#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include "treedata.h"

static void findandkill(BiTree *root, int target)
{
    if(root == NULL || *root == NULL)
    {
        return;
    }
    if((*root)->data == target)
    {
        *root = KillTree(*root);
        return;
    }
    findandkill(&(*root)->left, target);
    findandkill(&(*root)->right, target);
}

int main()
{
    system("chcp 65001 > nul");
    SetConsoleOutputCP(CP_UTF8);
    BiTree bitr_1;
    printf("请输入二叉树节点值（先序输入，0 表示空节点），例如：1 2 0 0 3 0 0\n");
    printf("        1\n");
    printf("       / \\\n");
    printf("      2   3\n");

    CreateBitree(&bitr_1);
    printf("请输入要删除的节点值：\n");
    int target;
    scanf("%d", &target);

    findandkill(&bitr_1, target);

    printf("删除后，前序遍历结果为：\n");
    PreOrder(bitr_1);
    printf("\n");

    KillTree(bitr_1);
    return 0;
}
