#ifndef __BLIZZARD_HASH_H
#define __BLIZZARD_HASH_H
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

//#define MAXMPQHASHTABLELEN 8192
//#define MAXMPQHASHTABLELEN 10949
#define EXPORT 

typedef struct {

	long nHashA;
	long nHashB;
	unsigned int bExists;
}MPQHASHTABLE;

EXPORT unsigned long cryptTable[0x500];

EXPORT unsigned long HashString(char *lpszString, unsigned long dwHashType);//�����ַ�Ĺ�ϣֵ 
EXPORT char* MPQHashTableInit(char **ppHashTable, long nTableLength);//��ʼ����ϣ��
EXPORT void MPQHashTableFree(char *pHashTable);//�ͷŹ�ϣ��
EXPORT unsigned int MPQHashTableAdd(char *lpszString, char *pHashTable);//���ַ����Ϣ�����ϣ��
EXPORT long MPQHashTableIsExist(char *lpszString, char *pHashTable);//�ж�ĳ�ַ��ڹ�ϣ�����Ƿ����
#endif
