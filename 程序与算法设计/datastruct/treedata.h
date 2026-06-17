#ifndef TREEDATA_H
#define TREEDATA_H

#include <stdio.h>
#include <stdlib.h>

#ifndef MaxSizex
#define MaxSizex 1000
#endif

typedef struct BiTNode
{
    int data;
    struct BiTNode *left;
    struct BiTNode *right;
    struct BiTNode *parent;
} BiTNode, *BiTree;//二叉树类型定�?

static void CreateBitree(BiTree *Bt)//先序输入二叉�?
{
    int x;
    scanf("%d", &x);
    if(x == 0)
    {
        *Bt = NULL;
    }
    else
    {
        *Bt = (BiTree)malloc(sizeof(BiTNode));
        if(*Bt == NULL)
        {
            printf("内存申请失败。\n");
            exit(1);
        }
        (*Bt)->data = x;
        (*Bt)->parent = NULL;
        CreateBitree(&(*Bt)->left);
        if((*Bt)->left != NULL)
        {
            (*Bt)->left->parent = *Bt;
        }
        CreateBitree(&(*Bt)->right);
        if((*Bt)->right != NULL)
        {
            (*Bt)->right->parent = *Bt;
        }
    }
}

static void PreOrder(BiTree Bt)//先序遍历
{
    if(Bt != NULL)
    {
        printf("%d ", Bt->data);
        PreOrder(Bt->left);
        PreOrder(Bt->right);
    }
}

static void preorderinarr(BiTree root ,int arr[] ,int *index)
{
    if(root != NULL)
    {
        arr[*index] = root->data;
        (*index)++;
        preorderinarr(root->left, arr, index);
        preorderinarr(root->right, arr, index);
    }
}//先序遍历将树的节点值存入数�?

static int getpreorder(BiTree root, int arr[])
{
    int index = 0;
    preorderinarr(root, arr, &index);
    return index;
}//获取树的先序遍历结果存入数组，并返回节点个数

static void InOrder(BiTree Bt)//中序遍历
{
    if(Bt != NULL)
    {
        InOrder(Bt->left);
        printf("%d ", Bt->data);
        InOrder(Bt->right);
    }
}

static void PostOrder(BiTree Bt)//后序遍历
{
    if(Bt != NULL)
    {
        PostOrder(Bt->left);
        PostOrder(Bt->right);
        printf("%d ", Bt->data);
    }
}

static int CountNodes(BiTree root)//统计节点个数
{
    if(root == NULL)
    {
        return 0;
    }
    return 1 + CountNodes(root->left) + CountNodes(root->right);
}

static int _post_tree_depth(BiTree root, int h, int *maxDepth)
{
    if(root == NULL)
    {
        if(h > *maxDepth)
        {
            *maxDepth = h;
        }
    }
    else
    {
        _post_tree_depth(root->left, h + 1, maxDepth);
        _post_tree_depth(root->right, h + 1, maxDepth);
    }
    return *maxDepth;
}

static int PostTreeDepth(BiTree root, int h)//后序遍历求树深度
{
    int maxDepth = 0;
    return _post_tree_depth(root, h, &maxDepth);
}

static BiTree KillTree(BiTree root)//后序遍历销毁树
{
    if(root != NULL)
    {
        KillTree(root->left);
        KillTree(root->right);
        free(root);
    }
    return NULL;
}



















typedef struct stacktree
{
    BiTree stackdata[MaxSizex];
    int top;
}stacktree, *StackTree;

static void initstack(StackTree s)
{
    s->top = -1;
}

static int stackisempty(StackTree s)
{
    return s->top == -1;
}

static void destroystack(StackTree s)
{
    s->top = -1;
}

static void poptree(StackTree s, BiTree *e)
{
    if(s->top == -1)
    {
        printf("栈空，无法弹出元素。\n");
        exit(1);
    }
    *e = s->stackdata[s->top];
    s->top--;
}

static void pushtree(StackTree s, BiTree e)
{
    if(s->top == MaxSizex - 1)
    {
        printf("栈满，无法压入元素。\n");
        exit(1);
    }
    s->stackdata[++s->top] = e;
}

static void PreOrder1(BiTNode *b) {
       BiTNode *p = NULL;
       stacktree st;				//定义栈指针st
       initstack(&st);			//初始化栈st
       if (b!=NULL) 
       {
            pushtree(&st,b);			//根结点进�?
            while (!stackisempty(&st)) 
            { 	//栈不为空时循�?
                    poptree(&st,&p);			//退栈结点p并访问它
                    printf("%d ",p->data);
                    if (p->right!=NULL)	//有右孩子时将其进�?
                        pushtree(&st,p->right);
                    if (p->left!=NULL)	//有左孩子时将其进�?
                        pushtree(&st,p->left);
                }
            printf("\n");
       }
       destroystack(&st);			//销毁栈
}

static void preorder2(BiTNode *b) {
       BiTNode *p=b;
       stacktree st;				//定义栈指针st
       initstack(&st);			//初始化栈st
       while (p!=NULL || !stackisempty(&st)) 
       { 	//p不空或栈不空时循�?
            while (p!=NULL) 
            { 	//p不空时循�?
                    printf("%d ",p->data);	//访问结点p
                    pushtree(&st,p);			//结点p进栈
                    p=p->left;				//p指向左孩�?
                }
            if (!stackisempty(&st)) 
            { 	//栈不空时退栈并令p指向退栈结点的右孩�?
                    poptree(&st,&p);
                    p=p->right;
                }
        }
       printf("\n");
       destroystack(&st);			//销毁栈
}

static void inorder(BiTNode * root)
{
    BiTNode *p=root;
    stacktree st;				//定义栈指针st
    initstack(&st);			//初始化栈st
    while (p!=NULL || !stackisempty(&st)) 
    { 	//p不空或栈不空时循�?
        while (p!=NULL) 
        { 	//p不空时循�?
            pushtree(&st,p);			//结点p进栈
            p=p->left;				//p指向左孩�?
        }
        if (!stackisempty(&st)) 
        { 	//栈不空时退栈并令p指向退栈结点的右孩�?
            poptree(&st,&p);
            printf("%d ",p->data);	//访问结点p
            p=p->right;
        }
    }
    printf("\n");
    destroystack(&st);			//销毁栈
}


#endif
