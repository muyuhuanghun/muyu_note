# ch4-串


---

### Slide 1


## 第四章 串

## 授课教师：傅翀

---

### Slide 2


- 4.1 串的基本概念

- 串（或字符串String）是由零个或多个字符组成的有限序列。
- 串的逻辑表示， ai（1≤i≤n）代表一个字符：

## 串    线性表

## “a1 a2 … an”

---

### Slide 3


- 串的概念

- 子串：一个串中任意个连续字符组成的子序列（含空串）称为该串的子串。
- 真子串：是指不包含自身的所有子串。
- 主串：包含子串的串称为主串。
- 空串： n=0时的串为空串
- 例如， “abcde”的子串有：
  - “”、“a”、“ab” 、“abc”、“abcd”和“abcde”等

---

### Slide 4


- 串的抽象数据类型定义

- ADT String {
- 数据对象: D={ai| ai ∈CharacterSet,i=1,2,…,n;  n≥0}
- 数据关系: R={<ai,ai+1>| ai,ai+1 ∈D, i=1,…,n-1;  n-1≥0}
- 基本操作：
- 1）StrAssign(S,chars)
- 初始条件： chars是字符串常量
- 操作结果：生成一个值等于chars的串S

---

### Slide 5


## 2）StrInsert(S,pos,T)
## 初始条件：串S和T存在，1≤pos≤StrLength(S) +1
## 操作结果：在串S的第pos个字符之前插入串T
## 3）StrDelete(S,pos,len)
## 初始条件：串S存在，1≤pos≤StrLength(S) -len +1
## 操作结果：从串S中删除第pos个字符起长度为len的子串
## 4）StrCopy(S,T)
## 初始条件：串S存在
## 操作结果：由串T复制得串S

---

### Slide 6


## 5）StrEmpty(S)
## 初始条件：串S存在
## 操作结果：若串S为空串，则返回TRUE，否则返回FALSE
## 6）StrCompare(S,T)
## 初始条件：串S和T存在
## 操作结果：若S>T，则返回值>0；若S=T，则返回值=0；若S<T，则返回值<0
## 7）StrLength(S)
## 初始条件：串S存在
## 操作结果：返回串S的长度，即串S中的元素个数

---

### Slide 7


## 8）StrClear(S)
## 初始条件：串S存在
## 操作结果：将S清为空串
## 9）StrCat(S,T)
## 初始条件：串S和T存在
## 操作结果：将串T的值连接在串S的后面
## 10）SubString(Sub,S,pos,len)
## 初始条件：串S存在, 1≤pos≤StrLength(S) -len +1
## 操作结果：用Sub返回串S的第pos个字符起长度为len的子串

---

### Slide 8


## 11）StrIndex(S,T,pos)
## 初始条件：串S和T存在，T是非空串，1≤pos≤StrLength(S)
## 操作结果：若串S中存在与串T相同的子串，则返回它在串S中第pos个字符之后第
## 一次出现的位置；否则返回0
## 12）StrReplace(S,T,V)
## 初始条件：串S，T和V存在，且T是非空串
## 操作结果：用V替换串S中出现的所有与T相等的不重叠子串
## 13）StrDestroy(S)
## 初始条件：串S存在
## 操作结果：销毁串S
## ｝ADT String;

---

### Slide 9


- 串

## 串的逻辑结构和线性表极为相似，区别仅在于串的数据对象约束为字符集。
## 串的基本操作和线性表有很大差别：
  - 在线性表的基本操作中，大多以“单个元素”作为操作对象；
  - 在串的基本操作中，通常以“串的整体”作为操作对象。

---

### Slide 10


## 4.2 串的存储实现

## 静态存储方式：
  - 顺序串
## 动态存储方式：
  - 堆串
  - 块链串

---

### Slide 11


- 4.2.1 定长顺序串

- 定长顺序串是将串设计成一种结构类型，串的存储分配是在编译时完成的。
- 串的定长顺序存储表示：

## #define MAXLEN 40
## typedef struct {   /*串结构定义*/
## char ch[MAXLEN];
## int len;
## } SString;

---

### Slide 12


- 4.2.2 堆串

- 这种存储方法以一组地址连续的存储单元存放串的字符序列，但它们的存储空间是在程序执行过程中动态分配的。
- 系统将一个地址连续、容量很大的存储空间作为字符串的可用空间，每当建立一个新串时，系统就从这个空间中分配一个大小和字符串长度相同的空间存储新串的串值。
- 在C语言中，存在一个称为“堆”的自由空间，由动态分配函数malloc( )分配一块实际串长所需的存储空间，如果分配成功，则返回这段空间的起始地址，作为串的基址。由free( )释放串不再需要的空间。

---

### Slide 13


- 堆串的定义

- typedef struct{
- char *ch;	//若是非空串，按串长分配空间，否则ch为NULL
- int length;	//串长
- } string;

## 程序执行过程中，按需生成新串，销毁旧串

---

### Slide 14


- 堆串的存储映象示例

## a='a program'，b='string '，c='process'

## Heap[MAXSIZE]                 free=23

## 符号表

---

### Slide 15


- 4.2.3 块链串

## 串的链式存储结构中每个结点包含字符域和结点链接指针域，字符域用于存放字符，指针域用于存放指向下一个结点的指针，因此，串可用单链表表示。
## 用单链表存放串，每个结点仅存储一个字符，因此，每个结点的指针域所占空间比字符域所占空间要大得多。为了提高空间的利用率，我们可以使每个结点存放多个字符，称为块链结构。

---

### Slide 16


- 块链结构的定义

## #define  BLOCK_SIZE  4  /*每结点存放字符个数*/
## typedef struct Block{
## char ch[BLOCK_SIZE];	 /*BLOCK_SIZE为1，就是单链表结构*/
## struct Block   *next;
## } Block;
## typedef struct {
## Block   *head;
## Block   *tail; 	/* tail联接2个串使用*/
## int     length;
## } BLString;

---

### Slide 17


## 存储密度

---

### Slide 18


## 以下关于串的叙述中，正确的是（ ）

## 串必须由字母组成

## 串是一种特殊的线性表

## 串的长度必须大于零

## 空串就是空格串

- A

- B

- C

- D

- 提交

- 可为此题添加文本、图片、公式等解析，且需将内容全部放在本区域内。

## 解析：串是字符组成的有限序列，属于线性结构，空串长度为0，空格串由空格组成。

---

### Slide 19


- 4.3  串的模式匹配

- 成功是指在目标串S中找到一个模式串T  T是S的子串，返回T在S中的位置。
- 不成功则指目标串S中不存在模式串T  T不是S的子串，返回-1。

---

### Slide 20


- 4.3.1  Brute-Force算法

- Brute-Force简称为BF算法，亦称简单匹配算法。
- 采用穷举的思路	，从S的每一个字符开始依次与T的字符进行匹配。

## a    a    a    a    b    c    d

## 匹配成功

## S:

## T:

---

### Slide 21


- 例如：目标串S=“aaaaab”，模式串T=“aaab”。S的长度为n（n=6），T的长度为m（m=4）。BF算法的匹配过程如下：

## a       a       a       a       a       b

## a       a       a       b

- 匹配失败：
- i = i-j+1 = 1 （回退到）
- j = 0 （从头开始）

- S：

- T：

---

### Slide 22


- i =1，j=0

## a       a       a       a       a       b

## a       a       a       b

- S：

- T：

- 匹配失败：
- i = i-j+1 = 2（回退到）
- j = 0（从头开始）

---

### Slide 23


- i=2，j=0

## a       a       a       a       a       b

## a       a       a       b

- S：

- T：

- 匹配成功：
- i = 6，j = 4
- 返回 i – j = 2

---

### Slide 24


- /*求从主串s的下标pos起，串t第一次出现的位置，成功返回位置序号，不成功返回-1*/
- int StrIndex(SString s,int pos, SString t) {
- int i, j, start;
- if (t.len==0)
- return(0);   /* 模式串为空串时，是任意串的匹配串 */
- start=pos;
- i=start;
- j=0;  		/* 主串从pos开始，模式串从头（0）开始 */
- while (i<s.len && j<t.len)
- if (s.ch[i]==t.ch[j]) {
- i++;
- j++;
- }   /* 当前对应字符相等时推进 */
- else {
- start++;        /* 当前对应字符不等时回溯 */
- i=start;
- j=0;   /* 主串从start+1开始，模式串从头（0）开始*/
- }
- if (j>=t.len)
- return(start);    /* 匹配成功时，返回匹配起始位置 */
- else
- return(-1);        /* 匹配不成功时，返回-1 */
- }

---

### Slide 25


- /*求从主串s的下标pos起，串t第一次出现的位置，成功返回位置序号，不成功返回-1*/
- int StrIndex(SString s,int pos, SString t) {
- int i, j;
- if (t.len==0)
- return(0);   /* 模式串为空串时，是任意串的匹配串 */
- i=pos;
- j=0;  		/* 主串从pos开始，模式串从头（0）开始 */
- while (i<s.len && j<t.len)
- if (s.ch[i]==t.ch[j]) {
- i++;
- j++;
- }   /* 当前对应字符相等时推进 */
- else {
- i=i-j+1;  /* 当前对应字符不等时回溯 */
- j=0;        /* 主串从start+1开始，模式串从头（0）开始*/
- }
- if (j>=t.len)
- return(i-j);    /* 匹配成功时，返回匹配起始位置 */
- else
- return(-1);        /* 匹配不成功时，返回-1 */
- }

- KMP

---

### Slide 26


- BF算法分析

- 算法在字符比较不相等时，需要回溯（即i=i-j+1）：即退到s中的下一个字符开始进行继续匹配。
- 最好情况下的时间复杂度为O(m)。
- 最坏情况下的时间复杂度为O(n×m)。

---

### Slide 27


- 4.3.2  KMP算法

- KMP算法是D.E.Knuth、J.H.Morris和V.R.Pratt共同提出的，简称KMP算法。
- 该算法较BF算法有较大改进，主要是消除了主串指针的回溯，从而使算法效率有了某种程度的提高。

---

### Slide 28


- BF算法

## 利用已经部分匹配这个有效信息，保持i指针不回溯
## 仅通过修改j指针，让模式串尽量地移动到有效的位置

- 人眼来优化的话

---

### Slide 29


## 当匹配失败时，j要回退。退到的位置k，存在着这样的性质：最前面的k个字符，与j未回退时它前面的最后k个字符是一样的。如果用数学公式来表示是这样的：
- P[0 ~ k-1] == P[j-k ~ j-1]

---

### Slide 30


- next

- 对于模式串T 的每个元素 tj，都存在一个实数 k ，使得模式串 T 开头的 k 个字符（t0 t1…tk-1）依次与 t j 前面的 k（tj-k tj-k+1…tj-1）个字符相等，这里第一个字符 tj-k 最多从 t1 开始，所以 k < j 。
- 如果这样的 k 有多个，则取最大的一个。
- 模式串 T 中每个位置 j 的字符都有这种信息，采用 next 数组表示，即 next[ j ]=MAX{ k }。

---

### Slide 32


## void GetNext(SString t,int next[]) {
## int j, k;
## j=0;
## k=-1;
## next[0]=-1;
## while (j<t.length-1) {
## if (k==-1 || t.data[j]==t.data[k]) {
## j++;
## k++;
## next[j]=k;
## }
## else
## k=next[k];
## }
## }

## 初始：j=0; k=-1; next[0]=-1;
## 1）j=1; k=0; next[1]=0;
## 2）t.data[1]  t.data[0]  不等   k=next[0]=-1;
## 3）j=2; k=0; next[2]=0;
## 4）t.data[2]  t.data[0]  不等   k=next[0]=-1;
## 5）j=3; k=0; next[3]=0;
## 6）t.data[3] = =t.data[0]  等
## j=4; k=1; next[4]=1;

- 示例模式串1：

---

### Slide 33


## /*求从主串s的下标pos起，串t第一次出现的位置*/
## int  StrIndex_KMP(SString s,int pos, SString t,int next[]) {
## int i, j;
## if (t.len==0)
## return(0);    /* 空串是任意字符串的子串 */
## i=pos;
## j=0;
## while (i<s.len && j<t.len)
## if (j==-1|| s.ch[i]==t.ch[j]) {     /* 主串与子串的对应字符相等，则继续比较下一字符 */
## i++;
## j++;
## }
## else
## j=next[j];  /* 发现失配字符则用next函数值更新j值，而i值不变 */
## if (j>=t.len)
## return(i- t.len);    /* 成功则返回主串的当前起始匹配位置 */
## else
## return(-1);    /* 不成功则返回-1 */
## }

- BF

---

### Slide 34


- ababcabcacbab

- abcac

- ababcabcacbab

## 0123456789ABC

- abcac

- ababcabcacbab

- j=next[2]=0

- j=next[4]=1

- abcac

- while (i<s.len && j<t.len)
- if (j==-1|| s.ch[i]==t.ch[j]){
- i++;
- j++;
- }
- else
- j=next[j];
- if (j>=t.len)
- return(i- t.len);   //10-5

- ababcabcacbab

- abcac

- ……

- ababcabcacbab

- abcac

- ……

---

### Slide 35


## void GetNext(SString t,int next[]) {
## int j, k;
## j=0;
## k=-1;
## next[0]=-1;
## while (j<t.length-1) {
## if (k==-1 || t.data[j]==t.data[k]) {
## j++;
## k++;
## next[j]=k;
## }
## else
## k=next[k];
## }
## }

## 初始：j=0; k=-1; next[0]=-1;
## 1）j=1; k=0; next[1]=0;
## 2）t.data[1]  t.data[0]  不等   k=next[0]=-1;
## 3）j=2; k=0; next[2]=0;
## 4）t.data[2]  t.data[0]  不等   k=next[0]=-1;
## 5）j=3; k=0; next[3]=0;
## 6）t.data[3] = =t.data[0]  等
## j=4; k=1; next[4]=1;
## 7）t.data[4] = =t.data[1]  等
## j=5; k=2; next[5]=2;

## 示例主串：abcaabcabcabfdcad

- 示例模式串2：

---

### Slide 36


## while (i<s.len && j<t.len)
## if (j==-1|| s.ch[i]==t.ch[j]){
## i++;
## j++;
## }
## else
## j=next[j];
## if (j>=t.len)
## return(i- t.len);   //13-6

- ……

---

### Slide 37


- KMP算法分析

- 设串S的长度为n，串T长度为m。
- 在KMP算法中求next数组的时间复杂度为O(m)，在后面的匹配中因主串s的下标不减即不回溯，比较次数可记为n，所以KMP算法时间复杂度为O(n+m)。

---

### Slide 38


## void GetNext(SString t,int next[]) {
## int j, k;
## j=0;
## k=-1;
## next[0]=-1;
## while (j<t.length-1) {
## if (k==-1 || t.data[j]==t.data[k]) {
## j++;
## k++;
## next[j]=k;
## }
## else
## k=next[k];
## }
## }//KMP

## 初始：j=0; k=-1; next[0]=-1;
## 1）j=1; k=0; next[1]=0;
## 2）t.data[1] = = t.data[0]  等
## j=2; k=1; next[2]=1;
## 3）t.data[2] = = t.data[1]  等
## j=3; k=2; next[3]=2;
## 4）t.data[3] = =t.data[2]  等
## j=4; k=3; next[4]=3;

## 示例主串：aaabaaaab

- 示例模式串3：

---

### Slide 39


- while (i<s.len && j<t.len)
- if (j==-1||s.ch[i]==t.ch[j]){
- i++;
- j++;
- }
- else
- j=next[j];
- if (j>=t.len)
- return(i- t.len);   //9-5

## 改进的KMP

---

### Slide 40


## void GetNext(SString t,int next[]) {
## int j, k;
## j=0;
## k=-1;
## next[0]=-1;
## while (j<t.length-1) {
## if (k==-1 || t.data[j]==t.data[k]) {
## j++;
## k++;
## if (t.data[j]!=t.data[k] )
## next[j]=k;
## else
## next[j]=next[k];
## }
## else
## k=next[k];
## }
## }//改进的KMP

## 初始：j=0; k=-1; next[0]=-1;
## 1）j=1; k=0; t.data[1] != t.data[0]  否
## next[1]=next[0]= -1;
## 2）t.data[1] = = t.data[0]  是
## j=2; k=1; t.data[2] != t.data[1]  否
## next[2]=next[1]= -1;
## 3）t.data[2] = = t.data[1]  是
## j=3; k=2; t.data[3] != t.data[2]  否
## next[3]=next[2]= -1;
## 4）t.data[3] = = t.data[2]  是
## j=4; k=3; t.data[4] != t.data[3]  是
## next[4]=3;

---

### Slide 41


- while (i<s.len && j<t.len)
- if (j==-1||s.ch[i]==t.ch[j]){
- i++;
- j++;
- }
- else
- j=next[j];
- if (j>=t.len)
- return(i- t.len);   //9-5

- ……

## KMP
