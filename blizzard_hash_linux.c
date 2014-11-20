#include <stdio.h>
#include "blizzard_hash.h"
static unsigned int g_hash_mask = 0;

/************************************************************************/
/*������InitCryptTable
/*��  �ܣ��Թ�ϣ�����Ԥ����  
/*����ֵ����
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
������:HashString
����:�����ַ�Ĺ�ϣֵ
����:lpszString:�ַ�ĵ�ַ
	     dwHashType:��ϣֵ����
	     dwHashType = 0ʱ����Ĺ�ϣֵ����ȷ���ַ��ڹ�ϣ���е�λ�ã�
            dwHashType = 1��dwHashType = 2ʱ����Ĺ�ϣֵ������֤�ַ�
����ֵ:�ַ�Ĺ�ϣֵ
*/
unsigned long HashString(char *lpszString, unsigned long dwHashType)
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
������:MPQHashTableInit
����:��ʼ����ϣ��
����:*ppHashTable:���ط���Ĺ�ϣ��ĵ�ַ
		nTableLength:��ϣ��ĳ���
����ֵ:0:ʧ��
		    1:�ɹ�
*/
char* MPQHashTableInit(char **ppHashTable, long nTableLength)
{
	long i = 0;
	char *p = NULL;
	MPQHASHTABLE *_pHashTable = NULL;
	
	/* ���nTableLength�Ƿ�Ϊ2���ݴη� */
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
������:MPQHashTableFree
����:�ͷŹ�ϣ��
����:pHashTable:��ϣ��ĵ�ַ
����ֵ:��
*/
void MPQHashTableFree(char *pHashTable)
{
	if (pHashTable != NULL)
	{
		free(pHashTable);
		pHashTable = NULL;
	}
}

/*
������:MPQHashTableAdd
����:���ַ����Ϣ�����ϣ��
����:lpszString:�ַ�ĵ�ַ
	     pHashTable:��ϣ��ĵ�ַ
����ֵ:0:ʧ��
		    1:�ɹ�
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
������:MPQHashTableIsExist
����:�ж�ĳ�ַ��ڹ�ϣ�����Ƿ����
����:lpszString:�ַ�ĵ�ַ
	     pHashTable:��ϣ��ĵ�ַ
����ֵ:-1:������
		    nHashPos ���ַ��ڹ�ϣ���е�����ֵ
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
//		    printf("output is %ld\n", nHashPos);
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
