# C 语言数据结构实现

> 📌 基于 C 语言的数据结构课程代码实现，涵盖矩阵、树、图、查找、排序五大模块。
> 所有代码均通过头文件 `.h` 组织，主函数 `.c` 负责调用测试。

---

## 📂 项目结构

```
datastruct/
├── matrixx.h          # 稀疏矩阵（三元组存储 + 加法/乘法）
├── matrix.c           # 矩阵加法测试
├── matrixmul.c        # 矩阵乘法测试
├── treedata.h         # 二叉树（创建/遍历/销毁 + 栈式非递归遍历）
├── treehomework.c     # 作业：查找并删除子树
├── tree_4_3.c         # 作业：顺序存储二叉树求最近公共祖先
├── huffmantree.h      # 哈夫曼树构建
├── huffrelease.h      # 哈夫曼编码
├── stack.h            # 泛型动态栈（自动扩容）
├── map/
│   ├── mapp.h         # 邻接矩阵图 + Dijkstra 最短路径（成都地铁）
│   ├── map.c          # 地铁最短路径查询主程序
│   ├── mapline.h      # 邻接表图 + DFS/BFS 遍历
│   └── mapline.c      # 邻接表遍历实现
├── find/
│   ├── findh.h        # 二叉搜索树（BST）查找
│   ├── hashtable.h    # 哈希表（除留余数法 + 线性探测）
│   └── hashtable.c    # 哈希表完整实现与测试
└── sort/
    ├── sort.h         # 堆排序 / 快速排序 / 简单选择排序
    └── heap_sort.c    # 堆排序测试
```

---

## 1️⃣ 稀疏矩阵（三元组存储）

### 数据结构定义

```c
// 三元组：行、列、值
typedef struct {
    int row, col;
    int data;
} triple;

// 稀疏矩阵：三元组数组 + 行数/列数/非零元素个数
typedef struct {
    triple data[MaxSizex];
    int m, n, len;
} tsmatrix;
```

### 矩阵加法 — `matrixadd()`

🌟 核心思路：双指针归并。由于三元组按行优先、同行按列排序，可以用类似归并排序的双指针策略：

- 行列相同 → 值相加（结果为 0 则跳过）
- A 的列 < B 的列 → 取 A
- A 的列 > B 的列 → 取 B
- A 的行 < B 的行 → 取 A
- A 的行 > B 的行 → 取 B

```c
while(i < A->len && j < B->len) {
    if(A->data[i].row == B->data[j].row) {
        if(A->data[i].col == B->data[j].col) {
            int sum = A->data[i].data + B->data[j].data;
            if(sum != 0) { /* 存入结果 */ }
            i++; j++;
        } else if(A->data[i].col < B->data[j].col) {
            /* 取 A[i] */ i++;
        } else {
            /* 取 B[j] */ j++;
        }
    } else if(A->data[i].row < B->data[j].row) {
        /* 取 A[i] */ i++;
    } else {
        /* 取 B[j] */ j++;
    }
}
```

⚠️ 注意：`MaxSize` 和 `MaxSizex` 混用可能导致宏定义冲突（代码中 `matrixadd` 第 86 行使用了 `MaxSize` 而非 `MaxSizex`）。

### 矩阵乘法 — `matrixmul()`

🌟 核心思路：对 A 的每个非零元素 `(i, k)`，找 B 中所有 `(k, j)` 的元素，累乘到结果 `(i, j)` 位置。

```c
for(int i = 0; i < A->len; i++) {
    for(int j = 0; j < B->len; j++) {
        if(A->data[i].col == B->data[j].row) {
            // 找到匹配：A[i].col == B[j].row
            // 结果位置 (A[i].row, B[j].col)
            // 在结果中查找是否已有该位置，有则累加，无则新增
        }
    }
}
```

⚠️ 乘法的时间复杂度为 O(A->len × B->len × c->len)，稀疏矩阵较大时效率较低。可优化为转置 B 后用哈希表加速查找。

---

## 2️⃣ 二叉树

### 数据结构定义

```c
typedef struct BiTNode {
    int data;
    struct BiTNode *left;
    struct BiTNode *right;
    struct BiTNode *parent;    // 🌟 带父指针，方便回溯
} BiTNode, *BiTree;
```

### 基本操作

| 操作 | 实现方式 | 说明 |
|:---|:---|:---|
| `CreateBitree()` | 先序递归 | 输入 0 表示空节点，自动设置 parent 指针 |
| `PreOrder()` | 先序递归 | 根→左→右 |
| `InOrder()` | 中序递归 | 左→根→右 |
| `PostOrder()` | 后序递归 | 左→右→根 |
| `CountNodes()` | 递归 | `1 + count(left) + count(right)` |
| `PostTreeDepth()` | 后序遍历 | 用 static 变量记录最大深度 |
| `KillTree()` | 后序销毁 | 必须后序！先销毁子树再 free 根 |

### 非递归遍历（栈实现）

📌 递归遍历虽然简洁，但存在栈溢出风险。代码实现了两种非递归先序遍历：

**方法一：经典栈模拟**

```c
// 根节点进栈 → 循环：弹出并访问 → 右孩子进栈 → 左孩子进栈
pushtree(&st, b);
while(!stackisempty(&st)) {
    poptree(&st, &p);
    printf("%d ", p->data);
    if(p->right) pushtree(&st, p->right);  // 右先进，后出
    if(p->left)  pushtree(&st, p->left);   // 左后进，先出
}
```

**方法二：Morris 思路的栈版本**

```c
// 一路向左走，沿途访问并入栈；到头后弹栈转向右子树
while(p != NULL || !stackisempty(&st)) {
    while(p != NULL) {
        printf("%d ", p->data);  // 先序：入栈前访问
        pushtree(&st, p);
        p = p->left;
    }
    if(!stackisempty(&st)) {
        poptree(&st, &p);
        p = p->right;
    }
}
```

💡 中序非递归只需把 `printf` 移到 `poptree` 之后——这就是 `inorder()` 函数的做法。

### 作业题：查找并删除子树

```c
// 递归查找目标值，找到后销毁以该节点为根的子树
static void findandkill(BiTree *root, int target) {
    if(root == NULL || *root == NULL) return;
    if((*root)->data == target) {
        *root = KillTree(*root);  // 销毁子树并置空指针
        return;
    }
    findandkill(&(*root)->left, target);
    findandkill(&(*root)->right, target);
}
```

### 作业题：顺序存储二叉树求 LCA

📌 完全二叉树用数组存储时，节点 `i` 的父节点为 `i/2`。求最近公共祖先（LCA）只需不断将较大下标除以 2 直到相等：

```c
int LCAIndex(int i, int j) {
    while(i != j) {
        if(i > j) i = i / 2;
        else      j = j / 2;
    }
    return i;
}
```

⚠️ 需要额外检查：下标越界、空节点（值为 0）、LCA 是否存在。

---

## 3️⃣ 哈夫曼树与编码

### 哈夫曼树构建

```c
typedef struct huffnode {
    char data;
    int weight;
    int parent, lchild, rchild;  // 数组下标表示，-1 表示不存在
} HuffNode;
```

🌟 构建算法（贪心）：
1. 初始化 `2n-1` 个节点，前 `n` 个为叶子
2. 从第 `n` 个开始，每轮在未合并节点中选两个最小权值节点
3. 合并为新节点，权值相加

```c
for(i = n; i < 2*n-1; i++) {
    // 在 [0, i-1] 中找 parent==-1 的最小两个节点
    min1 = min2 = 32767;
    for(k = 0; k < i; k++) {
        if(ht[k].parent == -1) {
            if(ht[k].weight < min1) {
                min2 = min1; rnode = lnode;  // 原最小下沉
                min1 = ht[k].weight; lnode = k;
            } else if(ht[k].weight < min2) {
                min2 = ht[k].weight; rnode = k;
            }
        }
    }
    ht[i].weight = ht[lnode].weight + ht[rnode].weight;
    ht[i].lchild = lnode; ht[i].rchild = rnode;
    ht[lnode].parent = i; ht[rnode].parent = i;
}
```

### 哈夫曼编码

从叶子向根回溯路径，左分支为 `0`，右分支为 `1`：

```c
// 从叶子 i 出发，沿 parent 指针回溯到根
idx = i; j = n;
while((p = ht[idx].parent) > 0) {
    if(ht[p].lchild == idx) str[--j] = '0';
    else                    str[--j] = '1';
    idx = p;
}
strcpy(book[i].code, &str[j]);
```

⚠️ `huffrelease.h` 第 33 行有运算符优先级 bug：`while(p = ht[idx].parent > 0)` 应为 `while((p = ht[idx].parent) > 0)`，当前写法中 `>` 优先于 `=`，导致 `p` 只会是 0 或 1。

---

## 4️⃣ 泛型动态栈

📌 `stack.h` 实现了一个工程级的泛型栈，亮点很多：

| 特性 | 实现方式 |
|:---|:---|
| **泛型支持** | 通过 `STACK_ELEM_TYPE` 宏定义元素类型，默认 `int` |
| **动态扩容** | `StackEnsureCapacity()` 容量不足时 `realloc` 翻倍 |
| **安全接口** | 所有操作返回 `STACK_OK` / `STACK_ERR`，支持错误检查 |
| **完整 API** | Init / Destroy / Push / Pop / Top / Clear / Swap / IsEmpty / Size |

```c
// 使用示例
Stack s;
StackInit(&s, 0);           // 默认初始容量 16
StackPush(&s, 42);
int val;
StackPop(&s, &val);         // val = 42
StackDestroy(&s);
```

---

## 5️⃣ 图

### 5.1 邻接矩阵 + Dijkstra（成都地铁最短路径）

📌 这是一个**完整的应用项目**：基于成都地铁线路数据，实现高校间最短路径查询。

**数据建模**：
- 9 个站点（含 5 所高校 + 必要换乘站）
- 6 条地铁线路（1/4/6/7/8/18 号线）
- 用位掩码 `stn_mask` 标记每个站点所属线路，支持换乘判断

```c
// 线路位掩码示例
// 火车南站：1号线 | 7号线 | 18号线
static const int stn_mask[2] = {
    (1 << LINE_1) | (1 << LINE_7) | (1 << LINE_18)
};
```

**Dijkstra 实现**：

```c
static int dijkstra(int src, int dst, int path[], int *plen) {
    int dist[MAX_STN], done[MAX_STN], prev[MAX_STN];
    // 初始化
    for(i = 0; i < MAX_STN; i++) {
        dist[i] = INF; done[i] = 0; prev[i] = -1;
    }
    dist[src] = 0;

    for(count = 0; count < MAX_STN; count++) {
        // 1. 找未访问的距离最小节点 u
        u = -1; min_d = INF;
        for(i = 0; i < MAX_STN; i++)
            if(!done[i] && dist[i] < min_d) { min_d = dist[i]; u = i; }

        if(u == -1 || u == dst) break;
        done[u] = 1;

        // 2. 松弛 u 的所有邻接点
        for(v = 0; v < MAX_STN; v++)
            if(!done[v] && G[u][v] < INF && dist[u] + G[u][v] < dist[v]) {
                dist[v] = dist[u] + G[u][v];
                prev[v] = u;
            }
    }

    // 3. 通过 prev 数组回溯构建路径
    cur = dst;
    while(cur != -1) { tmp[len++] = cur; cur = prev[cur]; }
    // 反转得到 src→dst 的路径
}
```

🌟 附加功能：`route_print()` 自动识别换乘站，输出乘坐线路和换乘提示。

### 5.2 邻接表 + DFS/BFS

```c
// 邻接表结构
typedef struct ArcNode {
    int adjvex;
    struct ArcNode *nextarc;
} ArcNode;

typedef struct VNode {
    char data;
    ArcNode *firstarc;
} VNode, AdjList[MAX_VERTEX];
```

| 遍历方式 | 实现 | 特点 |
|:---|:---|:---|
| `DFS()` | 递归 | 沿一条路走到底，回溯 |
| `DFSTraverse()` | DFS 入口 | 处理非连通图（外层循环） |
| `BFSTraverse()` | 队列辅助 | 类似层序遍历，用循环队列 |

⚠️ `mapline.h` 中 BFS 使用了**循环队列**（`front == rear` 判空，`(rear+1) % MAX_VERTEX == front` 判满），这是标准实现。

---

## 6️⃣ 查找

### 6.1 二叉搜索树（BST）

```c
typedef struct bnode {
    int key;
    struct bnode *lchild, *rchild;
} BSTNode, *BSTree;

BSTTree searchBST(BSTree T, int key) {
    if(T == NULL || T->key == key) return T;
    else if(key < T->key) return searchBST(T->lchild, key);
    else return searchBST(T->rchild, key);
}
```

⚠️ `findh.h` 第 1 行有 bug：`#ifdef FINDH_H` 应为 `#ifndef FINDH_H`，否则头文件保护失效。

### 6.2 哈希表（线性探测）

📌 完整实现了哈希表的**构建、插入、查找、ASL 计算**。

**哈希函数**：除留余数法，表长取素数 61

```c
int Hash(char *name) {
    int sum = 0;
    while(*name) sum += (int)(*name++);
    return sum % TABLE_SIZE;  // TABLE_SIZE = 61
}
```

**线性探测插入**：

```c
int InsertHash(HashTable *HT, char *name) {
    addr = Hash(name);
    while(HT->data[addr].status == OCCUPIED) {
        if(strcmp(HT->data[addr].name, name) == 0) return -1;  // 已存在
        addr = (addr + 1) % TABLE_SIZE;  // 线性探测
        if(addr == start) return -1;      // 表满
    }
    // 插入到空位
}
```

**平均查找长度（ASL）计算**：

```c
// 对每个已存元素模拟查找，统计查找长度
float CalcASL(HashTable HT) {
    for(i = 0; i < TABLE_SIZE; i++) {
        if(HT.data[i].status == OCCUPIED) {
            addr = Hash(HT.data[i].name);
            len = 1;
            while(strcmp(HT.data[addr].name, HT.data[i].name) != 0) {
                addr = (addr + 1) % TABLE_SIZE;
                len++;
            }
            totalLen += len; found++;
        }
    }
    return (float)totalLen / found;
}
```

---

## 7️⃣ 排序

### 堆排序

```c
// 筛选调整：以 a[k] 为根的子树调整为大顶堆
static void sift(int a[], int k, int m) {
    a[0] = a[k];  // 暂存根节点
    int j = 2*k;   // j 指向左孩子
    while(j <= m) {
        if(j < m && a[j] < a[j+1]) j++;  // 选较大的孩子
        if(a[0] >= a[j]) break;           // 根已最大，结束
        a[k] = a[j]; k = j; j = 2*k;     // 孩子上移
    }
    a[k] = a[0];  // 插入到最终位置
}

// 建堆：从最后一个非叶子节点 n/2 开始，向前逐个筛选
static void create_heap(int a[], int n) {
    for(int i = n/2; i > 0; i--)
        sift(a, i, n);
}

// 排序：每次将堆顶（最大值）交换到末尾，再调整堆
static void heap_sort(int a[], int n) {
    create_heap(a, n);
    for(int i = n; i > 1; i--) {
        swap(&a[1], &a[i]);    // 堆顶 → 末尾
        sift(a, 1, i-1);       // 对剩余元素调整
    }
}
```

💡 数据从 `a[1]` 开始，`a[0]` 用作暂存单元——这是堆排序的经典数组布局。

### 快速排序

```c
static int partition(int a[], int low, int high) {
    int pivot = a[low];       // 选第一个元素为基准
    while(low < high) {
        while(low < high && a[high] >= pivot) high--;
        swap(&a[low], &a[high]);
        while(low < high && a[low] <= pivot) low++;
        swap(&a[low], &a[high]);
    }
    a[low] = pivot;
    return low;
}

static void quick_sort(int a[], int low, int high) {
    if(low < high) {
        int pivot = partition(a, low, high);
        quick_sort(a, low, pivot-1);
        quick_sort(a, pivot+1, high);
    }
}
```

### 简单选择排序

```c
static void selection_sort(int a[], int n) {
    for(int i = 0; i < n-1; i++) {
        int min_index = i;
        for(int j = i+1; j < n; j++)
            if(a[j] < a[min_index]) min_index = j;
        swap(&a[i], &a[min_index]);
    }
}
```

---

## 🐛 已知 Bug 汇总

| 文件 | 行号 | 问题 | 修复方案 |
|:---|:---:|:---|:---|
| `matrixx.h` | 86 | `MaxSize` 未定义（应为 `MaxSizex`） | 统一宏名 |
| `huffrelease.h` | 33 | `while(p = ht[idx].parent > 0)` 运算符优先级错误 | 改为 `while((p = ht[idx].parent) > 0)` |
| `findh.h` | 1 | `#ifdef` 应为 `#ifndef` | 头文件保护方向反了 |
| `findh.h` | 16 | `BSTTree` 未定义（应为 `BSTree`） | 类型名拼写错误 |

---

> 📎 **相关笔记**：[[程序与算法设计]] | [[成都地铁交通简易]]
