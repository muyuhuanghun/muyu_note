import json

cells = []

# ============================================================
# 一、真题分析
# ============================================================
analysis = r"""
## 一、真题分析

### 题目来源与分布
- 24年真题：3轮（第一轮、第二轮、第三轮），共15道题
- 23年真题：3轮（第一轮、第二轮、第三轮），共15道题
- 每轮5道题，题型基本固定

### 考察知识点统计（共30道题）

| 知识点 | 出现次数 | 占比 |
|--------|---------|------|
| 图的最小生成树（Prim/Kruskal） | 6次 | 20% |
| 图的关键路径（AOE网） | 6次 | 20% |
| 图的入度/出度计算 | 5次 | 17% |
| 二叉树遍历（先序/层序/后序） | 5次 | 17% |
| 线性表操作（顺序表/链表） | 5次 | 17% |
| 排序算法（选择/插入） | 2次 | 7% |
| 哈希表 | 1次 | 3% |

### 题目难度分析
1. **基础题（约40%）**：线性表操作、入度出度计算、排序算法
   - 需要掌握基本数据结构定义和简单算法实现
   - 代码量适中，逻辑直接

2. **中等题（约35%）**：二叉树非递归遍历、哈希表插入
   - 需要理解栈/队列的应用场景
   - 代码需要处理边界条件

3. **较难题（约25%）**：最小生成树手算、关键路径计算
   - 需要理解图论算法的核心步骤
   - 手算时容易出错，需要仔细演算

### 重点考察方向
1. **图论**是绝对重点（最小生成树+关键路径+度数 = 57%）
2. **二叉树遍历**是核心考点，尤其是非递归实现
3. **线性表操作**是基础，每年必考
4. **排序算法**偶尔出现，但需要掌握基本实现

### 备考建议
1. 重点掌握Prim和Kruskal算法的手算过程
2. 熟练掌握关键路径的计算步骤（求最早/最晚发生时间）
3. 熟练实现二叉树的非递归先序遍历
4. 掌握顺序表和链表的基本操作
5. 了解简单选择排序和直接插入排序的实现
"""

cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': [analysis]
})

# ============================================================
# 二、模拟卷一
# ============================================================

mock1_title = r"""
## 二、模拟卷一

### 题目一：顺序表区间逆转（线性表）
**题目**：给定一个顺序表 L，实现函数将下标从 start 到 end（包含两端）的元素就地逆置。要求时间复杂度 O(n)，空间复杂度 O(1)。

函数声明：
```c
void reverse(SqList *L, int start, int end);
```

### 题目二：非递归后序遍历二叉树（树）
**题目**：使用非递归方法实现二叉树的后序遍历，并返回遍历结果数组。要求使用栈辅助实现。

函数声明：
```c
void postOrder(BiTree T, int result[], int *count);
```

### 题目三：Kruskal算法求最小生成树（图）
**题目**：给定一个无向连通图的边集，使用Kruskal算法求最小生成树，输出按权值从小到大排序的边集。

函数声明：
```c
void kruskal(Edge edges[], int n, int e, Edge result[], int *count);
```

### 题目四：计算有向图各顶点的入度（图）
**题目**：给定一个有向图的邻接矩阵，计算每个顶点的入度并存入数组。

函数声明：
```c
void inDegree(int adj[][MAXVEX], int n, int degree[]);
```

### 题目五：直接插入排序（排序）
**题目**：实现直接插入排序算法，将数组 arr 中的 n 个元素按升序排列。

函数声明：
```c
void insertSort(int arr[], int n);
```
"""

cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': [mock1_title]
})

# --- Q1 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷一 题目一 思路解析

**核心思路**：双指针交换法

1. 用两个指针分别指向 start 和 end 位置
2. 交换两个指针所指的元素
3. 左指针右移，右指针左移
4. 重复直到两指针相遇或交错

**关键点**：
- 注意 start 和 end 的合法性检查
- 交换时使用临时变量
- 循环条件是 left < right
"""]})

# --- Q1 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷一 题目一：顺序表区间逆转

MAXSIZE = 100

class SqList:
    def __init__(self):
        self.data = [0] * MAXSIZE
        self.length = 0

def swap(a, b):
    return b, a

# ===== 请补全以下函数 =====
def reverse(L, start, end):
    if start < 0 or end >= L.length or start >= end:
        return
    left, right = start, end
    while left < right:
        L.data[left], L.data[right] = L.data[right], L.data[left]
        left += 1
        right -= 1
# ===== 函数补全结束 =====

# 测试代码
L = SqList()
L.data = [1, 2, 3, 4, 5, 6, 7]
L.length = 7
print("逆转前:", L.data[:L.length])
reverse(L, 1, 5)
print("逆转后:", L.data[:L.length])
# 预期输出: [1, 6, 5, 4, 3, 2, 7]
"""]})

# --- Q2 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷一 题目二 思路解析

**核心思路**：利用栈模拟递归实现后序遍历

后序遍历顺序：左 -> 右 -> 根

方法：
1. 使用一个栈进行遍历
2. 记录上一次访问的节点 visited
3. 如果当前节点的右孩子为空或者右孩子已经被访问，则访问当前节点
4. 否则将右孩子压栈，继续向左走

**关键点**：
- 需要记录 visited 节点以判断右子树是否已访问
- 栈中保存待处理的节点
- 循环条件：current != None 或 stack 非空
"""]})

# --- Q2 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷一 题目二：非递归后序遍历二叉树

class BiTreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def postOrder(T, result, count):
    \"\"\"非递归后序遍历二叉树\"\"\"
    if T is None:
        return
    stack = []
    visited = None
    current = T
    count[0] = 0

    while current is not None or len(stack) > 0:
        while current is not None:
            stack.append(current)
            current = current.left
        peek_node = stack[-1]
        if peek_node.right is None or peek_node.right == visited:
            result[count[0]] = peek_node.val
            count[0] += 1
            visited = peek_node
            stack.pop()
        else:
            current = peek_node.right

# 测试代码
#     1
#    / \\
#   2   3
#  / \\
# 4   5
root = BiTreeNode(1)
root.left = BiTreeNode(2)
root.right = BiTreeNode(3)
root.left.left = BiTreeNode(4)
root.left.right = BiTreeNode(5)

result = [0] * 10
count = [0]
postOrder(root, result, count)
print("后序遍历结果:", result[:count[0]])
# 预期输出: [4, 5, 2, 3, 1]
"""]})

# --- Q3 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷一 题目三 思路解析

**核心思路**：贪心算法 + 并查集

1. 将所有边按权值从小到大排序
2. 初始化并查集，每个顶点自成一个集合
3. 依次选取权值最小的边：
   - 如果该边的两个顶点属于不同集合，则加入MST，并合并两个集合
   - 如果属于同一集合，则跳过（会形成环）
4. 重复直到选取了 n-1 条边（n为顶点数）

**关键点**：
- 并查集的 Find 操作使用路径压缩优化
- Union 操作判断是否在同一集合
- 边的排序使用 sort
"""]})

# --- Q3 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷一 题目三：Kruskal算法求最小生成树

class Edge:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight

# ===== 请补全以下并查集相关函数 =====
parent = []

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    root_x = find(x)
    root_y = find(y)
    if root_x != root_y:
        parent[root_x] = root_y
        return True
    return False
# ===== 函数补全结束 =====

def kruskal(edges, n, e, result, count):
    global parent
    parent = list(range(n))
    edges.sort(key=lambda x: x.weight)
    count[0] = 0
    for i in range(e):
        if count[0] == n - 1:
            break
        if union(edges[i].u, edges[i].v):
            result[count[0]] = edges[i]
            count[0] += 1

# 测试代码
edges = [
    Edge(0, 1, 2),
    Edge(0, 2, 3),
    Edge(1, 2, 1),
    Edge(1, 3, 4),
    Edge(2, 3, 5),
    Edge(3, 4, 6)
]
n = 5
e = 6
result = [None] * 10
count = [0]
kruskal(edges, n, e, result, count)
print("Kruskal最小生成树边集:")
for i in range(count[0]):
    print(f"({result[i].u}-{result[i].v}, 权值={result[i].weight})")
# 预期输出: (1-2,1), (0-1,2), (0-2,3), (1-3,4) 或等价结果
"""]})

# --- Q4 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷一 题目四 思路解析

**核心思路**：遍历邻接矩阵的每一列

1. 有向图的邻接矩阵中，adj[i][j] = 1 表示从顶点 i 到顶点 j 有一条有向边
2. 顶点 j 的入度 = 所有 adj[i][j] = 1 的个数（即第 j 列中1的个数）
3. 遍历每一列，统计每列中1的个数即可

**时间复杂度**：O(n^2)
**空间复杂度**：O(1)（不计输出数组）
"""]})

# --- Q4 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷一 题目四：计算有向图各顶点的入度

def inDegree(adj, n, degree):
    \"\"\"
    计算有向图各顶点的入度
    adj: 邻接矩阵
    n: 顶点数
    degree: 存储入度的数组
    \"\"\"
    # ===== 请补全以下代码 =====
    for j in range(n):
        degree[j] = 0
        for i in range(n):
            if adj[i][j] == 1:
                degree[j] += 1
    # ===== 代码补全结束 =====

# 测试代码
adj = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 1],
    [0, 0, 0, 0]
]
n = 4
degree = [0] * n
inDegree(adj, n, degree)
print("各顶点入度:", degree)
# 预期输出: [1, 1, 1, 1]
"""]})

# --- Q5 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷一 题目五 思路解析

**核心思路**：从第二个元素开始，依次将当前元素插入到前面已排序的部分

1. 从 i = 1 开始（假设第一个元素已排序）
2. 将 arr[i] 存入临时变量 key
3. 将 key 与前面已排序的元素从后往前比较
4. 如果前面的元素比 key 大，则后移一位
5. 找到 key 的正确位置后插入
6. 重复直到所有元素处理完

**时间复杂度**：最坏 O(n^2)，最好 O(n)
**空间复杂度**：O(1)
**稳定性**：稳定排序
"""]})

# --- Q5 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷一 题目五：直接插入排序

def insertSort(arr, n):
    \"\"\"
    直接插入排序
    arr: 待排序数组
    n: 数组长度
    \"\"\"
    # ===== 请补全以下代码 =====
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    # ===== 代码补全结束 =====

# 测试代码
arr = [5, 2, 4, 6, 1, 3]
n = len(arr)
print("排序前:", arr)
insertSort(arr, n)
print("排序后:", arr)
# 预期输出: [1, 2, 3, 4, 5, 6]
"""]})

# ============================================================
# 三、模拟卷二
# ============================================================

mock2_title = r"""
## 三、模拟卷二

### 题目一：链表逆序（线性表）
**题目**：给定一个单链表，使用非递归方法将链表就地逆置，并返回新的头节点。

函数声明：
```c
LinkNode* reverseList(LinkNode *head);
```

### 题目二：层序遍历二叉树（树）
**题目**：实现二叉树的层序遍历，返回每一层的节点值（二维数组形式）。

函数声明：
```c
void levelOrder(BiTree T, int result[][MAXSIZE], int *levelCount, int levelSize[]);
```

### 题目三：Prim算法求最小生成树（图）
**题目**：给定一个无向连通图的邻接矩阵，使用Prim算法从顶点0开始求最小生成树，输出边集。

函数声明：
```c
void prim(int adj[][MAXVEX], int n, Edge result[], int *count);
```

### 题目四：拓扑排序（图）
**题目**：对一个有向无环图进行拓扑排序，返回排序结果。

函数声明：
```c
void topologicalSort(int adj[][MAXVEX], int n, int result[], int *count);
```

### 题目五：简单选择排序（排序）
**题目**：实现简单选择排序算法，将数组 arr 中的 n 个元素按升序排列。

函数声明：
```c
void selectSort(int arr[], int n);
```
"""

cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': [mock2_title]
})

# --- Q1 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷二 题目一 思路解析

**核心思路**：三指针法逆置链表

1. 使用三个指针：prev（前一个节点）、curr（当前节点）、next_node（下一个节点）
2. 初始时 prev = None，curr = head
3. 遍历链表：
   - 先保存 curr.next 到 next_node
   - 将 curr.next 指向 prev（反转）
   - 然后 prev = curr，curr = next_node
4. 最后 prev 就是新的头节点

**关键点**：
- 需要保存 next 指针，否则断链后无法继续
- 循环条件是 curr != None
- 最后返回 prev
"""]})

# --- Q1 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷二 题目一：链表逆序

class LinkNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head):
    \"\"\"非递归逆置单链表\"\"\"
    # ===== 请补全以下代码 =====
    prev = None
    curr = head
    while curr is not None:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
    # ===== 代码补全结束 =====

def printList(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

# 测试代码
head = LinkNode(1)
head.next = LinkNode(2)
head.next.next = LinkNode(3)
head.next.next.next = LinkNode(4)
head.next.next.next.next = LinkNode(5)

print("逆置前:", printList(head))
head = reverseList(head)
print("逆置后:", printList(head))
# 预期输出: [5, 4, 3, 2, 1]
"""]})

# --- Q2 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷二 题目二 思路解析

**核心思路**：使用队列实现层序遍历

1. 将根节点入队
2. 当队列不为空时：
   - 记录当前层的节点数 level_size
   - 依次出队该层所有节点，记录值
   - 将出队节点的左右孩子依次入队
3. 重复直到队列为空

**关键点**：
- 需要记录每一层的节点数，以便区分层级
- 使用队列 FIFO 特性保证层序访问
"""]})

# --- Q2 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷二 题目二：层序遍历二叉树

from collections import deque

class BiTreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def levelOrder(T, result, levelCount, levelSize):
    if T is None:
        return
    queue = deque([T])
    levelCount[0] = 0
    while queue:
        level_size = len(queue)
        levelSize[levelCount[0]] = level_size
        for i in range(level_size):
            node = queue.popleft()
            result[levelCount[0]][i] = node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levelCount[0] += 1

# 测试代码
#     1
#    / \\
#   2   3
#  / \\   \\
# 4   5   6
root = BiTreeNode(1)
root.left = BiTreeNode(2)
root.right = BiTreeNode(3)
root.left.left = BiTreeNode(4)
root.left.right = BiTreeNode(5)
root.right.right = BiTreeNode(6)

result = [[0]*10 for _ in range(10)]
levelCount = [0]
levelSize = [0]*10
levelOrder(root, result, levelCount, levelSize)

print("层序遍历结果:")
for i in range(levelCount[0]):
    print(f"第{i+1}层:", result[i][:levelSize[i]])
# 预期输出:
# 第1层: [1]
# 第2层: [2, 3]
# 第3层: [4, 5, 6]
"""]})

# --- Q3 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷二 题目三 思路解析

**核心思路**：贪心算法，从一个顶点开始扩展

1. 维护两个数组：lowcost（到MST的最小代价）和 closest（最近的MST顶点）
2. 初始时，lowcost[0] = 0，其他为邻接矩阵中的值
3. 重复 n-1 次：
   - 找到 lowcost 中最小的顶点 k（不在MST中）
   - 将 k 加入MST，记录边 (closest[k], k)
   - 更新其他顶点的 lowcost 和 closest
4. 最终得到 n-1 条边构成MST

**时间复杂度**：O(n^2)
"""]})

# --- Q3 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷二 题目三：Prim算法求最小生成树

INF = 9999

class Edge:
    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight

def prim(adj, n, result, count):
    lowcost = [0] * n
    closest = [0] * n
    visited = [False] * n

    for i in range(1, n):
        lowcost[i] = adj[0][i]
        closest[i] = 0

    lowcost[0] = 0
    visited[0] = True
    count[0] = 0

    # ===== 请补全以下代码 =====
    for i in range(1, n):
        min_val = INF
        k = -1
        for j in range(n):
            if not visited[j] and lowcost[j] < min_val:
                min_val = lowcost[j]
                k = j
        if k == -1:
            break
        visited[k] = True
        result[count[0]] = Edge(closest[k], k, min_val)
        count[0] += 1
        for j in range(n):
            if not visited[j] and adj[k][j] < lowcost[j]:
                lowcost[j] = adj[k][j]
                closest[j] = k
    # ===== 代码补全结束 =====

# 测试代码
adj = [
    [0, 2, 3, INF, INF],
    [2, 0, 1, 4, INF],
    [3, 1, 0, 5, INF],
    [INF, 4, 5, 0, 6],
    [INF, INF, INF, 6, 0]
]
n = 5
result = [None] * 10
count = [0]
prim(adj, n, result, count)
print("Prim最小生成树边集:")
for i in range(count[0]):
    print(f"({result[i].u}-{result[i].v}, 权值={result[i].weight})")
# 预期输出: (0-1,2), (1-2,1), (1-3,4), (3-4,6) 或等价结果
"""]})

# --- Q4 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷二 题目四 思路解析

**核心思路**：基于入度的BFS

1. 统计所有顶点的入度
2. 将所有入度为0的顶点入队
3. 当队列不为空时：
   - 出队一个顶点，加入结果
   - 将该顶点的所有邻接顶点入度减1
   - 如果某邻接顶点入度变为0，则入队
4. 如果结果中顶点数等于总顶点数，则排序成功

**关键点**：
- 需要先统计入度
- 使用队列存储入度为0的顶点
- 时间复杂度 O(n+e)
"""]})

# --- Q4 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷二 题目四：拓扑排序

from collections import deque

def topologicalSort(adj, n, result, count):
    in_deg = [0] * n
    queue = deque()
    count[0] = 0

    # ===== 请补全以下代码 =====
    for j in range(n):
        for i in range(n):
            if adj[i][j] == 1:
                in_deg[j] += 1

    for i in range(n):
        if in_deg[i] == 0:
            queue.append(i)

    while queue:
        v = queue.popleft()
        result[count[0]] = v
        count[0] += 1
        for j in range(n):
            if adj[v][j] == 1:
                in_deg[j] -= 1
                if in_deg[j] == 0:
                    queue.append(j)
    # ===== 代码补全结束 =====

# 测试代码
adj = [
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
]
n = 4
result = [0] * n
count = [0]
topologicalSort(adj, n, result, count)
print("拓扑排序结果:", result[:count[0]])
# 预期输出: [0, 1, 2, 3] 或 [0, 2, 1, 3]
"""]})

# --- Q5 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷二 题目五 思路解析

**核心思路**：每轮从未排序部分选出最小元素，放到已排序部分末尾

1. 从 i = 0 开始
2. 在 arr[i..n-1] 中找到最小元素的下标 min_idx
3. 将 arr[i] 与 arr[min_idx] 交换
4. i++，重复直到 i = n-1

**时间复杂度**：始终 O(n^2)
**空间复杂度**：O(1)
**不稳定排序**（因为有远距离交换）
"""]})

# --- Q5 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷二 题目五：简单选择排序

def selectSort(arr, n):
    \"\"\"
    简单选择排序
    arr: 待排序数组
    n: 数组长度
    \"\"\"
    # ===== 请补全以下代码 =====
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    # ===== 代码补全结束 =====

# 测试代码
arr = [5, 2, 4, 6, 1, 3]
n = len(arr)
print("排序前:", arr)
selectSort(arr, n)
print("排序后:", arr)
# 预期输出: [1, 2, 3, 4, 5, 6]
"""]})

# ============================================================
# 四、模拟卷三
# ============================================================

mock3_title = r"""
## 四、模拟卷三

### 题目一：顺序表删除重复元素（线性表）
**题目**：给定一个有序顺序表，删除其中的重复元素，使表中每个元素只出现一次，返回新表长。

函数声明：
```c
int removeDuplicates(SqList *L);
```

### 题目二：非递归中序遍历二叉树（树）
**题目**：使用非递归方法实现二叉树的中序遍历，并将结果存入数组。

函数声明：
```c
void inOrder(BiTree T, int result[], int *count);
```

### 题目三：关键路径计算（图）
**题目**：给定一个AOE网（有向无环图），计算关键路径和各顶点的最早发生时间。

函数声明：
```c
void criticalPath(int adj[][MAXVEX], int n, int ve[], int vl[]);
```

### 题目四：邻接表求顶点出度（图）
**题目**：给定一个图的邻接表表示，计算每个顶点的出度。

函数声明：
```c
void outDegree(AdjList GL, int n, int degree[]);
```

### 题目五：冒泡排序（排序）
**题目**：实现冒泡排序算法，将数组 arr 中的 n 个元素按升序排列。

函数声明：
```c
void bubbleSort(int arr[], int n);
```
"""

cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': [mock3_title]
})

# --- Q1 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷三 题目一 思路解析

**核心思路**：双指针法

1. 使用两个指针：i（慢指针）指向已去重部分的末尾，j（快指针）遍历整个数组
2. 由于数组有序，重复元素一定相邻
3. 当 arr[j] != arr[i] 时，将 arr[j] 复制到 arr[i+1]
4. 最终 i+1 就是新表长

**时间复杂度**：O(n)
**空间复杂度**：O(1)
"""]})

# --- Q1 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷三 题目一：顺序表删除重复元素

MAXSIZE = 100

class SqList:
    def __init__(self):
        self.data = [0] * MAXSIZE
        self.length = 0

def removeDuplicates(L):
    if L.length == 0:
        return 0
    # ===== 请补全以下代码 =====
    i = 0
    for j in range(1, L.length):
        if L.data[j] != L.data[i]:
            i += 1
            L.data[i] = L.data[j]
    L.length = i + 1
    return L.length
    # ===== 代码补全结束 =====

# 测试代码
L = SqList()
L.data = [1, 1, 2, 3, 3, 3, 4, 5, 5]
L.length = 9
print("去重前:", L.data[:L.length])
new_len = removeDuplicates(L)
print("去重后:", L.data[:new_len])
print("新表长:", new_len)
# 预期输出: [1, 2, 3, 4, 5]，新表长5
"""]})

# --- Q2 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷三 题目二 思路解析

**核心思路**：利用栈模拟递归

1. 初始化一个空栈，当前节点指向根节点
2. 当当前节点不为空或栈不为空时：
   - 一路向左走，将经过的节点全部压栈
   - 当无法向左走时，弹出栈顶节点，访问它
   - 转向右子树
3. 中序遍历顺序：左 -> 根 -> 右

**关键点**：
- 先一路向左，再弹出访问，再转向右子树
- 栈用于保存待访问的父节点
"""]})

# --- Q2 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷三 题目二：非递归中序遍历二叉树

class BiTreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inOrder(T, result, count):
    stack = []
    current = T
    count[0] = 0

    # ===== 请补全以下代码 =====
    while current is not None or len(stack) > 0:
        while current is not None:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result[count[0]] = current.val
        count[0] += 1
        current = current.right
    # ===== 代码补全结束 =====

# 测试代码
#     1
#    / \\
#   2   3
#  / \\
# 4   5
root = BiTreeNode(1)
root.left = BiTreeNode(2)
root.right = BiTreeNode(3)
root.left.left = BiTreeNode(4)
root.left.right = BiTreeNode(5)

result = [0] * 10
count = [0]
inOrder(root, result, count)
print("中序遍历结果:", result[:count[0]])
# 预期输出: [4, 2, 5, 1, 3]
"""]})

# --- Q3 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷三 题目三 思路解析

**核心思路**：求AOE网的关键路径

1. **拓扑排序**求最早发生时间 ve[]：
   - ve[源点] = 0
   - ve[j] = max(ve[i] + w(i,j))，其中 (i,j) 是所有指向 j 的边

2. **逆拓扑排序**求最晚发生时间 vl[]：
   - vl[汇点] = ve[汇点]
   - vl[i] = min(vl[j] - w(i,j))，其中 (i,j) 是所有从 i 出发的边

3. **关键路径**：ve[i] == vl[i] 的顶点

**时间复杂度**：O(n+e)
"""]})

# --- Q3 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷三 题目三：关键路径计算

from collections import deque

def topologicalOrder(adj, n):
    in_deg = [0] * n
    for j in range(n):
        for i in range(n):
            if adj[i][j] > 0:
                in_deg[j] += 1
    queue = deque()
    for i in range(n):
        if in_deg[i] == 0:
            queue.append(i)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for j in range(n):
            if adj[v][j] > 0:
                in_deg[j] -= 1
                if in_deg[j] == 0:
                    queue.append(j)
    return order

def criticalPath(adj, n, ve, vl):
    order = topologicalOrder(adj, n)
    for i in range(n):
        ve[i] = 0

    # ===== 请补全以下代码 =====
    for i in order:
        for j in range(n):
            if adj[i][j] > 0:
                if ve[i] + adj[i][j] > ve[j]:
                    ve[j] = ve[i] + adj[i][j]

    for i in range(n):
        vl[i] = ve[order[-1]]

    for i in reversed(order):
        for j in range(n):
            if adj[i][j] > 0:
                if vl[j] - adj[i][j] < vl[i]:
                    vl[i] = vl[j] - adj[i][j]

    print("关键路径顶点:")
    for i in range(n):
        if ve[i] == vl[i]:
            print(f"顶点 {i}: ve={ve[i]}, vl={vl[i]}")
    # ===== 代码补全结束 =====

# 测试代码
adj = [
    [0, 3, 4, 0, 0, 0],
    [0, 0, 0, 5, 6, 0],
    [0, 0, 0, 8, 0, 7],
    [0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0]
]
n = 6
ve = [0] * n
vl = [0] * n
criticalPath(adj, n, ve, vl)
print("\\n最早发生时间 ve:", ve)
print("最晚发生时间 vl:", vl)
"""]})

# --- Q4 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷三 题目四 思路解析

**核心思路**：遍历邻接表的每个链表

1. 邻接表中每个顶点对应一个链表
2. 链表中的节点数就是该顶点的出度
3. 遍历每个顶点的链表，计数即可

**时间复杂度**：O(n+e)
**空间复杂度**：O(1)
"""]})

# --- Q4 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷三 题目四：邻接表求顶点出度

class ArcNode:
    def __init__(self, adjvex=0, next=None):
        self.adjvex = adjvex
        self.next = next

class VNode:
    def __init__(self, data=0, firstarc=None):
        self.data = data
        self.firstarc = firstarc

def outDegree(GL, n, degree):
    # ===== 请补全以下代码 =====
    for i in range(n):
        count = 0
        p = GL[i].firstarc
        while p is not None:
            count += 1
            p = p.next
        degree[i] = count
    # ===== 代码补全结束 =====

# 测试代码
GL = [VNode(i) for i in range(3)]
GL[0].firstarc = ArcNode(1)
GL[0].firstarc.next = ArcNode(2)
GL[1].firstarc = ArcNode(2)
GL[2].firstarc = ArcNode(0)

n = 3
degree = [0] * n
outDegree(GL, n, degree)
print("各顶点出度:", degree)
# 预期输出: [2, 1, 1]
"""]})

# --- Q5 思路 ---
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': ["""
### 模拟卷三 题目五 思路解析

**核心思路**：反复比较相邻元素，逆序则交换

1. 从 i = 0 到 n-2：
   - 从 j = 0 到 n-i-2：
     - 如果 arr[j] > arr[j+1]，交换它们
2. 每轮将最大的元素"冒泡"到末尾
3. 可以设置标志位优化：如果某轮没有交换，说明已有序，提前退出

**时间复杂度**：最坏 O(n^2)，最好 O(n)
**空间复杂度**：O(1)
**稳定排序**
"""]})

# --- Q5 代码 ---
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': ["""
# 模拟卷三 题目五：冒泡排序

def bubbleSort(arr, n):
    \"\"\"
    冒泡排序
    arr: 待排序数组
    n: 数组长度
    \"\"\"
    # ===== 请补全以下代码 =====
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    # ===== 代码补全结束 =====

# 测试代码
arr = [5, 2, 4, 6, 1, 3]
n = len(arr)
print("排序前:", arr)
bubbleSort(arr, n)
print("排序后:", arr)
# 预期输出: [1, 2, 3, 4, 5, 6]
"""]})

# ============================================================
# 五、总结
# ============================================================

summary = r"""
## 五、总结

### 三份模拟卷知识点覆盖

| 模拟卷 | 线性表 | 树 | 图 | 排序 |
|--------|--------|-----|-----|------|
| 模拟卷一 | 顺序表区间逆转 | 非递归后序遍历 | Kruskal算法、入度计算 | 直接插入排序 |
| 模拟卷二 | 链表逆序 | 层序遍历 | Prim算法、拓扑排序 | 简单选择排序 |
| 模拟卷三 | 删除重复元素 | 非递归中序遍历 | 关键路径、出度计算 | 冒泡排序 |

### 备考重点
1. **图论算法**：Prim、Kruskal、关键路径、拓扑排序（必考）
2. **二叉树遍历**：先序/中序/后序的非递归实现、层序遍历（高频）
3. **线性表操作**：顺序表和链表的基本操作（基础必考）
4. **排序算法**：插入排序、选择排序、冒泡排序（偶尔出现）

### 建议
- 先理解算法原理，再动手写代码
- 注意边界条件和特殊情况处理
- 手算练习很重要，尤其是图论算法
- 代码要规范，注意变量命名和注释
"""

cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': [summary]
})

# ============================================================
# 写入文件
# ============================================================
notebook = {
    'cells': cells,
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.8.0'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 4
}

with open('数据结构模拟.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print('Notebook created successfully!')
