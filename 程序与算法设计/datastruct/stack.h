#ifndef STACK_H
#define STACK_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 可配置的元素类型：在包含本头文件之前可以定义 `STACK_ELEM_TYPE`，
   例如：#define STACK_ELEM_TYPE double */
#ifndef STACK_ELEM_TYPE
typedef int STACK_ELEM_TYPE;
#else
typedef STACK_ELEM_TYPE STACK_ELEM_TYPE;
#endif

#ifndef STACK_INITIAL_CAPACITY
#define STACK_INITIAL_CAPACITY 16
#endif

#define STACK_OK 1
#define STACK_ERR 0

typedef struct {
	STACK_ELEM_TYPE *data;
	size_t size;     /* 当前元素数量 */
	size_t capacity; /* 分配容量 */
} Stack;

/* 初始化栈（分配 capacity 或默认容量），返回 STACK_OK 或 STACK_ERR */
static inline int StackInit(Stack *s, size_t capacity) {
	if (!s) return STACK_ERR;
	if (capacity == 0) capacity = STACK_INITIAL_CAPACITY;
	s->data = (STACK_ELEM_TYPE*)malloc(sizeof(STACK_ELEM_TYPE) * capacity);
	if (!s->data) return STACK_ERR;
	s->size = 0;
	s->capacity = capacity;
	return STACK_OK;
}

/* 释放栈占用内存 */
static inline void StackDestroy(Stack *s) {
	if (!s) return;
	free(s->data);
	s->data = NULL;
	s->size = 0;
	s->capacity = 0;
}

/* 是否为空（返回 1 表示空） */
static inline int StackIsEmpty(const Stack *s) {
	return (!s || s->size == 0) ? 1 : 0;
}

/* 当前元素个数 */
static inline size_t StackSize(const Stack *s) {
	return s ? s->size : 0;
}

/* 内部：确保至少有 min_capacity 容量，失败返回 STACK_ERR */
static inline int StackEnsureCapacity(Stack *s, size_t min_capacity) {
	if (!s) return STACK_ERR;
	if (s->capacity >= min_capacity) return STACK_OK;
	size_t newcap = s->capacity ? s->capacity * 2 : STACK_INITIAL_CAPACITY;
	while (newcap < min_capacity) newcap *= 2;
	STACK_ELEM_TYPE *tmp = (STACK_ELEM_TYPE*)realloc(s->data, sizeof(STACK_ELEM_TYPE) * newcap);
	if (!tmp) return STACK_ERR;
	s->data = tmp;
	s->capacity = newcap;
	return STACK_OK;
}

/* 入栈：返回 STACK_OK 或 STACK_ERR */
static inline int StackPush(Stack *s, STACK_ELEM_TYPE val) {
	if (!s) return STACK_ERR;
	if (s->size >= s->capacity) {
		if (StackEnsureCapacity(s, s->size + 1) != STACK_OK) return STACK_ERR;
	}
	s->data[s->size++] = val;
	return STACK_OK;
}

/* 出栈：如果非空将值写入 out（可为 NULL）并返回 STACK_OK，否则返回 STACK_ERR */
static inline int StackPop(Stack *s, STACK_ELEM_TYPE *out) {
	if (!s || s->size == 0) return STACK_ERR;
	s->size--;
	if (out) *out = s->data[s->size];
	return STACK_OK;
}

/* 取栈顶：不弹出，成功返回 STACK_OK，否则返回 STACK_ERR */
static inline int StackTop(const Stack *s, STACK_ELEM_TYPE *out) {
	if (!s || s->size == 0 || !out) return STACK_ERR;
	*out = s->data[s->size - 1];
	return STACK_OK;
}

/* 清空栈但不释放内存 */
static inline void StackClear(Stack *s) {
	if (!s) return;
	s->size = 0;
}

/* 交换两个栈的内容（O(1)） */
static inline void StackSwap(Stack *a, Stack *b) {
	if (!a || !b) return;
	Stack tmp = *a;
	*a = *b;
	*b = tmp;
}

#endif /* STACK_H */