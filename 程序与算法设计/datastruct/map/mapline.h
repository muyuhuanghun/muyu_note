#ifndef MAPLINE_H
#define MAPLINE_H

#include <stdio.h>
#include <stdlib.h>

#define MAX_VERTEX 100
#define INFINITY 32768

// 1. 边节点结构：表示一条边
typedef struct ArcNode {
    int adjvex;                // 该边指向的顶点在数组中的下标
    struct ArcNode *nextarc;   // 指向下一条边的指针
    // int weight;             // 如果是带权图，可以取消注释添加权值
} ArcNode;

// 2. 顶点节点结构：数组中的每一个元素
typedef struct VNode {
    char data;                 // 顶点的信息（如 'A', 'B' 等）
    ArcNode *firstarc;         // 指向该顶点连接的第一条边
} VNode, AdjList[MAX_VERTEX];

// 3. 邻接表结构：包含所有顶点和计数
typedef struct {
    AdjList vertices;          // 顶点数组
    int vexnum;                // 图中当前的顶点数
    int arcnum;                // 图中当前的边数
} ALGraph;

// --- 图的基本操作 ---
void InitGraph(ALGraph *G);
int AddVertex(ALGraph *G, char data);
int AddEdge(ALGraph *G, int from, int to);
int LocateVex(ALGraph G, char v);

// --- 遍历支持 ---

// 访问标记数组，用于 DFS 和 BFS
// 约定：0表示未访问，1表示已访问
extern int visited[MAX_VERTEX];

// 简单的循环队列，用于 BFS 遍历
typedef struct {
    int data[MAX_VERTEX];
    int front, rear;
} Queue;

// 队列基本操作 (供 BFS 使用)
void InitQueue(Queue *Q);
int QueueEmpty(Queue Q);
void EnQueue(Queue *Q, int e);
void DeQueue(Queue *Q, int *e);

// --- 遍历函数原型 ---

// 深度优先遍历 (Depth First Search)
void DFS(ALGraph G, int v);
void DFSTraverse(ALGraph G);

// 广度优先遍历 (Breadth First Search)
void BFSTraverse(ALGraph G);

#endif

//check the correct type of note

//i can't even undeerstand what hapened about the livesynvc system 