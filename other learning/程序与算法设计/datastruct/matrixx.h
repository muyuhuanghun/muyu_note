#ifndef MATRIXX_H
#define MATRIXX_H

#include <stdlib.h>

#ifndef MaxSizex
#define MaxSizex 1000
#endif

typedef struct
{
    int row, col;
    int data;
}triple;

typedef struct
{
    triple data[MaxSizex];
    int m , n , len;
}tsmatrix;

static tsmatrix * matrixadd(tsmatrix *A,tsmatrix * B)
{
    if (A->m != B->m || A->n != B->n)
    {
        return NULL;
    }

    tsmatrix *c = (tsmatrix*)malloc(sizeof(tsmatrix));
    if (c == NULL)
    {
        return NULL;
    }
    c->m = A->m;
    c->n = A->n;
    c->len = 0;
    int i=0,j=0;

    while(i<A->len && j<B->len)
    {
        if(A->data[i].row==B->data[j].row)
        {
            if(A->data[i].col==B->data[j].col)
            {
                int sum = A->data[i].data + B->data[j].data;
                if(sum != 0)
                {
                    if (c->len >= MaxSizex)
                    {
                        free(c);
                        return NULL;
                    }
                    c->data[c->len].row = A->data[i].row;
                    c->data[c->len].col = A->data[i].col;
                    c->data[c->len].data = sum;
                    c->len++;
                }
                i++;
                j++;
            }
            else if(A->data[i].col<B->data[j].col)
            {
                if (c->len >= MaxSizex)
                {
                    free(c);
                    return NULL;
                }
                c->data[c->len] = A->data[i];
                c->len++;
                i++;
            }
            else
            {
                if (c->len >= MaxSizex)
                {
                    free(c);
                    return NULL;
                }
                c->data[c->len] = B->data[j];
                c->len++;
                j++;
            }
        }
        else if(A->data[i].row<B->data[j].row)
        {
            if (c->len >= MaxSizex)
            {
                free(c);
                return NULL;
            }
            c->data[c->len] = A->data[i];
            c->len++;
            i++;
        }
        else
        {
            if (c->len >= MaxSizex)
            {
                free(c);
                return NULL;
            }
            c->data[c->len] = B->data[j];
            c->len++;
            j++;
        }
    }
    while(i < A->len)
    {
        if (c->len >= MaxSizex)
        {
            free(c);
            return NULL;
        }
        c->data[c->len++] = A->data[i++];
    }
    while(j < B->len)
    {
        if (c->len >= MaxSizex)
        {
            free(c);
            return NULL;
        }
        c->data[c->len++] = B->data[j++];
    }
    return c;
}

static tsmatrix* matrixmul(tsmatrix *A, tsmatrix *B)
{
    if(A->n != B->m)
    {
        return NULL;
    }

    tsmatrix *c = (tsmatrix*)malloc(sizeof(tsmatrix));
    if(c == NULL)
    {
        return NULL;
    }
    c->m = A->m;
    c->n = B->n;
    c->len = 0;

    for(int i=0;i<A->len;i++)
    {
        for(int j=0;j<B->len;j++)
        {
            if(A->data[i].col == B->data[j].row)
            {
                int row = A->data[i].row;
                int col = B->data[j].col;
                int val = A->data[i].data * B->data[j].data;
                int k, pos = -1;

                for(k=0;k<c->len;k++)
                {
                    if(c->data[k].row == row && c->data[k].col == col)
                    {
                        pos = k;
                        break;
                    }
                }

                if(pos != -1)
                {
                    c->data[pos].data += val;
                    if(c->data[pos].data == 0)
                    {
                        for(int t=pos;t<c->len-1;t++)
                        {
                            c->data[t] = c->data[t+1];
                        }
                        c->len--;
                    }
                }
                else if(val != 0)
                {
                    if(c->len >= MaxSizex)
                    {
                        free(c);
                        return NULL;
                    }
                    c->data[c->len].row = row;
                    c->data[c->len].col = col;
                    c->data[c->len].data = val;
                    c->len++;
                }
            }
        }
    }
    return c;
}

#endif
