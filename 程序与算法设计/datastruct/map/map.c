#include "mapp.h"
#include <windows.h>
int main(void) {
	int i;

	 system("chcp 65001 > nul");
    SetConsoleOutputCP(CP_UTF8);


	char input[128];
	int choice;

	graph_init();

	printf("========================================\n");
	printf("    成都高校地铁最短路径简化程序\n");
	printf("========================================\n");
	printf("支持高校：\n");
	for (i = 0; i < NUM_UNI; i++) {
		printf("  %d) %s\n", i + 1, uni_name[i]);
	}
	printf("可输入简称：四川大学/川大、电子科技大学/电子科大、西南交大、西南财大、四川师大\n");
	printf("========================================\n");

	for (;;) {
		printf("\n1. 打印简化地铁图\n");
		printf("2. 查询两所高校最短路径\n");
		printf("3. 退出\n");
		printf("请选择：");

		if (fgets(input, sizeof(input), stdin) == NULL) {
			break;
		}
		choice = atoi(input);

		if (choice == 1) {
			map_print();
		} else if (choice == 2) {
			char start_name[64], end_name[64];
			int s1, s2;
			int path[MAX_STN];
			int plen;
			int result;

			printf("请输入起点高校名称：");
			if (fgets(start_name, sizeof(start_name), stdin) == NULL) {
				continue;
			}
			start_name[strcspn(start_name, "\n")] = '\0';

			printf("请输入终点高校名称：");
			if (fgets(end_name, sizeof(end_name), stdin) == NULL) {
				continue;
			}
			end_name[strcspn(end_name, "\n")] = '\0';

			int u1 = find_uni(start_name);
			int u2 = find_uni(end_name);
			if (u1 < 0) {
				printf("未找到高校：%s\n", start_name);
				continue;
			}
			if (u2 < 0) {
				printf("未找到高校：%s\n", end_name);
				continue;
			}
			if (u1 == u2) {
				printf("两所高校相同，无需出行。\n");
				continue;
			}

			s1 = uni_stn[u1];
			s2 = uni_stn[u2];
			if (s1 < 0 || s2 < 0) {
				printf("高校对应站点未正确加载，请检查地铁图数据。\n");
				continue;
			}
			result = dijkstra(s1, s2, path, &plen);

			if (result >= INF) {
				printf("当前地图中没有可达路径。\n");
			} else {
				route_print(uni_name[u1], uni_name[u2], path, plen);
			}
		} else if (choice == 3) {
			printf("程序结束。\n");
			break;
		} else {
			printf("输入有误，请重新选择。\n");
		}
	}

	return 0;
}
