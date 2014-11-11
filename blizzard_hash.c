#include <stdio.h>
#include<assert.h>
#include "blizzard_hash.h"

static unsigned int g_hash_mask = 0;

/************************************************************************/
/*函数名：InitCryptTable
/*功  能：对哈希索引表预处理  
/*返回值：无
/************************************************************************/
static void InitCryptTable()
{
	unsigned long seed = 0x00100001, index1 = 0, index2 = 0, i;

	for (index1 = 0; index1 < 0x100; index1++)
	{
		for (index2 = index1, i = 0; i < 5; i++, index2 += 0x100)
		{
			unsigned long temp1, temp2;
			seed = (seed * 125 + 3) % 0x2AAAAB;
			temp1 = (seed & 0xFFFF) << 0x10;
			seed = (seed * 125 + 3) % 0x2AAAAB;
			temp2 = (seed & 0xFFFF);
			cryptTable[index2] = (temp1 | temp2);
		}
	}
}

/*
函数名:HashString
功能:计算字符串的哈希值
参数:lpszString:字符串的地址
	     dwHashType:哈希值类型
	     dwHashType = 0时计算的哈希值用于确定字符串在哈希表中的位置；
            dwHashType = 1，dwHashType = 2时计算的哈希值用于验证字符串
返回值:字符串的哈希值
*/
EXPORT unsigned long HashString(char *lpszString, unsigned long dwHashType)
{
	unsigned char *key = (unsigned char *)lpszString;
	unsigned long seed1 = 0x7FED7FED, seed2 = 0xEEEEEEEE;
	int ch;

	while(*key != 0)
	{
		ch = toupper(*key++);

		seed1 = cryptTable[(dwHashType << 8) + ch] ^ (seed1 + seed2);
		seed2 = ch + seed1 + seed2 + (seed2 << 5) + 3;
	}
	return seed1;
}

/*
函数名:MPQHashTableInit
功能:初始化哈希表
参数:*ppHashTable:返回分配的哈希表的地址
		nTableLength:哈希表的长度
返回值:0:失败
		    1:成功
*/
EXPORT char* MPQHashTableInit(char **ppHashTable, long nTableLength)
{
	long i = 0;
	char *p = NULL;
	MPQHASHTABLE *_pHashTable = NULL;
	
	/* 检查nTableLength是否为2的幂次方 */
	//assert(nTableLength&(nTableLength-1)==0);
	
	g_hash_mask = nTableLength - 1;

	InitCryptTable();
	
	p = malloc(nTableLength * sizeof(MPQHASHTABLE));
	if (p == NULL)
	{
		printf("%s, %d: malloc failed!\n", __FUNCTION__, __LINE__);
		return p;
	}
	*ppHashTable = p;
	_pHashTable = (MPQHASHTABLE *)p;
	
	for (i = 0; i < nTableLength; i++)
	{
		(_pHashTable + i)->nHashA = -1;
		(_pHashTable + i)->nHashB = -1;
		(_pHashTable + i)->bExists = 0;
	}
	
	return p;
}

/*
函数名:MPQHashTableFree
功能:释放哈希表
参数:pHashTable:哈希表的地址
返回值:无
*/
EXPORT void MPQHashTableFree(char *pHashTable)
{
	if (pHashTable != NULL)
	{
		free(pHashTable);
		pHashTable = NULL;
	}
}

/*
函数名:MPQHashTableAdd
功能:将字符串的信息加入哈希表
参数:lpszString:字符串的地址
	     pHashTable:哈希表的地址
返回值:0:失败
		    1:成功
*/
EXPORT unsigned int MPQHashTableAdd(char *lpszString, char *pHashTable)
{
	const unsigned long HASH_OFFSET = 0, HASH_A = 1, HASH_B = 2;
	unsigned long nHash = HashString(lpszString, HASH_OFFSET);
	unsigned long nHashA = HashString(lpszString, HASH_A);
	unsigned long nHashB = HashString(lpszString, HASH_B);
	unsigned long nHashStart = nHash & g_hash_mask;
	unsigned long nHashPos = nHashStart;
	MPQHASHTABLE *_pHashTable = (MPQHASHTABLE *)pHashTable;

	while ((_pHashTable + nHashPos)->bExists)
	{
		/*hash key already exists*/
		if (((_pHashTable + nHashPos)->nHashA == nHashA) && 
			((_pHashTable + nHashPos)->nHashB == nHashB))
		{
			return 1;
		}

		nHashPos = (nHashPos + 1)  & g_hash_mask;
		
		if (nHashPos == nHashStart)
		{
			return 0;
		}
	}
	
	(_pHashTable + nHashPos)->nHashA = nHashA;
	(_pHashTable + nHashPos)->nHashB = nHashB;
	(_pHashTable + nHashPos)->bExists = 1;

	return 1;
}

/*
函数名:MPQHashTableIsExist
功能:判断某字符串在哈希表中是否存在
参数:lpszString:字符串的地址
	     pHashTable:哈希表的地址
返回值:-1:不存在
		    nHashPos 该字符串在哈希表中的索引值
*/
EXPORT long MPQHashTableIsExist(char *lpszString, char *pHashTable)
{
	const unsigned long HASH_OFFSET = 0, HASH_A = 1, HASH_B = 2;
	unsigned long nHash = HashString(lpszString, HASH_OFFSET);
	unsigned long nHashA = HashString(lpszString, HASH_A);
	unsigned long nHashB = HashString(lpszString, HASH_B);
	unsigned long nHashStart = nHash & g_hash_mask;
	unsigned long nHashPos = nHashStart;
	MPQHASHTABLE *_pHashTable = (MPQHASHTABLE *)pHashTable;
	
	while ((_pHashTable + nHashPos)->bExists)
	{
		if (((_pHashTable + nHashPos)->nHashA == nHashA) && 
			((_pHashTable + nHashPos)->nHashB == nHashB))
		{
			return nHashPos;
		}
		else
		{
			nHashPos = (nHashPos +1) & g_hash_mask;
		}
		if (nHashPos == nHashStart)
		{
			break;
		}
	}
	return -1;
}

void test()
{	
	char *p = NULL;
	char *strs[] = {
		"t1", "t2", "t3"
	};
	long IsExits;
	int i;

	char *HashTablePos = MPQHashTableInit(&p, 10000);
	printf("pos of hashtable is %d\n", HashTablePos);

	for (i = 0; i < sizeof(strs) / sizeof(char*); ++i)
	{
		MPQHashTableAdd(strs[i], HashTablePos);
	}

	IsExits = MPQHashTableIsExist("t1", HashTablePos);
	printf("check if exists : %d", IsExits);
	getchar();
}

int main()
{
	//test();	
}
