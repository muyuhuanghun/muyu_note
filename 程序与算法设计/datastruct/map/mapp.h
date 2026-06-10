#ifndef MAP_H
#define MAP_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STN 9
#define NUM_UNI 5
#define INF 99999

enum {
	LINE_1 = 0,
	LINE_4,
	LINE_6,
	LINE_7,
	LINE_8,
	LINE_18,
	LINE_COUNT
};

typedef struct {
	int u;
	int v;
	int w;
	int line_num;
} Road;

static const char *line_name[LINE_COUNT] = {
	"地铁1号线",
	"地铁4号线",
	"地铁6号线",
	"地铁7号线",
	"地铁8号线",
	"地铁18号线"
};

// 仅保留高校站点及必须的换乘站
static const char *stn_name[MAX_STN] = {
	"川大江安校区",  // 0
	"珠江路",        // 1
	"火车南站",      // 2
	"文化宫",        // 3
	"西南财大",      // 4
	"西南交大",      // 5
	"建设北路",      // 6
	"四川师大",      // 7
	"理工大学"       // 8
};

static const int stn_mask[MAX_STN] = {
	(1 << LINE_8),                                 // 川大江安校区
	(1 << LINE_8) | (1 << LINE_18),                // 珠江路
	(1 << LINE_1) | (1 << LINE_7) | (1 << LINE_18), // 火车南站
	(1 << LINE_4) | (1 << LINE_7),                 // 文化宫
	(1 << LINE_4),                                 // 西南财大
	(1 << LINE_6) | (1 << LINE_7),                 // 西南交大
	(1 << LINE_6),                                 // 建设北路
	(1 << LINE_7),                                 // 四川师大
	(1 << LINE_7) | (1 << LINE_8)                  // 理工大学
};

static const char *uni_name[NUM_UNI] = {
	"四川大学江安校区",
	"电子科技大学沙河校区",
	"西南交通大学",
	"西南财经大学",
	"四川师范大学"
};

typedef struct {
	const char *alias;
	int uni_idx;
} UniAlias;

static const UniAlias uni_alias[] = {
	{"四川大学江安校区", 0}, {"四川大学", 0}, {"川大", 0}, {"川大江安", 0},
	{"电子科技大学沙河校区", 1}, {"电子科技大学", 1}, {"电子科大", 1}, {"电子科大沙河", 1},
	{"西南交通大学", 2}, {"西南交大", 2},
	{"西南财经大学", 3}, {"西南财大", 3},
	{"四川师范大学", 4}, {"四川师大", 4}, {"川师大", 4}
};

static const int uni_alias_cnt = sizeof(uni_alias) / sizeof(uni_alias[0]);
static int uni_stn[NUM_UNI] = {0, 6, 5, 4, 7};

static int G[MAX_STN][MAX_STN];

static Road edge_list[] = {
	{0, 1, 2, LINE_8},   // 川大江安校区 - 珠江路
	{1, 8, 9, LINE_8},   // 珠江路 - 理工大学
	{1, 2, 6, LINE_18},  // 珠江路 - 火车南站
	{8, 5, 7, LINE_7},   // 理工大学 - 西南交大
	{5, 3, 4, LINE_7},   // 西南交大 - 文化宫
	{3, 2, 7, LINE_7},   // 文化宫 - 火车南站
	{2, 7, 4, LINE_7},   // 火车南站 - 四川师大
	{7, 8, 8, LINE_7},   // 四川师大 - 理工大学
	{3, 4, 1, LINE_4},   // 文化宫 - 西南财大
	{5, 6, 4, LINE_6}    // 西南交大 - 建设北路
};

static int edge_cnt = sizeof(edge_list) / sizeof(edge_list[0]);

static void graph_init(void) {
	int i, j;
	for (i = 0; i < MAX_STN; i++) {
		for (j = 0; j < MAX_STN; j++) {
			G[i][j] = (i == j) ? 0 : INF;
		}
	}
	for (i = 0; i < edge_cnt; i++) {
		int u = edge_list[i].u;
		int v = edge_list[i].v;
		int w = edge_list[i].w;
		G[u][v] = w;
		G[v][u] = w;
	}
}

static void print_station_lines(int s) {
	int i, first = 1;
	for (i = 0; i < LINE_COUNT; i++) {
		if (stn_mask[s] & (1 << i)) {
			if (!first) {
				printf("/");
			}
			printf("%s", line_name[i]);
			first = 0;
		}
	}
	if (first) {
		printf("未知线路");
	}
}

static int is_transfer(int s) {
	int i, count = 0;
	for (i = 0; i < LINE_COUNT; i++) {
		if (stn_mask[s] & (1 << i)) {
			count++;
		}
	}
	return count > 1;
}

static int find_uni(const char *name) {
	int i;
	for (i = 0; i < uni_alias_cnt; i++) {
		if (strcmp(name, uni_alias[i].alias) == 0) {
			return uni_alias[i].uni_idx;
		}
	}
	return -1;
}

static int line_between(int u, int v) {
	int i;
	for (i = 0; i < edge_cnt; i++) {
		if ((edge_list[i].u == u && edge_list[i].v == v) ||
		    (edge_list[i].u == v && edge_list[i].v == u)) {
			return edge_list[i].line_num;
		}
	}
	return -1;
}

static int dijkstra(int src, int dst, int path[], int *plen) // 返回最短距离，路径通过 path 数组输出，plen 输出路径长度
{
	int dist[MAX_STN], done[MAX_STN], prev[MAX_STN];
	int i, count, u, v, min_d;

	for (i = 0; i < MAX_STN; i++) {
		dist[i] = INF;
		done[i] = 0;
		prev[i] = -1;
	}// 初始化距离为无穷大，未访问，前驱节点为 -1
	dist[src] = 0;// 起点距离为 0

	for (count = 0; count < MAX_STN; count++) 
	{
		u = -1;
		min_d = INF;// 找到未访问的距离最小的节点 u
		for (i = 0; i < MAX_STN; i++) // 遍历所有节点，找到未访问且距离最小的节点
		{
			if (!done[i] && dist[i] < min_d) 
			{
				min_d = dist[i];
				u = i;
			}
		}
		if (u == -1 || u == dst)// 如果没有找到可访问的节点或者已经到达目的地，结束循环 
		{
			break;
		}
		done[u] = 1;
		for (v = 0; v < MAX_STN; v++) // 更新 u 的邻接节点 v 的距离，如果通过 u 更近
		{
			if (!done[v] && G[u][v] < INF && dist[u] + G[u][v] < dist[v]) // 如果 v 未访问且 u 和 v 之间有边且通过 u 到 v 的距离更短
			{
				dist[v] = dist[u] + G[u][v];
				prev[v] = u;
			}
		}
	}

	if (dist[dst] >= INF) // 如果目的地不可达，返回 INF
	{
		return INF;
	}

	{
		int tmp[MAX_STN];// 临时数组用于存储路径
		int len = 0;
		int cur = dst;
		while (cur != -1) // 从目的地开始通过 prev 数组回溯到起点，构建路径
		{
			tmp[len++] = cur;
			cur = prev[cur];
		}
		for (i = 0; i < len; i++) 
		{
			path[i] = tmp[len - 1 - i];
		}
		*plen = len;
	}
	return dist[dst];
}

static void map_print(void) {
	int i;
	printf("========================================\n");
	printf("      成都高校轨道交通简化拓扑图\n");
	printf("      (基于成都地铁线路关系简化)\n");
	printf("========================================\n");
	printf("高校对应站点：\n");
	for (i = 0; i < NUM_UNI; i++) {
		printf("  %s -> %s %s\n", uni_name[i], stn_name[uni_stn[i]], is_transfer(uni_stn[i]) ? "[换乘站]" : "");
	}
	printf("\n字符版简图（括号内为估计站数权重）：\n");
	printf("  [建设北路/电子科大沙河]\n");
	printf("            | 地铁6号线(4)\n");
	printf("  [西南交大] --地铁7号线(4)-- [文化宫] --地铁4号线(1)-- [西南财大]\n");
	printf("      | 地铁7号线(7)                |\n");
	printf("  [理工大学] --地铁8号线(9)-- [珠江路] --地铁18号线(6)-- [火车南站] --地铁7号线(4)-- [四川师大]\n");
	printf("      ^\n");
	printf("      | 地铁8号线(2)\n");
	printf("  [川大江安校区]\n");
	printf("\n站点与线路：\n");
	for (i = 0; i < MAX_STN; i++) {
		printf("  %-16s  ", stn_name[i]);
		print_station_lines(i);
		printf(" %s\n", is_transfer(i) ? "[换乘站]" : "");
	}
	printf("\n相邻站连线：\n");
	for (i = 0; i < edge_cnt; i++) {
		printf("  %s --(%d)--> %s  [%s]\n",
		       stn_name[edge_list[i].u],
		       edge_list[i].w,
		       stn_name[edge_list[i].v],
		       line_name[edge_list[i].line_num]);
	}
	printf("========================================\n");
}

static void route_print(const char *start_uni, const char *end_uni, int path[], int plen) {
	int i, total = 0, last_line = -1;
	if (plen <= 0) {
		return;
	}
	printf("\n%s -> %s 的最短地铁路径：\n", start_uni, end_uni);
	for (i = 0; i < plen - 1; i++) {
		int u = path[i];
		int v = path[i + 1];
		int line_num = line_between(u, v);
		const char *line_text = (line_num >= 0) ? line_name[line_num] : "未知线路";
		int w = G[u][v];
		total += w;
		if (line_num != last_line) {
			if (last_line == -1) {
				printf("  乘坐%s\n", line_text);
			} else {
				printf("  在 %s 换乘到%s\n", stn_name[u], line_text);
			}
			last_line = line_num;
		}
		printf("    %s --[%s, 约%d站]--> %s\n", stn_name[u], line_text, w, stn_name[v]);
	}
	printf("总估计站数权重：%d\n", total);

}

#endif
