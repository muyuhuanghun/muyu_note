#ifdef FINDH_H
#define FINDH_H

#include <stdio.h>
#include <stdlib.h> 
#include <string.h>

typedef struct bnode
{
    int key;
    struct bnode *lchild;
    struct bnode *rchild;
}
BSTNode, *BSTree;

BSTTree searchBST(BSTree T, int key)
{
    if (T == NULL || T->key == key)
    {
        return T;
    }
    else if (key < T->key)
    {
        return searchBST(T->lchild, key);
    }
    else
    {
        return searchBST(T->rchild, key);
    }
}



#endif