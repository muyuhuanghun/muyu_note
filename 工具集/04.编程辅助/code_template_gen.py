#!/usr/bin/env python3
"""
代码模板生成器
📌 常用数据结构和算法的模板代码，支持 Python 和 C++
📌 直接复制到 LeetCode/icoding 等平台使用
"""

import argparse
import sys

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# ============================
# 📌 模板库
# ============================

TEMPLATES = {
    "python": {
        "quicksort": '''def quicksort(arr):
    """快速排序 — 平均 O(n log n)"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)
''',
        "bfs": '''from collections import deque

def bfs(graph, start):
    """BFS 广度优先搜索 — O(V+E)"""
    visited = set([start])
    queue = deque([start])
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return result
''',
        "dfs": '''def dfs(graph, node, visited=None):
    """DFS 深度优先搜索 — O(V+E)"""
    if visited is None:
        visited = set()
    visited.add(node)
    result = [node]
    for neighbor in graph[node]:
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))
    return result
''',
        "dijkstra": '''import heapq

def dijkstra(graph, start):
    """Dijkstra 最短路径 — O((V+E)logV)"""
    dist = {node: float("inf") for node in graph}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist
''',
        "binary_search": '''def binary_search(arr, target):
    """二分查找 — O(log n)"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
''',
        "union_find": '''class UnionFind:
    """并查集 — 路径压缩 + 按秩合并"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
''',
        "trie": '''class Trie:
    """前缀树 — 插入和查找 O(m)，m 为字符串长度"""
    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word):
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix):
        node = self
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
''',
        "lru_cache": '''from collections import OrderedDict

class LRUCache:
    """LRU 缓存 — get/put 均为 O(1)"""
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
''',
        "segment_tree": '''class SegmentTree:
    """线段树 — 区间查询和单点更新 O(log n)"""
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self._build(data, 2 * node, start, mid)
        self._build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, index, val, node=1, start=0, end=None):
        if end is None:
            end = self.n - 1
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if index <= mid:
            self.update(index, val, 2 * node, start, mid)
        else:
            self.update(index, val, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, l, r, node=1, start=0, end=None):
        if end is None:
            end = self.n - 1
        if r < start or l > end:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self.query(l, r, 2 * node, start, mid) +
                self.query(l, r, 2 * node + 1, mid + 1, end))
''',
        "topological_sort": '''from collections import deque

def topological_sort(n, edges):
    """拓扑排序 — Kahn 算法 O(V+E)"""
    graph = [[] for _ in range(n)]
    in_degree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque(i for i in range(n) if in_degree[i] == 0)
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != n:
        return []  # 存在环
    return result
''',
    },
    "cpp": {
        "quicksort": '''#include <vector>
using namespace std;

// 快速排序 — 平均 O(n log n)
void quicksort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int pivot = arr[(left + right) / 2];
    int i = left, j = right;
    while (i <= j) {
        while (arr[i] < pivot) i++;
        while (arr[j] > pivot) j--;
        if (i <= j) swap(arr[i++], arr[j--]);
    }
    quicksort(arr, left, j);
    quicksort(arr, i, right);
}
''',
        "bfs": '''#include <vector>
#include <queue>
using namespace std;

// BFS 广度优先搜索 — O(V+E)
vector<int> bfs(vector<vector<int>>& graph, int start) {
    vector<int> result;
    vector<bool> visited(graph.size(), false);
    queue<int> q;
    q.push(start);
    visited[start] = true;
    while (!q.empty()) {
        int node = q.front(); q.pop();
        result.push_back(node);
        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
    return result;
}
''',
        "graph": '''#include <vector>
#include <queue>
#include <stack>
using namespace std;

// 邻接表图结构 + BFS/DFS
struct Graph {
    int n;
    vector<vector<int>> adj;

    Graph(int n) : n(n), adj(n) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u); // 无向图
    }

    // BFS
    vector<int> bfs(int start) {
        vector<int> result;
        vector<bool> visited(n, false);
        queue<int> q;
        q.push(start);
        visited[start] = true;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            result.push_back(u);
            for (int v : adj[u]) {
                if (!visited[v]) {
                    visited[v] = true;
                    q.push(v);
                }
            }
        }
        return result;
    }

    // DFS（递归）
    void dfsHelper(int u, vector<bool>& visited, vector<int>& result) {
        visited[u] = true;
        result.push_back(u);
        for (int v : adj[u]) {
            if (!visited[v]) dfsHelper(v, visited, result);
        }
    }

    vector<int> dfs(int start) {
        vector<int> result;
        vector<bool> visited(n, false);
        dfsHelper(start, visited, result);
        return result;
    }
};
''',
        "binary_search": '''#include <vector>
using namespace std;

// 二分查找 — O(log n)
int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
''',
        "union_find": '''#include <vector>
using namespace std;

// 并查集 — 路径压缩 + 按秩合并
struct UnionFind {
    vector<int> parent, rank;

    UnionFind(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    bool unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        if (rank[px] < rank[py]) swap(px, py);
        parent[py] = px;
        if (rank[px] == rank[py]) rank[px]++;
        return true;
    }
};
''',
    },
}


def list_templates():
    """列出所有可用模板"""
    print("📋 可用模板:\n")
    for lang, templates in TEMPLATES.items():
        print(f"  [{lang}]")
        for name in templates:
            print(f"    - {name}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="代码模板生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python code_template_gen.py --lang python --template quicksort
  python code_template_gen.py --lang cpp --template graph
  python code_template_gen.py --list
        """,
    )
    parser.add_argument("--lang", choices=["python", "cpp"], help="编程语言")
    parser.add_argument("--template", help="模板名称")
    parser.add_argument("--list", action="store_true", help="列出所有模板")
    parser.add_argument("-o", "--output", help="输出到文件")

    args = parser.parse_args()

    if args.list:
        list_templates()
        return

    if not args.lang or not args.template:
        parser.print_help()
        return

    lang_templates = TEMPLATES.get(args.lang, {})
    template = lang_templates.get(args.template)

    if not template:
        print(f"❌ 未找到模板: {args.lang}/{args.template}")
        print(f"   可用模板: {', '.join(lang_templates.keys())}")
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(template)
        print(f"✅ 已保存到: {args.output}")
    else:
        print(template)


if __name__ == "__main__":
    main()
