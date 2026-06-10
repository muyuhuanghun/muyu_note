#include "hashtable.h"
#include <windows.h>
// ========================
// 哈希表基本操作实现
// ========================

// 初始化哈希表：将所有位置标记为 EMPTY
void InitHashTable(HashTable *HT) {
    int i;
    for (i = 0; i < TABLE_SIZE; i++) {
        HT->data[i].status = EMPTY;
        HT->data[i].name[0] = '\0';
    }
    HT->count = 0;
}

// 哈希函数：除留余数法
// 将姓名拼音每个字符的 ASCII 码累加，再对表长 TABLE_SIZE 取模
int Hash(char *name) {
    int sum = 0;
    while (*name) {
        sum += (int)(*name);
        name++;
    }
    return sum % TABLE_SIZE;
}

// 在哈希表中插入姓名（线性探测再散列）
// 插入成功返回实际查找长度
int InsertHash(HashTable *HT, char *name) {
    int addr, start;
    int len = 1; // 查找长度，初始为1（第一次探测）

    addr = Hash(name);
    start = addr;

    // 线性探测：如果当前位置被占用，依次向后探测
    while (HT->data[addr].status == OCCUPIED) {
        // 如果已存在相同姓名，插入失败
        if (strcmp(HT->data[addr].name, name) == 0) {
            printf("  [!] 姓名 \"%s\" 已存在，跳过\n", name);
            return -1;
        }
        addr = (addr + 1) % TABLE_SIZE;
        len++;
        // 探测一圈回到起点，说明表已满
        if (addr == start) {
            printf("  [!] 哈希表已满，无法插入 \"%s\"\n", name);
            return -1;
        }
    }

    // 找到空位，插入
    strcpy(HT->data[addr].name, name);
    HT->data[addr].status = OCCUPIED;
    HT->count++;

    printf("  插入 \"%-10s\" -> Hash=%2d, 实际存放位置=%2d, 查找长度=%d\n",
           name, Hash(name), addr, len);
    return len;
}

// 在哈希表中查找姓名
// 找到返回查找长度，未找到返回 -1
int SearchHash(HashTable HT, char *name) {
    int addr, start;
    int len = 1;

    addr = Hash(name);
    start = addr;

    while (HT.data[addr].status == OCCUPIED) {
        if (strcmp(HT.data[addr].name, name) == 0) {
            printf("  查找 \"%-10s\" -> Hash=%2d, 实际位置=%2d, 查找长度=%d\n",
                   name, Hash(name), addr, len);
            return len;
        }
        addr = (addr + 1) % TABLE_SIZE;
        len++;
        if (addr == start) break; // 探测一圈
    }

    printf("  查找 \"%-10s\" -> 未找到\n", name);
    return -1;
}

// 打印哈希表全部内容
void PrintHashTable(HashTable HT) {
    int i;
    printf("\n========== 哈希表内容 (表长=%d, 元素=%d) ==========\n",
           TABLE_SIZE, HT.count);
    printf("  下标\t| 状态\t| 姓名\n");
    printf("  ------+-------+----------------\n");
    for (i = 0; i < TABLE_SIZE; i++) {
        if (HT.data[i].status == OCCUPIED) {
            printf("  %2d\t| 占用\t| %s\n", i, HT.data[i].name);
        }
    }
    printf("==================================================\n");
}

// 计算并返回平均查找长度（仅对已存入的元素统计）
float CalcASL(HashTable HT) {
    int i;
    int totalLen = 0;
    int found = 0;

    for (i = 0; i < TABLE_SIZE; i++) {
        if (HT.data[i].status == OCCUPIED) {
            // 对每个已存元素模拟查找，累加查找长度
            int addr = Hash(HT.data[i].name);
            int len = 1;
            while (strcmp(HT.data[addr].name, HT.data[i].name) != 0) {
                addr = (addr + 1) % TABLE_SIZE;
                len++;
            }
            totalLen += len;
            found++;
        }
    }

    if (found == 0) return 0.0f;
    return (float)totalLen / found;
}

// ========================
// 主函数：演示哈希表操作
// ========================
int main() {
    system("chcp 65001 > nul");
    SetConsoleOutputCP(CP_UTF8);
    HashTable HT;
    int i, totalLen = 0;

    // 30个学生的姓名（汉语拼音）
    char *students[STU_NUM] = {
        "ZhangSan",   "LiSi",       "WangWu",     "ZhaoLiu",    "QianQi",
        "SunBa",      "ZhouJiu",    "WuShi",      "ZhengYi",    "FengEr",
        "ChenSan",    "ChuSi",      "WeiWu",      "JiangLiu",   "ShenQi",
        "HanBa",      "YangJiu",    "ZhuShi",     "QinYi",      "YouEr",
        "XuSan",      "HeSi",       "LvWu",       "ShiLiu",     "ZhangQi",
        "KongBa",     "CaoJiu",     "YanShi",     "HuaYi",      "TaoEr"
    };

    // 1. 初始化哈希表
    InitHashTable(&HT);

    // 2. 逐一插入30个姓名
    printf("========================================\n");
    printf("  哈希表插入过程 (表长=%d, 元素=%d)\n", TABLE_SIZE, STU_NUM);
    printf("  哈希函数: H(key) = sum(ASCII) %% %d\n", TABLE_SIZE);
    printf("  冲突处理: 线性探测再散列\n");
    printf("========================================\n\n");

    for (i = 0; i < STU_NUM; i++) {
        int len = InsertHash(&HT, students[i]);
        if (len > 0) {
            totalLen += len;
        }
    }

    // 3. 打印哈希表
    PrintHashTable(HT);

    // 4. 计算并输出平均查找长度
    float asl = CalcASL(HT);
    printf("\n  总查找长度 = %d\n", totalLen);
    printf("  成功插入元素数 = %d\n", HT.count);
    printf("  平均查找长度 ASL = %d / %d = %.4f\n", totalLen, HT.count, asl);

    if (asl <= 2.0f) {
        printf("  ASL <= 2，满足要求!\n");
    } else {
        printf("  ASL > 2，未满足要求，需调整表长或哈希函数\n");
    }

    // 5. 演示查找操作
    printf("\n========================================\n");
    printf("  演示查找操作\n");
    printf("========================================\n\n");

    SearchHash(HT, "ZhangSan");
    SearchHash(HT, "TaoEr");
    SearchHash(HT, "NotExist");

    return 0;
}
