#ifndef STACK_H
#define STACK_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* �����õ�Ԫ�����ͣ��ڰ�����ͷ�ļ�֮ǰ���Զ��� `STACK_ELEM_TYPE`��
   ���磺#define STACK_ELEM_TYPE double */
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
	size_t size;     /* ��ǰԪ������ */
	size_t capacity; /* �������� */
} Stack;

/* ��ʼ��ջ������ capacity ��Ĭ�������������� STACK_OK �� STACK_ERR */
static inline int StackInit(Stack *s, size_t capacity) {
	if (!s) return STACK_ERR;
	if (capacity == 0) capacity = STACK_INITIAL_CAPACITY;
	s->data = (STACK_ELEM_TYPE*)malloc(sizeof(STACK_ELEM_TYPE) * capacity);
	if (!s->data) return STACK_ERR;
	s->size = 0;
	s->capacity = capacity;
	return STACK_OK;
}

/* �ͷ�ջռ���ڴ� */
static inline void StackDestroy(Stack *s) {
	if (!s) return;
	free(s->data);
	s->data = NULL;
	s->size = 0;
	s->capacity = 0;
}

/* �Ƿ�Ϊ�գ����� 1 ��ʾ�գ� */
static inline int StackIsEmpty(const Stack *s) {
	return (!s || s->size == 0) ? 1 : 0;
}

/* ��ǰԪ�ظ��� */
static inline size_t StackSize(const Stack *s) {
	return s ? s->size : 0;
}

/* �ڲ���ȷ�������� min_capacity ������ʧ�ܷ��� STACK_ERR */
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

/* ��ջ������ STACK_OK �� STACK_ERR */
static inline int StackPush(Stack *s, STACK_ELEM_TYPE val) {
	if (!s) return STACK_ERR;
	if (s->size >= s->capacity) {
		if (StackEnsureCapacity(s, s->size + 1) != STACK_OK) return STACK_ERR;
	}
	s->data[s->size++] = val;
	return STACK_OK;
}

/* ��ջ������ǿս�ֵд�� out����Ϊ NULL�������� STACK_OK�����򷵻� STACK_ERR */
static inline int StackPop(Stack *s, STACK_ELEM_TYPE *out) {
	if (!s || s->size == 0) return STACK_ERR;
	s->size--;
	if (out) *out = s->data[s->size];
	return STACK_OK;
}

/* ȡջ�������������ɹ����� STACK_OK�����򷵻� STACK_ERR */
static inline int StackTop(const Stack *s, STACK_ELEM_TYPE *out) {
	if (!s || s->size == 0 || !out) return STACK_ERR;
	*out = s->data[s->size - 1];
	return STACK_OK;
}

/* ���ջ�����ͷ��ڴ� */
static inline void StackClear(Stack *s) {
	if (!s) return;
	s->size = 0;
}

/* ��������ջ�����ݣ�O(1)�� */
static inline void StackSwap(Stack *a, Stack *b) {
	if (!a || !b) return;
	Stack tmp = *a;
	*a = *b;
	*b = tmp;
}

#endif /* STACK_H */