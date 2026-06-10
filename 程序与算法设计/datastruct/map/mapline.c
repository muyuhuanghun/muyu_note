#include "mapline.h"

// 定义全局的访问数组
int visited[MAX_VERTEX];

// ========================
// 辅助队列基本操作实现 (用于 BFS)
// ========================

// 初始化队列
void InitQueue(Queue *Q) {
    Q->front = 0;
    Q->rear = 0;
}

// 判断队列是否为空。为空返回1，否则返回0
int QueueEmpty(Queue Q) {
    if (Q.front == Q.rear) {
        return 1;
    } else {
        return 0;
    }
}

// 元素 e 入队
void EnQueue(Queue *Q, int e) {
    if ((Q->rear + 1) % MAX_VERTEX == Q->front) {
        // 队列满，简单处理直接返回
        return;
    }
    Q->data[Q->rear] = e;
    Q->rear = (Q->rear + 1) % MAX_VERTEX;
}

// 队头元素出队，并用 e 返回
void DeQueue(Queue *Q, int *e) {
    if (Q->front == Q->rear) {
        // 队列空
        return;
    }
    *e = Q->data[Q->front];
    Q->front = (Q->front + 1) % MAX_VERTEX;
}

// ========================
// 图的基本操作实现
// ========================

// 初始化图
void InitGraph(ALGraph *G) {
    int i;
    G->vexnum = 0;
    G->arcnum = 0;
    for (i = 0; i < MAX_VERTEX; i++) {
        G->vertices[i].firstarc = NULL;
    }
}

// 添加顶点，返回顶点下标，失败返回 -1
int AddVertex(ALGraph *G, char data) {
    if (G->vexnum >= MAX_VERTEX) return -1;
    G->vertices[G->vexnum].data = data;
    G->vertices[G->vexnum].firstarc = NULL;
    return G->vexnum++;
}

// 添加有向边 (from -> to)，失败返回 -1
int AddEdge(ALGraph *G, int from, int to) {
    ArcNode *node;
    if (from < 0 || from >= G->vexnum || to < 0 || to >= G->vexnum) return -1;
    node = (ArcNode *)malloc(sizeof(ArcNode));
    if (!node) return -1;
    node->adjvex = to;
    node->nextarc = G->vertices[from].firstarc;
    G->vertices[from].firstarc = node;
    G->arcnum++;
    return 0;
}

// 查找顶点下标，未找到返回 -1
int LocateVex(ALGraph G, char v) {
    int i;
    for (i = 0; i < G.vexnum; i++) {
        if (G.vertices[i].data == v) return i;
    }
    return -1;
}

// ========================
// 图的遍历操作实现
// ========================

// 深度优先搜索 (DFS) 核心逻辑
// v 表示当前正在访问的顶点下标
void DFS(ALGraph G, int v) {
    ArcNode *p;

    // 1. 访问当前顶点，并将其标记为已访问
    printf("%c ", G.vertices[v].data);
    visited[v] = 1;

    // 2. 遍历当前顶点的所有邻接点
    p = G.vertices[v].firstarc;
    while (p != NULL) {
        int w = p->adjvex;
        // 如果邻接点 w 未被访问过，则对其进行递归 DFS 访问
        if (!visited[w]) {
            DFS(G, w);
        }
        p = p->nextarc; // 找下一个邻接点
    }
}

// 深度优先遍历入口 (处理非连通图)
void DFSTraverse(ALGraph G) {
    int i;
    // 1. 初始化访问数组为 0 (未访问)
    for (i = 0; i < G.vexnum; i++) {
        visited[i] = 0;
    }

    // 2. 遍历每一个顶点，如果未访问则作为起点调用 DFS 
    // (这层循环主要是为了防止图有多个连通分量/非连通图时漏掉顶点)
    printf("DFS 遍历结果: ");
    for (i = 0; i < G.vexnum; i++) {
        if (!visited[i]) {
            DFS(G, i);
        }
    }
    printf("\n");
}

// 广度优先遍历 (BFS) - 类似于树的层序遍历
void BFSTraverse(ALGraph G) {
    int i, v;
    ArcNode *p;
    Queue Q;

    // 1. 初始化访问数组为 0 和辅助队列
    for (i = 0; i < G.vexnum; i++) {
        visited[i] = 0;
    }
    InitQueue(&Q);

    printf("BFS 遍历结果: ");
    // 2. 遍历每一个顶点，处理可能有多个连通分量的情况
    for (i = 0; i < G.vexnum; i++) {
        if (!visited[i]) {
            // 访问该顶点并标记
            printf("%c ", G.vertices[i].data);
            visited[i] = 1;
            
            // 将顶点 i 入队
            EnQueue(&Q, i);

            // 当队列不空时，不断取出顶点并访问其未访问的邻接点
            while (!QueueEmpty(Q)) {
                DeQueue(&Q, &v); // 队头元素出队到 v
                
                // 遍历 v 的所有邻接点
                p = G.vertices[v].firstarc;
                while (p != NULL) {
                    int w = p->adjvex;
                    if (!visited[w]) {
                        // 访问、标记、入队
                        printf("%c ", G.vertices[w].data);
                        visited[w] = 1;
                        EnQueue(&Q, w);
                    }
                    p = p->nextarc; // 找下一个邻接点
                }
            }
        }
    }
    printf("\n");
}

