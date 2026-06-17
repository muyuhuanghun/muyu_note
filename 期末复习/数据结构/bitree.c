#include <stdio.h>
#include <stdlib.h>

typedef char ElemType;

// 二叉树节点定义
typedef struct BiTNode {
    ElemType data;
    struct BiTNode *lchild, *rchild;
} BiTNode, *BiTree;

// 创建新节点
BiTNode* CreateNode(ElemType data) {
    BiTNode *node = (BiTNode *)malloc(sizeof(BiTNode));
    node->data = data;
    node->lchild = NULL;
    node->rchild = NULL;
    return node;
}

// 先序遍历
void PreOrder(BiTree T) {
    if (T == NULL) return;
    printf("%c ", T->data);
    PreOrder(T->lchild);
    PreOrder(T->rchild);
}

// 中序遍历
void InOrder(BiTree T) {
    if (T == NULL) return;
    InOrder(T->lchild);
    printf("%c ", T->data);
    InOrder(T->rchild);
}

// 后序遍历
void PostOrder(BiTree T) {
    if (T == NULL) return;
    PostOrder(T->lchild);
    PostOrder(T->rchild);
    printf("%c ", T->data);
}

// 求树的深度
int TreeDepth(BiTree T) {
    if (T == NULL) return 0;

    int l = TreeDepth(T->lchild); 
    int r = TreeDepth(T->rchild);
    return (l > r ? l : r) + 1;
}

// 求节点个数
int NodeCount(BiTree T) {
    if (T == NULL) return 0;

    int leftCount = NodeCount(T->lchild);  // 先去把左子树的节点数算出来，记在账本上
    int rightCount = NodeCount(T->rchild); // 再去把右子树的节点数算出来，记在账本上

    return leftCount + rightCount + 1;     // 最后：左边 + 右边 + 我自己(1)，上报给上一层
}

// 求叶子节点个数
int LeafCount(BiTree T) {
    if (T == NULL) return 0;
    if (T->lchild == NULL && T->rchild == NULL) return 1;

    int leftLeaf = LeafCount(T->lchild);   // 去把左子树的叶子节点数算出来，记在账本上
    int rightLeaf = LeafCount(T->rchild); // 再去把右子树的叶子节点数算出来，记在账本上

    // 最后汇总：把我左边的叶子和右边的叶子加起来，上报给上一层
    return leftLeaf + rightLeaf;
}

// 层次遍历（需要队列）
#define MaxSize 100

// 队列节点（存储树节点指针）
typedef struct {
    BiTNode *data[MaxSize]; # 数组中的每个元素也是指针
    int front, rear;
} Queue;

void InitQueue(Queue *Q) { Q->front = 0; Q->rear = 0; }
bool IsEmpty(Queue Q) { return Q.front == Q.rear; }

bool EnQueue(Queue *Q, BiTNode *node) {
    if ((Q->rear + 1) % MaxSize == Q->front) return false;
    Q->data[Q->rear] = node;
    Q->rear = (Q->rear + 1) % MaxSize;
    return true;
}
bool DeQueue(Queue *Q, BiTNode **node) {
    if (Q->front == Q->rear) return false; # 判断队列是否为空
    *node = Q->data[Q->front];
    Q->front = (Q->front + 1) % MaxSize;
    return true;
}

void LevelOrder(BiTree T) {
    if (T == NULL) return;
    Queue Q;
    InitQueue(&Q);
    EnQueue(&Q, T);

    while (!IsEmpty(Q)) {
        BiTNode *node;
        DeQueue(&Q, &node);
        printf("%c ", node->data);
        if (node->lchild) EnQueue(&Q, node->lchild);
        if (node->rchild) EnQueue(&Q, node->rchild);
    }
}

// 销毁二叉树
void DestroyTree(BiTree T) {
    if (T == NULL) return;
    DestroyTree(T->lchild);
    DestroyTree(T->rchild);
    free(T);
}

int main() {
    //       A
    //      / \
    //     B   C
    //    / \
    //   D   E
    BiTree T = CreateNode('A');
    T->lchild = CreateNode('B');
    T->rchild = CreateNode('C');
    T->lchild->lchild = CreateNode('D');
    T->lchild->rchild = CreateNode('E');

    printf("先序遍历: ");
    PreOrder(T);
    printf("\n");

    printf("中序遍历: ");
    InOrder(T);
    printf("\n");

    printf("后序遍历: ");
    PostOrder(T);
    printf("\n");

    printf("层次遍历: ");
    LevelOrder(T);
    printf("\n");

    printf("树的深度: %d\n", TreeDepth(T));
    printf("节点个数: %d\n", NodeCount(T));
    printf("叶子节点: %d\n", LeafCount(T));

    DestroyTree(T);
    return 0;
}
