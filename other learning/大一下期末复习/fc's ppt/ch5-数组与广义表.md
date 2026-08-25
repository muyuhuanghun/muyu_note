# ch5-数组与广义表


---

### Slide 1


## 第五章 数组与广义表

## 授课教师：傅翀

---

### Slide 2


## 5.1 数组的定义和运算

- 数组是一种数据类型。
- 从逻辑结构上看，数组可以看成是一般线性表的扩充。
- 二维数组可以看成是线性表的线性表。

---

### Slide 3


## 我们可以把二维数组看成一个线性表：
## A=( 1     2    …  j     … n)，其中j（1≤j ≤n）本身也是一个线性表，称为列向量

- A =（   1     2        ┅         j          ┅      n    )

- 矩阵Am×n看成n个列向量的线性表
## j=(a1j,a2j, …,amj)

---

### Slide 4


## 我们还可以将数组Am×n看成另外一个线性表：
## B=(1，,2,，… ，m)，其中i（1≤i ≤m）本身也是一个线性表，称为行向量
## 即： I= （ai1，ai2， …，aij ，…，ain）

- B
- =

- 1
- 2
- ┇
- i
- ┇
- m

---

### Slide 5


- 数组的运算

- 数组是一组有固定个数的元素的集合。
- 对数组的操作不象对线性表的操作那样，可以在表中任意一个合法的位置插入或删除一个元素。
- 对于数组的操作一般只有两类：
  - 获得特定位置的元素值；
  - 修改特定位置的元素值。

---

### Slide 6


- 数组的抽象数据类型定义

- ADT Array｛
- 数据对象：D={ aj1 j2… jn| n>0，称为数组的维数，ji 是数组的第i维下标，
- 1≤ji≤bi，  bi 为数组第i维的长度， aj1 j2… jn ∈ElementSet}
- 数据关系：R={R1,R2,…,Rn}， Ri={< aj1… ji… jn ，aj1 … ji+1…jn > | 1≤jk≤bk，
- 1≤k≤n 且k≠i，1≤ji≤bi-1， aj1… ji… jn ，aj1… ji+1… jn ∈D，i=1，…，n}

---

### Slide 7


- 数组的抽象数据类型定义

- 基本操作：
- InitArray(A,n,bound1,…,boundn)： 若维数n和各维的长度合法，则构造相应的数组A，并返回TRUE；
- DestroyArray（A）： 销毁数组A；
- GetValue（A，e, index1, …,indexn）：  若下标合法，用e返回数组A中由index1, …,indexn所指定的元素的值。
- SetValue（A，e，index1, …,indexn）： 若下标合法，则将数组A中由index1, …,indexn所指定的元素的值置为e。
- ｝

## 数组下标是从1开始

---

### Slide 8


- 5.2 数组的顺序存储和实现

## 对于数组A，一旦给定其维数n及各维长度bi（1≤i≤n），则该数组中元素的个数是固定的，不可以对数组做插入和删除操作，不涉及移动元素操作，因此对于数组而言，采用顺序存储法比较合适。

---

### Slide 9


- 一维数组地址计算

- 一旦a1的存储地址LOC(a1)确定，并假设每个数据元素占用size个存储单元，则任一数据元素ai的存储地址LOC(ai)就可由以下公式求出：
## LOC(ai)=LOC(a1)+(i-1)*size 　(1≤i≤n)
- 共i-1个元素
## 数组a：a1　a2　a3　…　ai-1　ai　…　an
- 一维数组具有随机存储特性：可以在O(1)时间内找到序号为i的元素值。

---

### Slide 10


- 二维数组的顺序存储

- 二维数组的顺序存储结构有两种：
  - 一种是按行序存储，如高级语言C、BASIC、COBOL和PASCAL语言都是以行序为主。
  - 另一种是按列序存储，如高级语言中的FORTRAN语言就是以列序为主。

---

### Slide 11


- 二维数组地址计算-行主序

## LOC(aij) = LOC(a11) + [(i-1)*n + (j-1)] *size

---

### Slide 12


- 二维数组地址计算-列主序

## LOC(aij)=LOC(a11) + [(j-1)*m + (i-1)] *size

---

### Slide 13


- 三维数组地址计算

## 行主序：从最后一个下标（纵下标）开始变换（垂直行切4*2）
## a111 a112 a121 a122 a131 a132 a141 a142 … a331 a332 a341 a342
## 纵主序：从第一个下标（行下标）开始变换（垂直纵切3*4）
## a111 a211 a311 a121 a221 a321 a131 a231 a331  … a132 a232 a332 a142 a242 a342

## 规则可以推广到多维数组

---

### Slide 14


- 三维数组地址计算

- Am×n×r
- 行主序：LOC(aijk) = LOC(a111) + [(i-1)*n*r + (j-1)*r + (k-1)] *size
- 纵主序：LOC(aijk) = LOC(a111) + [(i-1) + (j-1) m+ (k-1) m*n] *size

---

### Slide 15


- n维数组地址计算

- 第一维主序：
- LOC (j1, j2, ... , jn ) = LOC (1, 1, ... , 1) +
- [ b2*b3*...*bn*(j1 - 1) + b3*b4*...*bn*(j2 - 1) + ... + bn*(jn-1 - 1)+ (jn - 1) ] * size

---

### Slide 16


- 5.3 特殊矩阵的压缩存储

## 在高级程序设计语言里面，矩阵通常采用二维数组表示。
## 特殊矩阵可采用压缩存储的方式
  - 元素分布有规律的矩阵，按规律实现压缩储存
  - 非零元素少的稀疏矩阵，采用存非零元素实现压缩存储

---

### Slide 17


## 对一个二维数组 A[6][8] 按行优先存储，若 A[0][0] 的地址为1000，每个元素占4字节，则 A[3][5] 的地址是（ ）

## 1084

## 1100

## 1124

## 1140

- A

- B

- C

- D

- 提交

- 可为此题添加文本、图片、公式等解析，且需将内容全部放在本区域内。

- 行优先地址计算 = 基址 + (行数×列数 + 列号)×元素大小 = 1000 + (3×8 + 5)×4 = 1124

---

### Slide 18


- 5.3.1 特殊矩阵

## 三角矩阵（ n阶矩阵）
  - 下三角矩阵：若当i<j时，有aij=0
  - 上三角矩阵：若当 i>j时，有aij=0
  - 对称矩阵：若矩阵中的所有元素均满足aij=aji

---

### Slide 19


- 下三角矩阵

- 按“行序为主序”进行存储，得到的序列为：a11,a21,a22,a31,a32,a33…an1,an2…ann
- 由于下三角矩阵的元素个数为n(n+1)/2，所以可压缩存储到一个大小为n(n+1)/2的一维数组中。
- 下三角矩阵中元素aij(i>j)，在一维数组A中的位置为：
  - LOC[aij]= LOC[a11]+ i (i -1)/2+ j-1

---

### Slide 20


- 上三角矩阵和对称矩阵

- 上三角矩阵：将其压缩存储到一个大小为n(n+1)/2的一维数组C中。其中元素aij(i<j)在数组C中的存储位置为：
  - Loc[aij]= Loc[a11] + j(j -1)/2 + i -1
## 对称矩阵：其元素满足aij=aji，我们可以为每一对相等的元素分配一个存储空间，即只存下三角（或上三角）矩阵，从而将n2个元素压缩到n(n+1)/2个空间中。

---

### Slide 21


- 带状矩阵

- 所有的非零元素都集中在以主对角线为中心的带状区域中。最常见的是三对角带状矩阵。

---

### Slide 22


- 三对角带状矩阵

- 三对角带状矩阵的压缩存储，以行序为主序进行存储，并且只存储非零元素
- 确定存储该矩阵所需的一维向量空间的大小
  - 除第一行和最后一行只有两个元素外，其余各行均有3个非零元素。由此可得到一维向量所需的空间大小为：3n-2
- 确定非零元素在一维数组空间中的位置
  - LOC[aij] = LOC[a11]+3*(i-1)-1+j-i+1
  - =LOC[a11]+2(i-1)+j-1

---

### Slide 23


- 0     0   3   0    0   15
- 12   0   0   0   18   0
- 9    0   0   24   0   0
- 0    0   0    0    0   -7
- 0    0   0    0    0    0
- 0    0   14   0   0    0
- 0    0    0    0   0    0

- 5.3.2 稀疏矩阵

- 指矩阵中大多数元素为零的矩阵。一般地，当非零元素个数只占矩阵元素总数的25%—30%,或低于这个百分数时，我们称这样的矩阵为稀疏矩阵。

---

### Slide 24


- 稀疏矩阵的三元组表表示法

- 对于稀疏矩阵的压缩存储要求在存储非零元素的同时，还必须存储该非零元素在矩阵中所处的行号和列号。
- 我们将这种存储方法叫做稀疏矩阵的三元组表示法。

---

### Slide 25


- 三元组表的类型定义

## #define MAXSIZE 1000  /*非零元素的个数最多为1000*/
## typedef struct{
## int  row,  col;  /*该非零元素的行下标和列下标*/
## ElementType  e； /*该非零元素的值*/
## }Triple;
## typedef struct{
## Triple  data[MAXSIZE];  /* 非零元素的三元组表 */
## int m, n, len;  /*矩阵的行数、列数和非零元素的个数*/
## }TSMatrix；

---

### Slide 26


- 稀疏矩阵的转置运算

- 矩阵转置：指变换元素的位置，把位于（row，col）位置上的元素换到（col ，row）位置上，也就是说，把元素的行列互换，正常矩阵算法：
## void TransMatrix（ElementType source[n][m], ElementType dest[m][n]）{
## /*Source和dest分别为被转置的矩阵和转置后的矩阵（用二维数组表示）*/
## int i, j;
## for(i=0;i<m;i++)
## for (j=0;j< n;j++)
## dest[i][ j]=source[j] [i] ;
## }

- 时间复杂度为：O(m*n)
- 矩阵有m行n列

---

### Slide 27


- 稀疏矩阵的转置运算（三元组表）

- 矩阵source的三元组表A的行、列互换就可以得到B中的元素。
- 为了保证转置后的矩阵的三元组表B也是以“行序为主序”进行存放，则需要对行、列互换后的三元组B，按B的行下标（即A的列下标）大小重新排序。

---

### Slide 28


- 对于一个m×n的矩阵Am×n，其转置矩阵是一个n×m的矩阵Bn×m，满足bi,j=aj,i，其中0≤i≤m-1，0≤j≤n-1。

---

### Slide 29


- 一种非高效的算法：按第0、1、2、… 、n-1列进行转换

---

### Slide 30


## /*把矩阵A转置到B所指向的矩阵中去。矩阵用三元组表表示*/
## void TransposeTSMatrix(TSMatrix  A,  TSMatrix  * B) {
## int  i , j, k ;
## B->m= A.n ; B->n= A.m ; B->len= A.len ;
## if(B->len>0) {
## j=0; 	/* j为三元组表B的下标 */
## for(k=0; k<A.n; k++)	/* 扫描三元组表A共n次 */
## for(i=0; i<A.len; i++)  	/* i为三元组表A的下标 */
## if(A.data[i].col==k){ 	/* 寻找三元组表A的列值为k的进行转置 * /
## B->data[j].row=A.data[i].col;
## B->data[j].col=A.data[i].row;
## B->data[j].e=A.data[i].e;
## j++;
## } /* 内循环if结束*/
## } /* if(B->len>0)结束*/
## }

- 时间复杂度为：O(n*t)。
- 矩阵A有m行n列，t个非0元素

---

### Slide 31


- 快速的稀疏矩阵的转置算法（三元组表）

- 优化：去掉双重循环，扫描三元组表A一次，就能定位到三元组表B的正确位置上 。
- 设两个数组
  - num[col]：表示原始矩阵A中col列中非零元个数
  - position[col]：指示原始矩阵A中col列第一个非零元在三元组表B中位置（下标值）

---

### Slide 32


## 0

## 2

## 4

## 6

## 7

## 7

## 8

## 2

## 2

## 2

## 1

## 0

## 1

## 0

---

### Slide 33


- /*基于矩阵的三元组表示，采用快速转置法，将矩阵A转置为B所指的矩阵*/
- FastTransposeTSMatrix (TSMatrix  A,  TSMatrix  * B) {
- int col , t , p，q;
- int num[MAXSIZE], position[MAXSIZE] ;
- B->len= A.len ; B->n= A.m ; B->m= A.n ;
- if(B->len) {
- for(col=0;col<A.n;col++)
- num[col]=0; 	 	/*清零num数组*/
- for(t=0;t<A.len;t++)
- num[A.data[t].col]++; 	/*计算三元组表A每一列的非零元素的个数*/
- position[0]=0;
- for(col=1;col<A.n;col++) 	/*求col列中第一个非零元素在B.data[ ]中的正确位置*/
- position[col]=position[col-1]+num[col-1];
- for(p=0;p<A.len.p++) {	/* 从头扫描三元组表A一次 */
- col=A.data[p].col;
- q=position[col]; 	 /*col列中第一个非零元素在B.data[ ]中的正确位置*/
- B->data[q].row=A.data[p].col;
- B->data[q].col=A.data[p].row;
- B->data[q].e=A.data[p].e
- position[col]++; 	/*col列中下一个非零元素在B.data[ ]中的正确位置，修改了position数组*/
- }
- }
- }

---

### Slide 34


- 十字链表

## 矩阵的每一个非零元素用一个结点表示

- right： 用于链接同一行中的下一个非零元素；
- down：用以链接同一列中的下一个非零元素。

---

### Slide 35


## 3个行头结点

## 4个列头结点

---

### Slide 36


- 十字链表的结构类型定义

## typedef struct OLNode{
## int  row,  col;        /* 非零元素的行和列下标 */
## ElementType     value;
## struct OLNode  *down, * right;  /* 非零元素所在行表列表的后继链域 */
## }OLNode; *OLink;
## typedef struct {
## OLink  * row_head,  *col_head;   /* 行、列链表的头指针向量 */
## int  m,  n,  len;      /* 稀疏矩阵的行数、列数、非零元素的个数 */
## }CrossList;

---

### Slide 37


## /*采用十字链表存储结构，创建稀疏矩阵M*/
## CreateCrossList (CrossList * M) {
## int m,n,t,i,j;
## OLink p,q;
## printf("输入M的行数、列数和非零元素的个数\n");
## scanf("%d,%d,%d",&m,&n,&t);  /*输入M的行数、列数和非零元素的个数*/
## M->m=m;    M->n=n;    M->len=t;
## if(!(M->row_head=(OLink *)malloc(m*sizeof(OLink))))
## exit(OVERFLOW);
## if(!(M->col_head=(OLink *)malloc(n*sizeof(OLink))))
## exit(OVERFLOW);
## for(i=0,i<m,i++)
## M->row_head[i]=NULL;   /*初始化行头指针向量*/
## for(j=0,j<n,j++)
## M->col_head[j]=NULL;     /*初始化列头指针向量*/

---

### Slide 38


## for(scanf(&i,&j,&e);i!=-1;scanf(&i,&j,&e)) {
## if(!(p=(OLNode *)malloc(sizeof(OLNode))))
## exit(OVERFLOW);
## p->row=i;    p->col=j;    p->value=e;  /*生成结点*/
## if(M->row_head[i]==NULL)
## M->row_head[i]=p;
## else{  /*寻找行表中的插入位置*/
## q=M->row_head[i];
## while(q->right&&q->right->col<j)
## q=q->right;  /*找到链表末尾插入*/
## }
## p->right=q->right;
## q->right=p;     /*完成插入*/
## ｝

## if(M->col_head[j]==NULL)
## M->col_head[j]=p;
## else{   /*寻找列表中的插入位置*/
## q=M->col_head[j];
## while(q->down&&q->down->row<i);
## q=q->down; /*找到链表末尾插入*/
## p->down=q->down;
## q->down=p;     /*完成插入*/
## }
## } /*for结束*/
## }

---

### Slide 39


- 5.4  广义表

- 广义表是线性表的推广，是有限个元素的序列，其逻辑结构表示法：
  - GL = （d1，d2，d3，…，dn）
- 广义表中的di既可以是单个元素，还可以是一个广义表。
- GL是广义表的名字，通常用大写字母表示。
- n是广义表的长度。
- 若 di是一个广义表，则称di是广义表GL的子表。
- 在GL中， d1是GL的表头，其余部分组成的表（d2，d3，…，dn）称为GL的表尾。

---

### Slide 40


- 5.4.1  广义表的概念

## D =（） 空表，其长度为零。
## A = (a，(b，c)) 表长度为2的广义表，其中第一个元素是单个数据a，第二个元素是一个子表（b，c）。
  - head(A)=a ，表A的表头是a。
  - tail(A)=((b，c)) ，表A的表尾是((b，c)) 。
## B=（A，A，D）长度为3的广义表，其前两个元素为表A，第三个元素为空表D。
## C=（a，C） 长度为2的递归定义的广义表，C相当于无穷表C=（a，（a，（a，（…））））。

---

### Slide 41


- 5.4.1  广义表的概念

- 广义表的元素可以是子表，而子表还可以是子表…，由此，广义表是一个多层的结构。
- 广义表可以被其他广义表共享。如：广义表B就共享表A。在表B中不必列出表A的内容，只要通过子表的名称就可以引用该表。
- 广义表具有递归性，如广义表C。

---

### Slide 42


- 广义表中有两类结点：
  - 一类是单个元素结点，即原子结点。
  - 一类是子表结点，即表结点。
- 任何一个非空的广义表都可以将其分解成表头和表尾两部分。
- 一个表结点可由三个域构成：标志域，指向表头的指针域，指向表尾的指针域。
- 原子结点只需要两个域：标志域和值域。

- 5.4.1  广义表的储存结构

---

### Slide 43


## D =（）
## A = (a，(b，c))
## B=（A，A，D）
## C=（a，C）

- 广义表的头尾链表存储结构图

## 同层结点链存储结构图

---

### Slide 44


- 广义表的头尾链表类型定义

## typedef enum {ATOM, LIST} ElemTag;   /*ATOM＝0，表示原子；LIST＝1，表示子表*/
## typedef struct GLNode {
## ElemTag   tag; 		/*标志位tag用来区别原子结点和表结点*/
## union  {
## AtomType  atom;	/*原子结点的值域atom*/
## struct {
## struct GLNode  * hp, *tp;
## } htp; 			/*表结点的指针域htp， 包括表头指针域hp和表尾指针域tp*/
## } atom_htp;   /* atom_htp 是原子结点的值域atom和表结点的指针域htp的联合体域*/
## } GLNode,  *GList；

---

### Slide 45


## 

## 

## 1

## 

## 1

## a

## 0

## b

## 0

## 

## 1

## 

## c

## 0

## 

## 1

## 1

## 

## 1

## a

## 0

## D

## A

## B

## C

## 

## 1

## 1

## 

## 

## 1

- 广义表的同层结点链存储结构图

## D =（）
## A = (a，(b，c))
## B=（A，A，D）
## C=（a，C）

## 头尾链表存储结构图

---

### Slide 46


- 广义表的同层结点链存储类型定义

## typedef enum {ATOM, LIST} ElemTag;   /*ATOM＝0，表示原子；LIST＝1，表示子表*/
## typedef struct GLNode {
## ElemTag   tag; 		/*标志位tag用来区别原子结点和表结点*/
## union  {
## AtomType  atom;	/*原子结点的值域atom*/
## struct GLNode  * hp;
## } atom_htp;
## struct GLNode  * tp;
## } GLNode,  *GList；
