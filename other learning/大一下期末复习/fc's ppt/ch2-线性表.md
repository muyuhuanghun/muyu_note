# ch2-线性表


---

### Slide 1


## 第二章 线性表

## 授课教师：傅翀

---

### Slide 2


## 线性表的知识结构

- 线性表的概念

- 线性表的存储结构

---

### Slide 3


  - 线性表的概念及抽象数据类型
  - 线性表的顺序存储
  - 线性表的链式存储
  - 线性表的应用

## 本章要点

---

### Slide 4


- 2.1.1 线性表的定义

- 线性表（Linear List）是由n (n≥0)个类型相同的数据元素a1,a2,…，an组成的有限序列，记做（a1,a2,…，ai-1，ai，ai+1， …，an）。
- 数据元素之间是一对一的关系，即每个数据元素最多有一个直接前驱和一个直接后继。
- 线性表的逻辑结构图为：

---

### Slide 5


- 线性表的特点

  - 同一性：线性表由同类数据元素组成，每一个ai必须属于同一数据对象。
  - 有穷性：线性表由有限个数据元素组成，表长度就是表中数据元素的个数。
  - 有序性：线性表中相邻数据元素之间存在着 序偶关系<ai,ai+1>。

---

### Slide 6


- 2.1.2 抽象数据类型定义

  - ADT  LinearList{
  - 数据元素：D = { ai | ai∈D0, i=1,2,…，n 	n≥0 ，D0为某一数据对象 }
  - 关系：        Ｓ＝ { <ai,ai+1> | ai, ai+1∈D0，i=1,2, …,n-1 ｝
  - 基本操作：
  - 1）InitList（L）     操作前提：L为未初始化线性表。操作结果：将L初始化为空表。
  - 2）DestroyList(L) 操作前提：线性表L已存在。 操作结果：将L销毁。
  - 3）ClearList(L)      操作前提：线性表L已存在 。操作结果：将表L置为空表。
  - ………
  - }ADT  LinearList

---

### Slide 7


  - 线性表的概念及抽象数据类型
  - 线性表的顺序存储
  - 线性表的链式存储
  - 线性表的应用

## 本章要点

---

### Slide 8


- 线性表的逻辑表示为：

## (a1，a2，…，ai，ai+1，…，an)

- ai（1≤i≤n）表示第i（i表示逻辑位序）个元素。

- 2.1 线性表的逻辑结构

---

### Slide 9


- 顺序存储结构示意图

- 采用顺序存储结构的线性表通常称为顺序表

- 通过数据元素物理存储的相邻关系来反映数据元素之间逻辑上的相邻关系

- 关系线性化
- 结点顺序存

---

### Slide 10


- 顺序存储结构的C语言定义

  - #define	MAXSIZE 100                    /*线性表可能达到的最大长度*/
  - typedef  struct
  - {
  - ElemType  elem[MAXSIZE]；      /*线性表占用的数组空间*/
  - int  last；  /*记录线性表中最后一个元素在数组elem[ ]中的位置(下标值)，
  - 空表置为-1。注意，数组中实际存储的元素个数为 last+1 */
  - } SeqList；
## 注意区分元素的序号和数组的下标，如a1的序号为1，而其对应的数组下标为0。
## SeqList  L1, *L；      L = &L1;

---

### Slide 11


## 2.2.2 线性表顺序存储结构的基本运算

## 查找操作
## 插入操作
## 删除操作
## 顺序表合并算法

---

### Slide 12


- 查找操作

## 线性表的两种基本查找运算
## 按序号查找 GetData( L, i ) ：要求查找线性表L中第i个数据元素，其结果是
  - L.elem[i-1] 或 L->elem[i-1]
## 按内容查找 Locate( L, e ) ：要求查找线性表L中与给定值e相等的数据元素，其结果是：
  - 若在表L中找到与e相等的元素，则返回该元素在表中的序号；
  - 若找不到，则返回一个“空序号”，如-1。

---

### Slide 13


- 线性表的查找运算

## int  Locate(SeqList L，ElemType e) {
## i=0 ;                  /*i为扫描计数器，初值为0，即从第一个元素开始比较*/
## while ((i<=L.last)&&(L.elem[i]!=e) )
## i++;            /*顺序扫描表，直到找到值为e的元素，或扫描到表尾而没找到*/
## if  (i<=L.last)
## return(i);    /*若找到值为e的元素，则返回其序号*/
## else
## return(-1);  /*若没找到，则返回空序号*/
## }
## /*算法的时间复杂度为O(n)*/

---

### Slide 14


- 插入操作

- 线性表的插入运算是指在表的第 i (1≤i≤n+1)个位置，插入一个新元素 e
  - 使长度为n的线性表 (e1，…，ei-1，ei，…，en)
  - 变成长度为n+1的线性表（e1，…,ei-1，e，ei，…，en）。

---

### Slide 15


## 插入算法示意图

## 已知：线性表 (4,9,15,28,30,30,42,51,62)，需在第4个元素之前插入一个元素“21”。则需要将第9个位置到第4个位置的元素依次后移一个位置，然后将“21”插入到第4个位置

---

### Slide 16


## 插入运算

## #define OK 1
## #define ERROR 0
## int  InsList(SeqList *L,int i,ElemType e) {
## int k;
## if( (i<1) || (i>L->last+2) ) {     /*首先判断插入位置是否合法*/
## printf(“插入位置i值不合法”)；
## return(ERROR);   }
## if(L->last>=MAXSIZE-1) {
## printf(“表已满无法插入”)；
## return(ERROR);   }
## for(k=L->last;k>=i-1;k--)     /*为插入元素而移动位置*/
## L->elem[k+1]=L->elem[k];
## L->elem[i-1]=e;         /*在C语言中数组第i个元素的下标为i-1*/
## L->last++;
## return(OK);
## }

---

### Slide 17


## 算法分析

- 对于本算法来说，元素移动的次数不仅与表的实际长度有关，而且与插入位置i有关：
  - 当I = last+2 时，移动次数为 0 ；
  - 当I = 1 时，移动次数为 last+1（线性表的实际长度），达到最大值。

## 算法最好时间复杂度

## 算法最坏时间复杂度

---

### Slide 18


- 18

## 此时需要将ai～an的元素均后移一个位置，共移动 n-i+1 个元素。

## 因此插入算法的平均时间复杂度为O(n)。

- 所以在长度为n的线性表中插入一个元素时所需移动元素的平均次数为：

- 算法分析

---

### Slide 19


- 删除操作

- 线性表的删除运算是指将表的第i(1≤i≤n)个元素删去，
  - 使长度为n的线性表  (e1，…,ei-1，ei，ei+1，…，en)
  - 变成长度为n-1的线性表(e1，…,ei-1， ei+1，…，en)。

---

### Slide 20


- 删除算法示意

## 将线性表(4,9,15,21,28,30,30,42,51,62)中的第5个元素删除。

---

### Slide 21


## 删除算法

## /*在顺序表L中删除第i个数据元素，并用指针参数e返回其值*/
## int  DelList(SeqList *L,int i, ElemType *e) {
## int k;
## if((i<1)||(i>L->last+1)) {
## printf(“删除位置不合法！”);
## return(ERROR);
## }
## *e = L->elem[i-1];        /* 将删除的元素存放到e所指向的变量中*/
## for(k=i;k<=L->last;k++)
## L->elem[k-1]= L->elem[k];         /*将后面的元素依次前移*/
## L->last--;
## return(OK);
## }

---

### Slide 22


## a1　　a2　　…　　ai	ai+1      …　 an

## 此时需要将ai+1～an的元素均前移一个位置，共移动 n-(i+1)+1 = n-i 个元素。

- 所以在长度为n的线性表中删除一个元素时所需移动元素的平均次数为：

## 因此删除算法的平均时间复杂度为O(n)。

- 算法分析

---

### Slide 23


- 合并算法

## 已知 ：有两个顺序表LA和LB，其元素均为非递减有序排列，编写一个算法，将它们合并成一个顺序表LC，要求LC也是非递减有序排列。
## 算法思想 ：
  - 设表LC是一个空表，设两个指针i、j分别指向表LA和LB中的元素，
  - 若LA.elem[i]>LB.elem[j]，则当前先将LB.elem[j]插入到表LC中，
  - 若LA.elem[i]≤LB.elem[j] ，当前先将LA.elem[i]插入到表LC中，
  - 如此进行下去，直到其中一个表被扫描完毕，然后再将未扫描完的表中剩余的所有元素放到表LC中。

---

### Slide 24


- 顺序表的合并算法

## 已知 ：有两个顺序表LA和LB，其元素均为非递减有序排列，编写一个算法，将它们合并成一个顺序表LC，要求LC也是非递减有序排列。

- 例如，LA=（2，2，3），LB＝（1，3，3，4），其二路合并过程如下：

- LA：2　2　3

- LB：1　3　3　4

## 较小者复制到LC

- LC：

- 1

- 2

- 2

- 3

- 3

- 3

- 4

---

### Slide 25


- void merge(SeqList *LA,  SeqList *LB,  SeqList *LC){   /* 顺序表的合并算法 */
- int i,j,k,l;
- i=0;j=0;k=0;
- while(i<=LA->last&&j<=LB->last)    /* 只要有一个表被遍历了就结束循环 */
- if(LA->elem[i]<=LB->elem[j]) {
- LC->elem[k]= LA->elem[i];
- i++;  k++;    }
- else {
- LC->elem[k]=LB->elem[j];
- j++;  k++;     }
- while(i<=LA->last) {	/* 当表LA有剩余元素，则将余下的元素赋给表LC */
- LC->elem[k]= LA->elem[i];
- i++;  k++;    }
- while(j<=LB->last) {  	/* 当表LB有剩余元素，则将余下的元素赋给表LC */
- LC->elem[k]= LB->elem[j];
- j++;  k++;    }
- LC->last=LA->last+LB->last+1;
- }

## 算法的时间复杂度 O(LA->last+LB->last)

- 单链表合并算法

---

### Slide 26


## 例如，LA=（2，2，3），LB＝（1，3，3，4），其二路合并过程如下：

## LA：2　2　3

## LB：1　3　3　4

## 较小者复制到LC

## LC：

## 1

## 2

## 2

## 3

## 3

## 3

## 4

- while(i<=LA->last&&j<=LB->last)
- if(LA->elem[i]<=LB->elem[j]) {
- LC->elem[k]= LA->elem[i];
- i++;  k++;    }
- else {
- LC->elem[k]=LB->elem[j];
- j++;  k++;     }

- while(i<=LA->last) {
- LC->elem[k]= LA->elem[i];
- i++;  k++;    }
- while(j<=LB->last) {
- LC->elem[k]= LB->elem[j];
- j++;  k++;    }
- LC->last = LA->last + LB->last + 1;

---

### Slide 27


- 顺序存储结构的优点和缺点

## 优点：
  - 无需为表示结点间的逻辑关系而增加额外的存储空间；
  - 可方便地随机存取表中的任一元素。
## 缺点：
  - 插入或删除运算不方便，除表尾的位置外，在表的其它位置上进行插入或删除操作都必须移动大量的结点，其效率较低；
  - 由于顺序表要求占用连续的存储空间，存储分配只能预先进行静态分配。因此当表长变化较大时，难以确定合适的存储规模。

---

### Slide 28


## 以下关于线性表的说法中，正确的是

## 线性表中的元素必须是相同数据类型的。

## 线性表只能采用顺序存储结构来实现。

## 在线性表中，除了第一个元素外，每个元素都有且仅有一个前驱元素。

## 线性表的长度是固定的，一旦创建就不能改变。

- A

- B

- C

- D

- 提交

- 可为此题添加文本、图片、公式等解析，且需将内容全部放在本区域内。

- 解析：A选项正确，线性表中的元素必须是相同数据类型的，这是线性表定义的基本要求。
- B选项错误，线性表可以采用顺序存储结构（如数组）或链式存储结构（如链表）来实现。
- C选项错误，在线性表中，第一个元素没有前驱元素，最后一个元素没有后继元素，其他每个元素都有且仅有一个前驱元素和一个后继元素。
- D选项错误，线性表的长度可以是动态的，根据实际需要可以增加或减少元素，从而改变线性表的长度。

---

### Slide 29


- 2.3  线性表的链式存储

- 采用链式存储结构的线性表称为链表 。
- 设计链式存储结构时，每个逻辑结点存储单独存储，为了表示逻辑关系，增加指针域。

- 每个物理结点增加一个指向后继结点的指针域  单链表。
- 每个物理结点增加一个指向后继结点的指针域和一个指向前驱结点的指针域 双链表。

---

### Slide 30


## 线性表
## (a1，a2，…，ai，…an )

## 映射

## 逻辑结构

## …

## L

## 带头结点单链表示意图

- 2.3.1  单链表

## 不带头结点单链表示意图

---

### Slide 31


- 单链表的示例图

## 存储结构

---

### Slide 32


- 第一个结点的操作和表中其他结点的操作相一致，无需进行特殊处理；
- 无论链表是否为空，都有一个头结点，因此空表和非空表的处理也就统一了。

## 单链表增加一个头结点的优点如下：

- 带头结点单链表

---

### Slide 33


- 当访问过一个结点后，只能接着访问它的后继结点，而无法访问它的前驱结点。

## a

## b

- …

- …

- 单链表的特点

---

### Slide 34


## 存储密度是指结点数据本身所占的存储量和整个结点结构中所占的存储量之比：

- 一般地，存储密度越大，存储空间的利用率就越高。
- 显然，顺序表的存储密度为1（100%），而链表的存储密度小于1。

---

### Slide 35


- 单链表的存储结构描述

- typedef struct Node {      / * 结点类型定义 * /
- ElemType data；
- struct Node  *next；
- }Node, *LinkList；            /* LinkList为结构指针类型*/

## LinkList 和 Node * 同为结构指针类型
## LinkList 一般用作单链表的头指针变量
## Node * 一般用作指向单链表中结点的指针

---

### Slide 36


- LinkList L

- L指向单链表的第一个结点
  - 若 L ==NULL，表示单链表为一个空表
  - 非空表，则 L 指向第一个元素结点（首元结点）
- L指向单链表的头结点
  - 若 L->next ==NULL，表示单链表为一个空表
  - 非空表，则 L->next 指向首元结点

---

### Slide 37


- 2.3.2 初始化单链表

- void init_linklist(LinkList *L) {          /* L 实际上是二重指针 */
- *L=(LinkList)malloc(sizeof(Node));
- /* 申请结点空间，建立头结点 */
- (*L)->next=NULL;                   /* 建立空的单链表 */
- }

---

### Slide 38


- 头插法建表

- 从一个空表开始，创建一个头结点。
- 依次读取字符数组a中的元素，生成新结点
- 将新结点插入到当前链表的表头上，直到结束为止。

- 注意：链表的结点顺序与逻辑次序相反。

---

### Slide 39


  - void CreateFromHead(LinkList   L) {
  - Node   *s;
  - char	c;
  - int flag=1;
  - while(flag) {   /* flag初值为1，当输入"$"时，置flag为0，建表结束*/
  - c=getchar();
  - if(c!='$') {
  - s=(Node*)malloc(sizeof(Node)); /*建立新结点s*/
  - s->data=c;
  - s->next=L->next;       /*将s结点插入表头*/
  - L->next=s;
  - }
  - else
  - flag=0;
  - }
  - }

---

### Slide 40


- 尾插法建表

- 注意：链表的结点顺序与逻辑次序相同。

- 从一个空表开始，创建一个头结点。
- 依次读取字符数组a中的元素，生成新结点
- 将新结点插入到当前链表的表尾上，直到结束为止。

---

### Slide 41


## void CreateFromTail(LinkList L){   /* flag初值为1，当输入“$”时，flag为0，建表结束 */
## Node *r, *s;
## char c;
## int   flag =1;
## r=L;                  /* r 指针动态指向链表的当前表尾*/
## while(flag)
## c=getchar();
## if(c!='$') {
## s=(Node*)malloc(sizeof(Node));
## s->data=c;
## r->next=s;
## r=s;
## }
## else {
## flag=0;
## r->next=NULL;   /*将最后一个结点的next链域置为空，表示链表的结束*/
## }
## }
## }

---

### Slide 42


## 单链表查找：按序号

## Node * Get (LinkList  L, int i) {   /* 在带头结点的单链表L中查找第i个结点 */
## /* 若找到(1≤i≤n)，则返回该结点的存储位置; 否则返回NULL */
## int j;
## Node  *p;
## p=L;
## j=0;   /*从头结点开始扫描*/
## while (( p->next!=NULL) && (j<i) ) {
## p=p->next;      /* 扫描下一结点*/
## j++;                  /* 已扫描结点计数器 */
## }
## if(i == j)
## return p;          /* 找到了第i个结点 */
## else
## return NULL;   /* 找不到，i≤0或i>n */
## }

## 算法的时间复杂度为 O(n)

---

### Slide 43


## /* 在带头结点的单链表L中查找其结点值等于key的结点 */
## Node *Locate( LinkList L,ElemType key) { /* 若找到则返回该结点的位置p，否则返回NULL */
## Node *p;
## p=L->next;      /* 从表中第一个结点比较 */
## while (p!=NULL)
## if (p->data!=key)
## p=p->next;
## else
## break;     /* 找到结点key，退出循环 */
## return p;
## }

## 单链表查找：按值

## 算法的时间复杂度为 O(n)

---

### Slide 44


## int ListLength(LinkList L) {   /* 求带头结点的单链表L的长度 */
## Node *p;
## int j;
## p=L->next;
## j=0;           /* 用来存放单链表的长度 */
## while(p!=NULL) {
## p=p->next;
## j++;
## }
## return j;   /*j为求得的单链表长度*/
## }

## 求单链表的长度

## 算法的时间复杂度为 O(n)

---

### Slide 45


- int InsList(LinkList L,int i,ElemType e)｛
- /* 在带头结点的单链表L中第i个位置插入值为e的新结点 */
- Node *pre,*s;
- int k;
- pre=L;
- k=0;    /* 从头开始，查找第i-1个结点 */
- while(pre!=NULL&&k<(i-1)) {
- pre=pre->next;
- k++; //k=i-2时，pre指向i-1
- }  /* 查找第i-1结点 */
- if(pre==NULL)
- printf("插入位置不合理!");
- return ERROR;
- }
- s=(Node*)malloc(sizeof(Node));
- s->data=e;
- s->next=pre->next;
- pre->next=s;
- return OK;
- }

## 单链表插入操作

## 若单链表有m个结点，插入位置为m+1时，则是在尾部插入结点

## 双向链表前插

---

### Slide 46


## 单链表删除

- int DelList(LinkList L,int i,ElemType *e) {
- /* 在带头结点的单链表L中删除第i个元素，并将删除的元素保存到变量*e中 */
- Node *pre,*r;
- int k;
- pre=L;
- k=0;
- while(pre->next!=NULL && k<i-1) {
- pre=pre->next;
- k=k+1;
- } /* 查找第i-1结点 */
- if((pre->next) ==NULL) {
- printf("删除结点的位置i不合理!");
- return ERROR;
- }
- r=pre->next;
- pre->next=pre->next->next;  /*修改指针，删除结点r*/
- *e = r->data;
- free(r);    /*释放被删除的结点所占的内存空间*/
- printf("成功删除结点!");
- return OK;
- }

---

### Slide 47


- 两个有序单链表的合并

## 有两个单链表LA和LB，其元素均为非递减有序排列，编写一个算法，将它们合并成一个单链表LC，要求LC也是非递减有序排列。
  - 要求：新表LC利用现有的表LA和LB中的元素结点空间，而不需要额外申请结点空间。
  - 例如LA=(2, 2, 3), LB=(1, 3, 3, 4), 则LC=(1, 2, 2, 3, 3, 3, 4)
## 算法描述：要求利用现有的表LA和LB中的结点空间来建立新表LC
  - 可通过更改结点的next域来重建新的元素之间的线性关系，为保证新表仍然递增有序
  - 可以利用尾插入法建立单链表的方法，只是新建表中的结点不用malloc
  - 只需要从表LA和LB中选择合适的点插入到新表LC中即可

---

### Slide 48


- LinkList  MergeLinkList(LinkList LA, LinkList LB) {   /* MergeLinkList */
- Node *pa,*pb;
- LinkList LC；
- pa=LA->next;
- pb=LB->next;
- LC=LA;                  /* LA的表头赋给LC */
- LC->next=NULL;  /*LC初始化为空表*/
- r=LC;                     /*r始终指向LC的表尾*/
- /*当两个表中均未处理完时，比较选择将较小值结点插入到新表LC中 */
- while( pa!=NULL && pb!=NULL ) {
- if(pa->data<=pb->data){
- r->next=pa;  r=pa;  pa=pa->next;   }
- else{
- r->next=pb;  r=pb; pb=pb->next;  }
- }
- if(pa)  /* 若表LA未完，将表LA中后续元素链到新表LC表尾 */
- r->next=pa;
- else	 /* 否则将表LB中后续元素链到新表LC表尾 */
- r->next=pb;
- free(LB);
- return(LC);
- }

- 顺序表的合并算法

---

### Slide 49


- 2.3.3  循环链表

- 循环链表(Circular Linked List) 是一个首尾相接的链表。

- 线性表
- (a1，a2，…，ai，…an)

## 映射

## 逻辑结构

## 存储结构

## a1

## a2

## an

## …

## CL

## 带头结点循环单链表示意图

---

### Slide 50


## 链表中没有空指针域
## p所指结点为尾结点的条件：p->next==L

## 与非循环单链表相比，循环单链表：

- 循环链表

---

### Slide 51


## 在用头指针表示的循环链表中
  - 找 开始结点a1 的时间复杂度是 O(1)
  - 找 终端结点an 的时间复杂度是 O(n)
## 在用尾指针表示的循环链表中
  - 找 开始结点a1 的时间复杂度是 O(1)
  - rear ->next ->next
  - 找 终端结点an 的时间复杂度是 O(1)
  - rear

- 带尾指针的循环链表

---

### Slide 52


- 初始化循环单链表

## void initClinklist(LinkList *CL) {  /* CL是循环单链表的头指针变量 */
## *CL = (LinkList)malloc(sizeof(Node));   /* 建立头结点 */
## (*CL) -> next = *CL ;                   /*置为空表*/
## }

## CL

---

### Slide 53


## void CreateClinklist (LinkList CL){   /* CL已经初始化，当输入 $ 时，建表结束 */
## Node *rear, *s;
## char c;
## rear = CL;           /* rear 指针动态指向链表的当前表尾 */
## c=getchar();       /* 读入第一个元素 */
## while(c!='$’) {
## s = (Node*)malloc(sizeof(Node));
## s->data = c;
## rear->next = s;
## rear = s;
## c=getchar();
## }
## rear->next = CL;   /*将最后一个结点的next链域指向头结点*/
## }

## 建立循环单链表

- rear

- CL

- c1

- ci-1

- …

- ci

- s

---

### Slide 54


- 循环单链表合并为一个循环单链表

## 已知：有两个带头结点的循环单链表LA、LB，编写一个算法，将两个循环单链表合并为一个循环单链表，其头指针为LA。
## 算法思想：
  - 先找到两个链表的尾，并分别由指针p、q指向它们
  - 然后将第一个链表的尾与第二个表的第一个结点链接起来
  - 修改第二个表的尾q，使它的链域指向第一个表的头结点

---

### Slide 55


## LinkList   merge_1(LinkList LA,LinkList LB) {
## Node *p, *q;
## p=LA;
## q=LB;
## while (p->next!=LA)
## p=p->next;	   /*找到表LA的表尾，用p指向它*/
## while (q->next!=LB)
## q=q->next;	   /*找到表LB的表尾，用q指向它*/
## q->next=LA;	   /*修改表LB 的尾指针，使之指向表LA 的头结点*/
## p->next=LB->next;  /*修改表LA的尾指针，使之指向表LB 中的第一个结点*/
## free(LB);
## return(LA);
## }

## 采用头指针合并

## a1

## an

## …

## b1

## bm

## …

## LA

- p

- q

## 需要遍历链表，找到表尾
## 算法的时间复杂度为 O(n)

---

### Slide 56


## 采用尾指针合并

## /*此算法将两个采用尾指针的循环链表首尾连接起来*/
## LinkList  merge_2(LinkList RA,LinkList RB) {
## Node *p;
## p=RA->next;        /* 保存链表RA的头结点地址 */
## RA->next=RB->next->next;   /* 链表RB的开始结点链到链表RA的终端结点之后*/
## free(RB->next);    /* 释放链表RB的头结点 */
## RB->next=p;         /* 链表RA的头结点链到链表RB的终端结点之后 */
## return  RB;             /* 返回新循环链表的尾指针 */
## }

## 算法的时间复杂度为 O(1)

---

### Slide 57


- 2.3.4  双向链表

- 线性表
- (a1，a2，…，ai，…an )

## 映射

## 逻辑结构

## 存储结构

- a1

- an

- ∧

## …

## L

## 带头结点双链表示意图

- a2

---

### Slide 58


- 双向链表

## 双向链表的结构定义：
## typedef struct Dnode  {
## ElemType data；
## struct DNode  *prior，*next；
## } DNode,	* DoubleList；

- 从任一结点出发可以快速找到其前驱结点和后继结点；
- 从任一结点出发可以访问其他结点。

---

### Slide 59


- 线性表
- (a1，a2，…，ai，…an)

## 映射

## 逻辑结构

## 存储结构

- a1

- a2

- an

## …

## L

## 带头结点双向循环链表

- 双向循环链表

- 空的双向循环链表

---

### Slide 60


## 链表中没有空指针域
## p所指结点为尾结点的条件：p->next == L
## 一步操作即 L->prior 可以找到尾结点

## 与非循环双链表相比，循环双链表：

## L

- 双向循环链表

---

### Slide 61


- 双向链表的前插操作

## 操作语句：
##  s->prior = p->prior
##  p->prior ->next = s
##  s->next = p
##  p->prior = s

## a

## b

## c

## …

## p

## s

## 

## 

## 

## 

## …

## 单链表插入

---

### Slide 62


- 双向链表的前插操作

## a

## b

## c

## …

## p

## s

## 

## 

## 

## 

## …

## 单链表插入

- 操作语句：
-  s->next = p->next
-  p->next->prior = s
-  s->prior = p
-  p->next = s

---

### Slide 63


- int DlinkIns(DoubleList L,int i,ElemType e) {
- DNode  *s,*p;
- int k;
- p=L;
- k=0;                     /*从"头"开始，查找第i个结点*/
- while(p!=NULL&&k<i) {     /*找到p指向第i个结点*/
- p=p->next;
- k++;
- }
- if(p==NULL) {      /*如当前位置p为空表已找完还未数到第i个，说明插入位置不合理*/
- printf("插入位置不合理!");
- return ERROR;
- }
- s=(DNode*)malloc(sizeof(DNode));
- if (s)	{
- s->data=e;
- s->prior=p->prior;
- p->prior->next=s;
- s->next=p;
- p->prior=s;
- return OK;
- }
- else
- return ERROR;
- }

## i-1

## i

## e

## …

## p

## s

## 

## 

## 

## 

## …

---

### Slide 64


## 双向链表的删除操作

## 算法描述：欲删除双向链表中的第i个结点，则指针的变化情况如图所示。

## a

## b

## c

## p

## …

---

### Slide 65


- int DlinkDel(DoubleList L,int i,ElemType *e) {
- DNode  *p;
- int k;
- p=L;
- k=0;                     /*从"头"开始，查找第i个结点*/
- while(p!=NULL && k<i) {  /* 找到p指向第i个结点 */
- p=p->next;
- k++;
- }
- if(p==NULL)  {
- return ERROR;
- }
- else	{
- *e=p->data;
- p->prior->next=p->next;
- p->next->prior=p->prior;
- free(p);
- return OK;
- }
- }

## a

## b

## c

## p

## …

---

### Slide 66


- 2.4  一元多项式的表示及相加

- 一元多项式可按升幂的形式写成：
  - Pn(x) = p0+p1x1+p2x2+…+pnxn
  - 其中 pi 是指数 i 的项的系数
- 假设 Qm(x) 是一个一元多项式，则它也可以用一个线性表Q来表示。即：
  - Q= (q0，q1，q2， …，qm )
- 若假设m<n，则两个多项式相加的结果
  - Rn(x)= Pn(x) + Qm(x)，也可以用线性表R来表示：
  - R=(p0+q0，p1+ q1,，p2+ q2，…，pm+ qm ，pm+1，…，pn)

---

### Slide 67


- 一元多项式的存储

## 一元多项式可以利用线性表来处理，其存储方式：
  - 顺序存储
  - 链式存储

---

### Slide 68


- 2026/3/4

- 68

- 一元多项式的顺序存储-方法1

## 一元多项式Pn(x)的顺序表示有两种：
## 方法1：只存储该一元多项式各项的系数，每个系数所对应的指数项则隐含在存储系数的顺序表的下标中。
## 采用这种存储方法使得多项式的相加运算的算法定义十分简单，只需将下标相同的单元的内容相加即可。
## 适合于存储表示非零系数多的多项式。

- p0

- p1

- …

- pi

- …

- pn

## 数组p

## Pn(x) = p0+p1x1+…+pixi+…+pnxn

---

### Slide 69


- 2026/3/4

- 69

- 一元多项式的顺序存储-方法2

## 方法2：采用只存储非零项的方法，此时每个非零项需要存储：非零项系数和非零项指数。
## 适合存储表示非零项少的多项式。

## Pn(x) = p1x1+pixi+pjxj+pkxk

- 非零项系数

- 非零项指数

## 数组p

- ……

---

### Slide 70


- 2026/3/4

- 70

- 一元多项式的链式存储表示

## 在链式存储中，对一元多项式只存非零项，则该多项式中每一非零项由两部分构成（指数项和系数项），用单链表存储表示的结点结构为：

- struct Polynode 	{
- int coef;
- int exp;
- Polynode *next;
- } Polynode , * Polylist;

---

### Slide 71


- 建立一元多项式链式存储的算法

## 【算法思想】
  - 通过键盘输入一组多项式的系数和指数
  - 用尾插法建立一元多项式的链表
  - 以输入系数0为结束标志，并约定建立多项式链表时，总是按指数从小到大的顺序排列。

---

### Slide 72


- 72

## Polylist  PolyCreate() {
## Polynode *head, *rear, *s;
## int c,e;
## head =(Polynode *)malloc(sizeof(Polynode)); /* 建立多项式的头结点 */
## rear=head;   	             /* rear 始终指向单链表的尾 */
## scanf(“%d,%d”,&c,&e);   /*键入多项式的系数和指数项*/
## while(c!=0) {	            /*若c=0，则代表多项式的输入结束*/
## s=(Polynode*)malloc(sizeof(Polynode));	/*申请新的结点*/
## s->coef=c ;
## s->exp=e ;
## rear->next=s ;	                 /*在当前表尾做插入*/
## rear=s;
## scanf(“%d,%d”,&c,&e);
## }
## rear->next=NULL;/*将表的最后一个结点的next置NULL，以示表结束*/
## return(head);
## }

---

### Slide 73


- 1

- 7

- 22

- 8

- 8

## ∧

- 9

## polyb

## 一元多项式的相加（单链表）

## A(x) = 7 + 3x + 9x8 + 5x17

## B(x) = 8x +22x7 - 9x8

---

### Slide 74


- 一元多项式的相加（单链表）

## 运算规则：
  - 两个多项式中所有指数相同的项的对应系数相加，若和不为零，则构成“和多项式”中的一项；
  - 所有指数不相同的项均复抄到“和多项式”中。
## 算法实现
  - 若p->exp<q->exp，则p所指的结点应是“和多项式”中的一项，令指针p后移
  - 若p->exp>q->exp，则q所指的结点应是“和多项式”中的一项，将结点q插入在结点p之前，且令指针q在原来的链表上后移；
  - 若p->exp=q->exp，则将两个结点中的系数相加
    - 当和不为零时修改结点p的系数域，释放q结点；
    - 若和为零，则和多项式中无此项，从A中删去p结点，同时释放p和q结点。

---

### Slide 75


- /*此函数用于将两个多项式相加，然后将和多项式存放在多项式polya中，并将多项式ployb删除*/
- void  PolyAdd(Polylist polya, Polylist polyb) {
- Polynode  *p, *q, *tail, *temp;
- int sum;
- p=polya->next;  /*令 p 指向polya多项式链表中的第一个结点*/
- q=polyb->next;  /*令 q 指向polyb多项式链表中的第一个结点*/
- tail=polya;           /* tail指向和多项式的尾结点*/
- while (p!=NULL && q!=NULL) {   /*当两个多项式均未扫描结束时*/
- if  (p->exp < q->exp) {   /*则p所指的结点放入和多项式*/
- tail->next=p;
- tail=p;
- p=p->next;
- }
- else if ( p->exp == q->exp) {  /*若指数相等，则相应的系数相加*/
- sum=p->coef + q->coef;
- if (sum != 0) {
- p->coef=sum;
- tail->next=p;
- tail=p;
- p=p->next;

---

### Slide 76


- temp=q;
- q=q->next;
- free(temp);   /*删除结点q的同一指数结点*/
- }
- else {       /*若系数和为零，则删除结点p与q，并将指针指向下一个结点*/
- temp=p;
- p=p->next;
- free(temp);
- temp=q;
- q=q->next;
- free(temp);
- }
- }
- else {   /*则q所指的结点放入和多项式*/
- tail->next=q;
- tail=q;
- q = q->next;
- }
- }
- if(p!=NULL)  /*多项式A中还有剩余，则将剩余的结点加入到和多项式中*/
- tail->next=p;
- else               /*否则，将B中的结点加入到和多项式中*/
- tail->next=q;
- }

---

### Slide 77


- 线性表链式存储方式的比较

---

### Slide 78


- 例2.6

## 设计一个高效的算法，从顺序表L中删除所有值为x的元素，并要求算法的时间复杂度为O(n)，空间复杂度为O（1）。
  - i 记录原表的位置；
  - j 记录新表将要放数据的位置
  - 若L->elem[i] != x，L->elem[j]=L->elem[i]，然后i++，j++；
    - 若L->elem[j] == x，则j++，继续向后找，直到找到值非x的元素并将其移入到L->elem[i]，然后i++，j++；
  - 直到表末尾。

---

### Slide 79


## void   delx(SeqList  *L, ElemType x) {
## int i, j ;
## i=0;
## j=0;
## while(i<=L->last)
## if(L->elem[i]!=x){
## L->elem[j]=L->elem[i]; /* 建立没有 x 的新表 */
## i++;
## j++;
## }
## else i++; /* 过滤掉 x 的数据项 */
## L->last=j-1;
## }

---

### Slide 80


- 例2.7 带头结点单链表的就地逆置问题

## 逆置就是使得表中内容由原来的（a1,a2,…，ai-1，ai，ai+1， …，an）变为（an,an-1,…，ai+1，ai，ai-1， …，a1）。
## 就地逆置就是不需要额外申请结点空间，只需要利用原有的表中的节点空间。
## 若对顺序表中的元素进行逆置，可以借助于“交换”前后相应元素；
## 对单链表中的元素进行逆置，则不能按“交换”思路，因为对于链表中第i个结点需要顺链查找第n-i+1(链表长度为n)个结点，逆置链表的时间复杂度将达O(n2)

---

### Slide 81


- 例2.7

## 算法思路：逆置后的单链表初始为空，表中的结点不是新生成的，而是从原链表中依次“删除”，再逐个头插入到逆置表中（类同算法2.5头查法创建链表）。
## 设逆置链表的初态为空表，“删除”已知链表中的第一个结点，然后将它“插入”到逆置链表的“表头”，即使它成为逆置链表中“新”的第一个结点，如此循环，直至原链表为空表止。

## a1

## a2

## an

## ∧

## …

## L

## p

## q

## an

## an-1

## a1

## ∧

## …

---

### Slide 82


## void  ReverseList(LinkList  L) {
## Node *p, *q;
## p=L->next;
## /* P为原链表的当前处理结点*/
## L->next=NULL;
## /*逆置单链表初始为空表*/
## while(p!=NULL) {
## /*当原链表未处理完*/
## q=p->next；
## p->next=L->next;
## L->next=p;
## p=q;
## /*p指向下一个待插入的结点*/
## }
## }

## 例2.7 带头结点单链表的就地逆置

## a1

## ∧

## a2

## an

## ∧

## …

## L

## p

## q

## a3

## a4

## a1

## ∧

## a2

## an

## ∧

## …

## L

## p

## q

## a3

## a4

## a1

## ∧

## a2

## an

## ∧

## …

## L

## p

## q

## a3

## a4

---

### Slide 83


- 例2.8

## 已知带头结点单链表L，设计算法实现：以表中第一元素作为标准，将表中所有值小于第一个元素的结点均放在第一结点之前，所有值大于第一元素的结点均放在第一元素结点之后。
## 可以在单链表L中，找到值小于第一个结点元素值的结点的前驱结点pre，删除pre->next对应的结点p，之后将被删除的结点p插入到头结点L之后，这样避免每次要记录待插入位置的前驱。

---

### Slide 84


- void changelist(LinkList L) {
- Node *p1, *pre,*p, *q;
- if（L->next==NULL）
- return ERROR；
- p1=L->next;     /*p1指向表中第一元素*/
- pre=p1;
- p=p1->next;
- while（p）{
- q=p->next;
- if( p->data >= p1->data){
- pre=p;
- p=q;
- }
- else{
- pre->next =p->next;
- p->next=L->next;
- L->next=p;
- p=q ;
- }
- }
- }

## a4

## pre

## 6

## 9

## an

## ∧

## …

## L

## p1

## 5

## q

---

### Slide 85


- 例2.9

- 建立一个带头结点的线性链表，用以存放输入的二进制数，链表中每个结点的data域存放一个二进制位。并在此链表上实现对二进制数加1的运算 。
- ①建链表：带二进制数可用带头结点的单链表存储，第一个结点存储二进制数的最高位，依次存储，最后一个结点存储二进制数的最低位。
- ②二进制加法规则：实现二进制数加1运算，方向从低位往高位找到第一个值为0的位，从该位开始，对后面所有低位进行求反运算。

---

### Slide 86


- 例2.9

- ③链表实现二进制加1时，从高位往低位与运算方向正好相反，从第一个结点开始找，找出最后一个值域为0的结点，把该结点值域赋为1，其后所有结点的值域赋为0。
- ④若在链表中未找到值域为0的结点，则表示该二进制数各位均为1，此时，申请一新结点，值域为1，插入到头结点与原链表的第一个结点之间，成为新链表的第一个结点，其后所有结点的值域赋为0。

---

### Slide 87


## void BinAdd(LinkList  L) {
## Node *q,*r,*temp,*s;
## q=L->next;
## r=L;
## while(q!=NULL) {  /*查找最后一个值域为0的结点*/
## if(q->data == 0)
## r = q;
## q = q->next;
## } /*如果找不到值域为0的结点，说明全1，则r=L */

- 例2.9

---

### Slide 88


## if  (r != L)
## r->data = 1;   /* 将最后一个值域为0的结点的值域赋为1 */
## else {                   /* 未找到值域为0的结点，头插新结点 */
## temp = r->next;
## s=(Node*)malloc(sizeof(Node));      /*申请新结点*/
## s->data=1;                       /*值域赋为1*/
## s->next=temp;
## r->next = s;                     /*插入到头结点之后*/
## r = s;
## }
## r = r->next;
## while(r!=NULL) {               /*将后面的所有结点的值域赋为0*/
## r->data = 0;
## r = r->next;
## }
## }/*BinAdd结束*/
