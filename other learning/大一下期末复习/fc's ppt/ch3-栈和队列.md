# ch3-栈和队列


---

### Slide 1


## 第三章 栈和队列

## 授课教师：傅翀

---

### Slide 2


  - 栈
  - 队列

## 本章要点

---

### Slide 3


- 3.1  栈

- 栈是一种只能在一端进行插入或删除操作的线性表。
- 栈只能选取同一个端点进行插入和删除操作

- 线性表

---

### Slide 4


- 3.1.1 栈的定义

- 允许进行插入、删除操作的一端称为栈顶。
- 表的另一端称为栈底。
- 当栈中没有数据元素时，称为空栈。
- 栈的插入操作通常称为进栈或入栈。
- 栈的删除操作通常称为退栈或出栈。

- 栈顶

- 栈底

- 栈示意图

---

### Slide 5


- 栈的抽象数据类型定义

## 关系：栈中数据元素之间是线性关系

## 数据元素：可以是任意类型的数据，但必须属于同一个数据对象。

- 基本操作：
- InitStack（S）初始化栈，构造一个空栈。
- ClearStack（S）置为空栈。
- IsEmpty（S）       IsFull（S）
- Push（S，x）进栈。
- Pop（S，x）出栈
- GetTop（S，x）取栈顶元素

---

### Slide 6


- 3.1.2  栈的表示和实现

- 栈中元素逻辑关系与线性表的相同，栈可以采用与线性表相同的存储结构。

## 栈

## 顺序栈

## 链栈

## 逻辑结构

## 存储结构

---

### Slide 7


## 顺序栈

## #define Stack_Size 50
## typedef struct{
## StackElementType  elem[Stack_Size];  /*用来存放栈中元素的一维数组*/
## int  top;         /*用来存放栈顶元素的下标, top为-1表示空栈*/
## }SeqStack;

---

### Slide 8


## 栈
## (a1，a2，…，ai，…an )

- 直接映射

- a1

- a2

- …

- ai

- …

- an

- …

- MaxSize-1

- 0

- 1

- i-1

- n-1

- data

- top

- 逻辑结构

- 存储结构

## 顺序栈的示意图

---

### Slide 9


- 例如：MaxSize=5

- （b）a进栈

- （c）b、c、d、e进栈

- （d）出栈一次

---

### Slide 10


## 初始化

## void  InitStack(SeqStack *S)  {  /*构造一个空栈S*/
## S->top= -1;
## }

- S

- top

## 注意：s为栈指针
## top为s所指栈的栈顶指针

---

### Slide 11


## 判栈空/栈满

- int IsEmpty(SeqStack *S) {  /*判栈S为空栈时返回值为真，反之为假*/
- return(S->top==-1?TRUE:FALSE);
- }
- int IsFull(SeqStack *S) {     /*判栈S为满时返回真，否则返回假*/
- return(S->top== Stack_Size-1? TRUE: FALSE);
- }

---

### Slide 12


- 进栈

## int Push(SeqStack * S, StackElementType x) {
## if(S->top== Stack_Size-1)
## return(FALSE);  /*栈已满*/
## S->top++;
## S->elem[S->top]=x;
## return(TRUE);
## }

---

### Slide 13


- 出栈

## int Pop(SeqStack *S, StackElementType *x){
## if(S->top==-1)     /*栈为空*/
## return(FALSE);
## else {
## *x= S->elem[S->top];
## S->top--;    /* 修改栈顶指针 */
## return(TRUE);
## }
## }

---

### Slide 14


- 取栈顶元素

## int GetTop（SeqStack *S, StackElementType *x）{
## /* 将栈S的栈顶元素弹出，放到x所指的存储空间中，但栈顶指针保持不变 */
## if(S->top==-1)  /*栈为空*/
## return(FALSE);
## else {
## *x = S->elem[S->top];
## return(TRUE);
## }
## }

---

### Slide 15


- 两栈共享技术

- 主要利用了栈“栈底位置不变，而栈顶位置动态变化”的特性。
- 为两个栈申请一个共享的一维数组空间S[M]，将两个栈的栈底分别放在一维数组的两端，分别是0，M-1。
- 共享栈的空间示意为：top[0]和top[1]分别为两个栈顶指示器 。

- top[0]

- top[1]

- 0

- M-1

---

### Slide 16


- 两栈共享的数据结构定义

- #define M 100
- typedef struct{
- StackElementType Stack[M];
- StackElementType top[2];
- /*top[0]和top[1]分别为两个栈顶指示器*/
- }DqStack;

---

### Slide 17


- 两栈共享的初始化操作算法

## void InitStack(DqStack *S)
## {
## S->top[0]=-1;
## S->top[1]=M;
## }

---

### Slide 18


- 两栈共享的进栈操作算法

## int Push(DqStack *S, StackElementType x, int i){
## if(S->top[0]+1==S->top[1])  /*栈已满*/
## return(FALSE);
## switch(i) {
## case 0:		 /*0号栈*/
## S->top[0]++;
## S->Stack[S->top[0]]=x;
## break;
## case 1: 		/*1号栈*/
## S->top[1]--;
## S->Stack[S->top[1]]=x;
## break;
## default: return(FALSE)   /*参数错误*/
## }
## return(TRUE);
## }

- top[0]

- top[1]

- 0

- M-1

---

### Slide 19


- 两栈共享的出栈操作算法

## int Pop(DqStack *S, StackElementType *x, int i) {
## switch(i)   {
## case 0:
## if(S->top[0]==-1)
## return(FALSE);
## *x=S->Stack[S->top[0]];
## S->top[0]--;
## break;
## case 1:
## if(S->top[1]==M)
## return(FALSE);
## *x=S->Stack[S->top[1]];
## S->top[1]++;
## break;
## default: return(FALSE);
## }
## return(TRUE);
## }

- top[0]

- top[1]

- 0

- M-1

---

### Slide 20


- 栈：
- 执行期间编译器自动分配，编译器用它实现函数调用：调用函数时，栈增长；函数返回时，栈收缩。局部变量、函数参数、返回数据、返回地址等放在栈中

- 堆：
- 动态储存分配器维护着的一个进程的虚拟存储器区域。一般由程序员分配释放（堆在操作系统对进程初始化的时候分配），若程序员不释放，程序结束时可能由OS回收，每个进程，内核都维护着一个变量brk指向堆顶。

---

### Slide 21


- 链栈

- 采用链表存储的栈称为链栈，这里采用带头结点的单链表实现。
- 为便于操作，采用带头结点的单链表实现栈。

- top为栈顶指针，始终指向当前栈顶元素前面的头结点。若top->next=NULL，则代表空栈。
- 注意：链栈在使用完毕时，应该释放其空间。

---

### Slide 22


- 链栈结构

- typedef struct node{
- StackElementType  data;
- struct node *next;
- }LinkStackNode;
- typedef  LinkStackNode  *LinkStack;

---

### Slide 23


- 链栈的进栈操作

## int Push(LinkStack top, StackElementType x) { /* 将数据元素x压入栈top中 */
## LinkStackNode * temp;
## temp=(LinkStackNode * )malloc(sizeof(LinkStackNode));
## if(temp==NULL)
## return(FALSE);   /* 申请空间失败 */
## temp->data=x;
## temp->next=top->next;
## top->next=temp;   /* 修改当前栈顶指针 */
## return(TRUE);
## }

---

### Slide 24


- 链栈的出栈操作

## /* 将栈top的栈顶元素弹出，放到x所指的存储空间中 */
## int Pop(LinkStack top, StackElementType *x) {
## LinkStackNode * temp;
## temp=top->next;
## if(temp==NULL)  /*栈为空*/
## return(FALSE);
## top->next=temp->next;
## *x=temp->data;
## free(temp);       /* 释放存储空间 */
## return(TRUE);
## }

---

### Slide 25


## 将多个链栈的栈顶指针放在一个一维数组里来统一管理，从而实现管理和使用多个栈。
## #define M 10  /*M个栈链*/
## typedef struct node{
## StackElementType  data;
## struct node *next;
## }LinkStackNode, *linkStack;
## linkStack top[M];

- 多栈运算

---

### Slide 26


- 3.1.3 栈的应用举例

- 表达式求值：无括号算术表达式求值
- 1、运算符优先级表（ ↑ 为幂运算， # 表达式结束符）
- 2、设置两个栈：OVS(运算数栈)和OPTR(运算符栈)；
- 3、自左向右扫描，遇操作符则与OPTR栈顶比较优先级：
  - 当前操作符优先级大于OPTR栈顶则进OPTR栈；
  - 当前操作符优先级小于等于OPTR栈顶，OVS栈顶、次顶和OPTR栈顶退栈，并运算得到结果T(i)， T(i)进OVS栈。

## 3+4*5         #   +-   */   ↑
## ①         0    1    2    3
## ②

---

### Slide 27


- Y

- N

- N

- N

- Y

- N

- 置空栈OVS、OPTR

- 进OVS

- OVS栈顶、次顶和OPTR栈顶退栈，并运算得到结果T(i)， T(i)进OVS栈

- 进OPTR栈

- W是运算符

- Y

- W=‘#’’

- OPTRZ栈空

- W优先级≤OPTR栈顶优先级

- 开始

- 读字符W

- 结束

- OVS(运算数栈)
- OPTR(运算符栈)

- Y

## A/B↑C+D*E#

---

### Slide 28


## 例：实现A/B↑C+D*E#的运算过程时栈区变化情况

---

### Slide 29


- 3.1.4  栈与递归的实现

- 自学。

---

### Slide 30


## 一个初始为空的栈，依次执行以下操作后，栈顶元素是什么？
## 操作序列：push(10), push(20), pop(), push(30), pop(), pop()

## 10

## 20

## 30

## 栈为空

- A

- B

- C

- D

- 提交

- 可为此题添加文本、图片、公式等解析，且需将内容全部放在本区域内。

## 1. push(10) → 栈内元素：[10]（栈顶：10）
## 2. push(20) → 栈内元素：[10, 20]（栈顶：20）
## 3. pop() → 弹出20，栈内元素：[10]（栈顶：10）
## 4. push(30) → 栈内元素：[10, 30]（栈顶：30）
## 5. pop() → 弹出30，栈内元素：[10]（栈顶：10）
## 6. pop() → 弹出10，栈为空。

---

### Slide 31


- 3.2  队列 - 3.2.1 队列的定义

- 队列(Queue)简称队，它也是一种运算受限的线性表。

- 队列只能选取一个端点进行插入操作，另一个端点进行删除操作

## 线性表

---

### Slide 32


## 把进行插入的一端称做队尾（rear）。
## 进行删除的一端称做队首或队头（front）。
## 向队列中插入新元素称为进队或入队，新元素进队后就成为新的队尾元素。
## 从队列中删除元素称为出队或离队，元素出队后，其后继元素就成为队首元素。
## 队列具有先进先出 (Fist In Fist Out，缩写为FIFO)的特性

## 队尾

## 队头

## 队列示意图

---

### Slide 33


- 队列的抽象数据类型定义

- ADT  Queue
- 数据元素：可以是任意类型的数据，但必须属于同一个数据对象。
- 关系：队列中数据元素之间是线性关系。
- 基本操作：
- InitQueue(&Q)：初始化操作。设置一个空队列。
- IsEmpty(Q)：判空操作。若队列为空，则返回TRUE，否则返回FALSE。
- IsFull(Q)：判满操作。若队列为满，则返回TRUE，否则返回FALSE。
- EnterQueue(&Q，x)：进队操作。在队列Q的队尾插入x。操作成功，返回值为TRUE，否则返回值为FALSE。
- DeleteQueue(&Q,&x)：出队操作。使队列Q的队头元素出队，并用x带回其值。操作成功，返回值为TRUE，否则返回值为FALSE。
- GetHead（Q,&x）：取队头元素操作。用x取得队头元素的值。操作成功，返回TRUE，否则返回值为FALSE。
- ClearQueue(&Q)：队列置空操作。将队列Q置为空队列。
- DestroyQueue(&Q)： 队列销毁操作。释放队列的空间。

---

### Slide 34


- 3.2.2 队列的表示与实现

- 既然队列中元素逻辑关系与线性表的相同，队列可以采用与线性表相同的存储结构。

---

### Slide 35


- 链队列

## typedef struct Node{
## QueueElementType  data; /*数据域*/
## struct Node        *next;      /*指针域*/
## }LinkQueueNode;

## typedef struct {
## LinkQueueNode   * front;
## LinkQueueNode   * rear;
## }LinkQueue;

---

### Slide 36


- 初始化操作

## int InitQueue(LinkQueue * Q) { /* 将Q初始化为一个空的链队列 */
## Q->front = (LinkQueueNode *)malloc(sizeof(LinkQueueNode));
## if(Q->front!=NULL){
## Q->rear = Q->front;
## Q->front->next = NULL;
## return(TRUE);
## }
## else
## return(FALSE);    /* 溢出！*/

---

### Slide 37


## 入队操作

## int EnterQueue(LinkQueue *Q, QueueElementType x){  /* 将数据元素x插入到队列Q中 */
## LinkQueueNode  * NewNode;
## NewNode=(LinkQueueNode * )malloc(sizeof(LinkQueueNode));
## if(NewNode!=NULL) {
## NewNode->data=x;
## NewNode->next=NULL;
## Q->rear->next=NewNode;
## Q->rear=NewNode;
## return(TRUE);
## }
## else  return(FALSE);    /* 溢出！*/
## }

- a1

- a2

- an

- ∧

- …

- 队头

- 队尾

- front

- rear

- ∧

- front

- rear

---

### Slide 38


- 出队操作

## /* 将队列Q的队头元素出队，并存放到x所指的存储空间中 */
## int DeleteQueue(LinkQueue * Q, QueueElementType *x) {
## LinkQueueNode * p;
## if(Q->front==Q->rear)
## return(FALSE);
## p=Q->front->next;
## Q->front->next=p->next;  /* 队头元素p出队 */
## if(Q->rear==p)  /* 如果队中只有一个元素p，则p出队后成为空队 */
## Q->rear=Q->front;
## *x=p->data;
## free(p);   /* 释放存储空间 */
## return(TRUE);
## }

- a1

- a2

- an

- ∧

- …

- 队头

- 队尾

- front

- rear

- p

---

### Slide 39


- 循环队列

## 队列
## (a1,a2,…,ai,…an )

## …

## a1

## …

## an

- …

## f

## MaxSize-1

## f

## r

## 队列的元素空间

## front

## 0

## r

## rear

- 逻辑结构

- 存储结构

## #define MAXSIZE 50  /*队列的最大长度*/
## typedef struct{
## QueueElementType  element[MAXSIZE];
## /* 队列的元素空间*/
## int  front;   /*头指针指示器*/
## int  rear ;   /*尾指针指示器*/
## }SeqQueue;·

---

### Slide 40


- 把数组的前端和后端连接起来，形成一个环形的顺序表，即把存储队列元素的表从逻辑上看成一个环，称为循环队列或环形队列。

- 实际上内存地址一定是连续的，不可能是环形的，这里是通过逻辑方式实现环形队列

- rear = (rear+1)%MaxSize
- front = (front+1)%MaxSize

---

### Slide 42


## 队空和队满：rear==front

## 怎么办？

---

### Slide 43


- 处理方法

## 方法一：是少用一个元素空间。
  - 当队尾指针所指向的空单元的后继单元是队头元素所在的单元时，则停止入队。
  - 现在队列“满”的条件为：
  - （rear+1）mod MAXSIZE==front。
  - 判队空的条件不变，仍为rear==front。
## 方法二：是增设一个标志量的方法，以区别队列是“空”还是“满”。

---

### Slide 44


## 初始化操作

- /* 将*Q初始化为一个空的循环队列 */
- void InitQueue（SeqQueue * Q）{
- Q->front = Q->rear = 0;
- }

---

### Slide 45


## 入队操作

## int EnterQueue(SeqQueue *Q, QueueElementType x) { /*将元素x入队*/
## if((Q->rear+1)%MAXSIZE == Q->front)  /*队列已经满了*/
## return(FALSE);
## Q->element[Q->rear]=x;
## Q->rear=(Q->rear+1)%MAXSIZE;  /* 重新设置队尾指针 */
## return(TRUE);  /*操作成功*/
## }

---

### Slide 46


## 出队操作

## /*删除队列的队头元素，用x返回其值*/
## int DeleteQueue(SeqQueue *Q, QueueElementType * x) {
## if（Q->front==Q->rear）  /*队列为空*/
## return(FALSE);
## *x=Q->element[Q->front];
## Q->front = (Q->front+1)%MAXSIZE;  /*重新设置队头指针*/
## return(TRUE);  /*操作成功*/
## }

---

### Slide 47


- 方法二（标志域）

- typedef struct {
- QueueElementType  element[MAXSIZE];  /* 队列的元素空间*/
- int front;  /*头指针指示器*/
- int rear;    /*尾指针指示器*/
- int tag;     /*标志域*/
- }SeqQueue;

- 47

---

### Slide 48


## 初始化操作（标志域）

- /* 将*Q初始化为一个空的循环队列 */
- void InitQueue（SeqQueue * Q）{
- Q->front = Q->rear = 0;
- }

---

### Slide 49


## 入队操作（标志域）

## int EnterQueue(SeqQueue *Q, QueueElementType x) { /*将元素x入队*/
## if(Q->rear==Q->front && Q->tag==1)  /*队列已经满了*/
## return(FALSE);
## Q->element[Q->rear]=x;
## Q->rear=(Q->rear+1)%MAXSIZE;  /* 重新设置队尾指针 */
## if(Q->front==Q->rear)
## Q->tag=1;
## return(TRUE);  /*操作成功*/
## }

---

### Slide 50


## 出队操作（标志域）

## /*删除队列的队头元素，用x返回其值*/
## int DeleteQueue(SeqQueue *Q, QueueElementType * x) {
## if（Q->front==Q->rear && Q->tag==0 ）  /*队列为空*/
## return(FALSE);
## *x=Q->element[Q->front];
## Q->front = (Q->front+1)%MAXSIZE;  /*重新设置队头指针*/
- if(Q->front==Q->rear)
- Q->tag=0;
## return(TRUE);  /*操作成功*/
## }

---

### Slide 51


- 课堂实践

- 将前面的表达式求解例题，编制成完整的C程序。要求：请按照下面的步骤，进行逐步进阶编程：
- 第一步：实现一个简单的栈（支持入栈、出栈、查看栈顶元素等）
- 第二步：实现不带括号的表达式求值（仅支持加减乘除求幂）
- 第三步：增加对括号的支持 *
- 第四步：增加对负数和求幂运算的支持 *
- 第五步：增加对表达式格式错误的检查 *
- 说明：带*号的部分，可根据自身基础选做，不强制要求。

- 51
