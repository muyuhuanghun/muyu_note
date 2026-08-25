#ifndef HASHTABLE_H
#define HASHTABLE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 哈希表相关常量
#define MAX_NAME_LEN 20    // 姓名最大长度
#define TABLE_SIZE 61      // 哈希表长度(素数，适合除留余数法)
#define STU_NUM 30         // 学生人数

// 哈希表元素状态
typedef enum { EMPTY, OCCUPIED } Status;

// 哈希表元素结构
typedef struct {
    char name[MAX_NAME_LEN]; // 姓名(拼音)
    Status status;            // 当前状态：空或占用
} HashElem;

// 哈希表结构
typedef struct {
    HashElem data[TABLE_SIZE]; // 哈希表存储数组
    int count;                  // 已存入的元素个数
} HashTable;

// ========================
// 哈希表基本操作声明
// ========================

// 初始化哈希表
void InitHashTable(HashTable *HT);

// 哈希函数：除留余数法
// 将姓名中每个字符的ASCII码值求和，再对表长取模
int Hash(char *name);

// 在哈希表中插入一个姓名（线性探测再散列处理冲突）
// 返回实际查找长度
int InsertHash(HashTable *HT, char *name);

// 在哈希表中查找姓名
// 返回查找长度，若未找到返回 -1
int SearchHash(HashTable HT, char *name);

// 打印哈希表内容
void PrintHashTable(HashTable HT);

// 计算平均查找长度
float CalcASL(HashTable HT);

#endif // HASHTABLE_H
