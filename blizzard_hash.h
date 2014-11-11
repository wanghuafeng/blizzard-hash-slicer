#ifndef __BLIZZARD_HASH_H
#define __BLIZZARD_HASH_H

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

//#define MAXMPQHASHTABLELEN 8192
//#define MAXMPQHASHTABLELEN 10949
#define EXPORT __declspec(dllexport)

typedef struct {

	long nHashA;
	long nHashB;
	unsigned int bExists;
}MPQHASHTABLE;

EXPORT unsigned long cryptTable[0x500];

EXPORT unsigned long HashString(char *lpszString, unsigned long dwHashType);//计算字符串的哈希值 
EXPORT char* MPQHashTableInit(char **ppHashTable, long nTableLength);//初始化哈希表
EXPORT void MPQHashTableFree(char *pHashTable);//释放哈希表
EXPORT unsigned int MPQHashTableAdd(char *lpszString, char *pHashTable);//将字符串的信息加入哈希表
EXPORT long MPQHashTableIsExist(char *lpszString, char *pHashTable);//判断某字符串在哈希表中是否存在

#endif
