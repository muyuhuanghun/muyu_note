# 程序设计与算法基础 II — 综合复习

> 以历年机考真题为骨干，按知识点整理。每道题附解题思路和核心代码，完整解答见 `复习用/from fuxi/` 下对应文件。

---

## 一、线性表

### 1.1 核心操作模板

**顺序表插入**（从后往前移）：
```c
void seq_insert(SeqList *L, int pos, int val) {
    for (int i = L->last; i >= pos; i--)
        L->elem[i + 1] = L->elem[i];  // 后移一位
    L->elem[pos] = val;
    L->last++;
}
```

**顺序表删除**（从前往后覆盖）：
```c
void seq_delete(SeqList *L, int pos) {
    for (int i = pos; i < L->last; i++)
        L->elem[i] = L->elem[i + 1];  // 前移一位
    L->last--;
}
```

**链表头插法**（结果逆序）：
```c
node* build_list_head(int arr[], int n) {
    node *head = NULL;
    for (int i = 0; i < n; i++) {
        node *new = malloc(sizeof(node));
        new->data = arr[i];
        new->next = head;  // 新结点指向原链表头
        head = new;
    }
    return head;
}
```

**链表尾插法**（结果正序）：
```c
node* build_list_tail(int arr[], int n) {
    node dummy;  // 哨兵结点，简化头结点处理
    node *tail = &dummy;
    for (int i = 0; i < n; i++) {
        node *new = malloc(sizeof(node));
        new->data = arr[i];
        new->next = NULL;
        tail->next = new;
        tail = new;
    }
    return dummy.next;
}
```

### 1.2 真题

**真题 160：合并顺序表** — 归并两个非递减顺序表
- 解题思路：双指针 i/j 分别扫描 LA/LB，比较后逐个放入 LC，最后处理剩余
- 核心：`if (LA->elem[i] < LB->elem[j]) LC->elem[k++] = LA->elem[i++];`
- 完整解答见 → [[160 合并顺序表]]

**真题 176：整除移除** — 移除顺序表中能被 f 整除的元素
- 解题思路：双指针法，i 扫描、j 记录保留位置，O(n) 时间 O(1) 空间
- 核心：`if (L->elem[i] % f != 0) L->elem[j++] = L->elem[i];`
- 完整解答见 → [[176 整除移除]]

**真题 177：共享结点** — 求两个链表共享结点数量
- 解题思路：(1) 求两链表长度 (2) 长链表先走差值步 (3) 同步走找到交汇点 (4) 从交汇点数到尾部
- 核心技巧：**求差 → 对齐 → 同步走**
- 完整解答见 → [[177 共享结点]]

**真题 197：保留线性表中偶数** — 双指针筛选
- 解题思路：和 176 同一双指针模式，条件改为 `% 2 == 0`
- 完整解答见 → [[197 保留线性表中偶数]]

**真题 201：合并有序数组** — 归并两个有序数组到第三个数组
- 解题思路：和 160 完全一样的归并思路，区别在于用 `const int *` 和独立的 lena/lenb
- 完整解答见 → [[201 合并有序数组]]

### 1.3 套路总结

线性表题三大套路：
1. **双指针** — 顺序表删除/筛选、链表倒数查找，O(n) 时间 O(1) 空间
2. **归并** — 两个有序表合并，O(n+m)
3. **求差+对齐** — 链表交汇点/共享结点，先求长度差再同步走

---

## 二、栈与队列

### 2.1 核心操作模板

**非递归先序遍历**（高频考题）：
```c
void preorder(BiTree root) {
    Stack S;
    init_stack(&S);
    push(&S, root);
    while (!is_empty(&S)) {
        BiTNode *node;
        pop(&S, &node);
        visit(node);
        // ⚠️ 先右后左入栈！栈是后进先出，左后入 = 左先出 = 先访问左子树
        if (node->right) push(&S, node->right);
        if (node->left) push(&S, node->left);
    }
}
```

**非递归中序遍历**：
```c
void inorder(BiTree root) {
    Stack S;
    init_stack(&S);
    BiTNode *curr = root;
    while (curr || !is_empty(&S)) {
        while (curr) {           // 一路向左，全部入栈
            push(&S, curr);
            curr = curr->left;
        }
        pop(&S, &curr);          // 弹出 → 访问
        visit(curr);
        curr = curr->right;      // 转向右子树
    }
}
```

### 2.2 真题

**真题 113：循环链表表示队列** — 带头结点循环链表，只设尾指针
- 解题思路：头结点是哨兵（不存数据），`LQ->next == LQ` 表示空队列
- init：创建头结点，`next` 指向自己
- enter：找队尾 O(n)，尾插新结点，新结点 `next` 指向头结点
- leave：删除 `head->next`（队首），注意释放内存
- 完整解答见 → [[113 循环链表表示队列]]

**真题 120/198：非递归先序遍历** — 栈模拟递归
- 解题思路：递归的"回溯"本质就是栈的 LIFO。先右后左入栈，保证左子树先被访问
- 120 和 198 区别仅在数据结构定义（BiTNode vs bitnode，tag 类型不同）
- 完整解答见 → [[120 非递归先序遍历]]、[[198 非递归先序遍历]]

**真题 178：反转字符串** — 递归转栈
- 解题思路：递归版本先读完再回溯输出 = 天然逆序。栈版本：全部入栈再全部出栈
- 核心：递归回溯 = 栈的 LIFO
- 完整解答见 → [[178 反转字符串]]

### 2.3 套路总结

栈和队列三大考法：
1. **栈模拟递归** — 非递归遍历、递归转非递归。关键：理解 LIFO = 回溯
2. **表达式求值** — 后缀表达式：数字入栈，遇运算符弹两个算
3. **队列实现** — 循环链表队列判空条件、层次遍历用队列

---

## 三、树与二叉树

### 3.1 核心操作模板

**层序遍历**（队列实现）：
```c
void level_order(BiTree root) {
    BiTNode *queue[100];
    int head = 0, tail = 0;
    queue[head++] = root;
    while (head > tail) {
        BiTNode *curr = queue[tail++];
        visit(curr);
        if (curr->left) queue[head++] = curr->left;
        if (curr->right) queue[head++] = curr->right;
    }
}
```

**BST 插入**：
```c
void bst_insert(node *root, int value) {
    if (value > root->data) {
        if (!root->right) {
            root->right = new_node(value);
        } else bst_insert(root->right, value);
    } else {
        if (!root->left) {
            root->left = new_node(value);
        } else bst_insert(root->left, value);
    }
}
```

### 3.2 真题

**真题 162：BST 建树 + 层序遍历**
- 解题思路：(1) 从数组逐个插入建 BST (2) 数组模拟队列做 BFS，结果覆盖回原数组
- 完整解答见 → [[162 树的层序遍历]]

**真题 179：镜像二叉树**
- 解题思路：递归交换左右子树。分配新结点，`left = mirror(right)`, `right = mirror(left)`
- 完整解答见 → [[179 镜像二叉树]]

**真题 180：孩子-兄弟表示法的层序遍历**
- 解题思路：普通树用孩子-兄弟法存储后，层序遍历时对每个出队结点，将其所有孩子（通过 `first` + `sibling` 链）入队
- 关键区别：二叉树是 `left/right`，普通树是 `first/sibling`
- 完整解答见 → [[180 树的层序遍历]]

### 3.3 套路总结

树与二叉树五大考法：
1. **遍历** — 递归一行代码；非递归用栈；层序用队列
2. **建树** — BST 逐个插入；前序+中序重建（递归分治）
3. **结点关系** — LCA 递归；路径打印（回溯+数组）
4. **树的变换** — 镜像翻转；树转二叉树（孩子-兄弟）
5. **计数统计** — 叶子数（左右都空）；高度（max(左,右)+1）

---

## 四、图

### 4.1 核心操作模板

**邻接矩阵入度/出度**：
```c
int indegree(MatrixGraph *G, int v) {
    int count = 0;
    for (int i = 0; i < G->vexnum; i++)
        if (G->arcs[i][v] != 0) count++;  // 第 v 列非零元素个数
    return count;
}

int outdegree(MatrixGraph *G, int v) {
    int count = 0;
    for (int j = 0; j < G->vexnum; j++)
        if (G->arcs[v][j] != 0) count++;  // 第 v 行非零元素个数
    return count;
}
```

**DFS 遍历**：
```c
void DFS(MatrixGraph *G, int v, bool visited[]) {
    visited[v] = true;
    visit(G->vertex[v]);
    for (int w = 0; w < G->vexnum; w++)
        if (G->arcs[v][w] != 0 && !visited[w])
            DFS(G, w, visited);
}
```

**BFS 遍历**：
```c
void BFS(MatrixGraph *G, int v) {
    int queue[MAX], head = 0, tail = 0;
    bool visited[MAX] = {false};
    visited[v] = true;
    queue[head++] = v;
    while (head > tail) {
        int curr = queue[tail++];
        visit(G->vertex[curr]);
        for (int w = 0; w < G->vexnum; w++)
            if (G->arcs[curr][w] != 0 && !visited[w]) {
                visited[w] = true;
                queue[head++] = w;
            }
    }
}
```

### 4.2 真题

**真题 127：邻接矩阵基本操作**
- 解题思路：insert_vertex 检查满/重复后添加；insert_arc 定位两顶点、检查存在/重复后设弧，无向图需设双向
- 完整解答见 → [[127 邻接矩阵]]

**真题 161：关键路径**
- 解题思路：(1) 正向求 ve[j]=max{ve(i)+w} (2) 逆向求 vl[j]=min{vl(k)-w} (3) e(i)=l(i) 的弧是关键活动
- 关键路径：`0 → 1 → 2 → 3 → 5`，长度 16
- 完整解答见 → [[161 关键路径]]

**真题 181：图的焊接（合并边）**
- 解题思路：遍历 G2 的每条弧，在 G1 中通过 locate_vertex 映射顶点标签，检查重复后用头插法插入
- 复杂度来源：标签映射、去重判断、头插法
- 完整解答见 → [[181 图的焊接]]

**真题 200：判断欧拉通路**
- 解题思路：统计每个顶点的入度和出度，检查 |入度-出度| ≤ 1，且差值为 ±1 的顶点恰好 0 个或 2 个
- 完整解答见 → [[200 判断欧拉通路]]

### 4.3 手算必考

**Prim 最小生成树**：
1. 任选起点加入集合 S
2. 找 S 到 V-S 的最小权边
3. 将边和对应顶点加入 S
4. 重复 n-1 次

**Kruskal 最小生成树**：
1. 所有边按权值排序
2. 从小到大选边，不成环就加入
3. 选够 n-1 条边停止

**关键路径（AOE 网）**：
1. 正向：`ve(j) = max{ve(i) + w(i,j)}`（所有前驱取 max）
2. 逆向：`vl(j) = min{vl(k) - w(j,k)}`（所有后继取 min）
3. `e(i) = ve(弧尾)`，`l(i) = vl(弧头) - w`
4. `e(i) == l(i)` → 关键活动，连成关键路径

### 4.4 套路总结

图论五大考法：
1. **存储结构** — 邻接矩阵（稠密图）、邻接表（稀疏图）
2. **遍历** — DFS（递归/栈）、BFS（队列）
3. **最短路径** — Dijkstra（单源不含负权）、Floyd（所有点对）
4. **最小生成树** — Prim（从点出发）、Kruskal（从边出发）
5. **拓扑排序/关键路径** — AOE 网求最长路径

---

## 五、查找与哈希

### 5.1 核心操作模板

**线性探测法插入**：
```c
void hash_insert_linear(int table[], int size, int key) {
    int idx = key % size;                  // 初始哈希位置
    while (table[idx] != 0)               // 冲突：线性探测
        idx = (idx + 1) % size;           // ⚠️ 取模实现循环
    table[idx] = key;
}
```

**拉链法插入**：
```c
void hash_insert_chain(HashNode *table[], int size, int key) {
    int idx = key % size;
    HashNode *node = malloc(sizeof(HashNode));
    node->key = key;
    node->next = table[idx];
    table[idx] = node;  // 头插法
}
```

### 5.2 真题

**真题 163：线性探测法**
- 解题思路：哈希函数 H(key)=key%13，冲突时 `key=(key+1)%SIZE` 循环探测。用 `calloc` 初始化（0 表示空位）
- 完整解答见 → [[163 线性探测法]]

**真题 199：哈希冲突（拉链法）**
- 解题思路：哈希函数 key%P，冲突时头插法插入链表。新结点的 `next` 指向原桶头，桶头更新为新结点
- 完整解答见 → [[199 哈希冲突]]

**真题 182：哈希排序（计数排序）**
- 解题思路：利用无重复值的特点，hash(K)=K。找最大值 m，建 m+1 大小的计数数组，值做下标计数，再按序收集
- 时间 O(n+m)，空间 O(m)，只适用于非负整数
- 完整解答见 → [[182 哈希排序]]

### 5.3 套路总结

查找四大考法：
1. **BST** — 左小右大，平均 O(log n)，最坏 O(n)
2. **AVL** — 平衡因子绝对值 ≤ 1，四种旋转 LL/RR/LR/RL
3. **哈希表** — 除留余数法 + 冲突处理（链地址/线性探测/二次探测）
4. **计数排序** — 值做下标，O(n+m)，非比较排序

---

## 六、排序

### 6.1 算法对比

| 算法 | 平均 | 最坏 | 空间 | 稳定 |
|:---|:---:|:---:|:---:|:---:|
| 选择排序 | O(n^2) | O(n^2) | O(1) | 否 |
| 插入排序 | O(n^2) | O(n^2) | O(1) | 是 |
| 快速排序 | O(n log n) | O(n^2) | O(log n) | 否 |
| 堆排序 | O(n log n) | O(n log n) | O(1) | 否 |
| 归并排序 | O(n log n) | O(n log n) | O(n) | 是 |
| 计数排序 | O(n+m) | O(n+m) | O(m) | 是 |

### 6.2 手写代码模板

**简单选择排序** — 每次选最小交换到前面：
```c
void selection_sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++)
            if (arr[j] < arr[min_idx]) min_idx = j;
        swap(&arr[i], &arr[min_idx]);
    }
}
```

**直接插入排序** — 类似打牌，新牌插入已排序的正确位置：
```c
void insertion_sort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i], j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];  // 后移
            j--;
        }
        arr[j + 1] = key;  // 插入
    }
}
```

**快速排序** — 分治，选基准分区：
```c
int partition(int arr[], int low, int high) {
    int pivot = arr[high], i = low - 1;
    for (int j = low; j < high; j++)
        if (arr[j] <= pivot) swap(&arr[++i], &arr[j]);
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}
```

**堆排序** — 建堆 + 逐个取堆顶：
```c
void heap_sort(int arr[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--)  // 建最大堆
        heapify_down_max(arr, n, i);
    for (int i = n - 1; i > 0; i--) {      // 逐个取堆顶
        swap(&arr[0], &arr[i]);
        heapify_down_max(arr, i, 0);
    }
}
```

### 6.3 手算第一趟结果

给定数组 `[49, 38, 65, 97, 76, 13, 27, 49]`：

| 排序算法 | 第一趟结果 | 说明 |
|:---|:---|:---|
| 直接插入 | `[38, 49, 65, 97, 76, 13, 27, 49]` | 38 插入到 49 前面 |
| 简单选择 | `[13, 38, 65, 97, 76, 49, 27, 49]` | 最小的 13 和第一个交换 |
| 快速排序 | `[27, 38, 13, 49, 76, 97, 65, 49]` | 以 49 为基准分区 |

---

## 七、考试策略

### 时间分配（2 小时 5 题）

| 阶段 | 时间 | 内容 |
|:---|:---:|:---|
| 手算题 | 15-20 min | Prim/Kruskal/关键路径 |
| 编程题 ×4-5 | 每题 20-25 min | 按难度排序做 |
| 检查 | 10 min | 边界情况、编译错误 |

### 做题顺序建议

1. 先做手算题（稳拿分）
2. 再做编程题，从简单到难：线性表/排序 → 树遍历 → 图 → 其他

### 编程题技巧

- 先写核心逻辑，再补边界检查
- 用注释说明思路（即使没写完也有步骤分）
- 善用辅助函数（swap、visit 等）
- 注意 `malloc` 后检查是否为 NULL

### 高频考点

| 频率 | 考点 |
|:---:|:---|
| ★★★ | 非递归先序遍历、顺序表/链表操作 |
| ★★ | 图的遍历/入度出度、哈希表操作 |
| ★ | 排序算法、关键路径手算 |

---

## 八、真题速查表

| 编号 | 题目 | 知识点 | 文件 |
|:---:|:---|:---|:---|
| 113 | 循环链表表示队列 | 队列+循环链表 | [[113 循环链表表示队列]] |
| 120 | 非递归先序遍历 | 栈+二叉树 | [[120 非递归先序遍历]] |
| 127 | 邻接矩阵操作 | 图的存储 | [[127 邻接矩阵]] |
| 160 | 合并顺序表 | 线性表归并 | [[160 合并顺序表]] |
| 161 | 关键路径 | AOE 网 | [[161 关键路径]] |
| 162 | BST+层序遍历 | 队列+BST | [[162 树的层序遍历]] |
| 163 | 线性探测法 | 哈希表 | [[163 线性探测法]] |
| 176 | 整除移除 | 双指针 | [[176 整除移除]] |
| 177 | 共享结点 | 链表双指针 | [[177 共享结点]] |
| 178 | 反转字符串 | 递归转栈 | [[178 反转字符串]] |
| 179 | 镜像二叉树 | 递归 | [[179 镜像二叉树]] |
| 180 | 孩子-兄弟层序遍历 | 队列+树 | [[180 树的层序遍历]] |
| 181 | 图的焊接 | 邻接表合并 | [[181 图的焊接]] |
| 182 | 哈希排序 | 计数排序 | [[182 哈希排序]] |
| 197 | 保留偶数 | 双指针 | [[197 保留线性表中偶数]] |
| 198 | 非递归先序遍历 | 栈+二叉树 | [[198 非递归先序遍历]] |
| 199 | 哈希冲突 | 拉链法 | [[199 哈希冲突]] |
| 200 | 欧拉通路 | 图论+度数 | [[200 判断欧拉通路]] |
| 201 | 合并有序数组 | 归并 | [[201 合并有序数组]] |
