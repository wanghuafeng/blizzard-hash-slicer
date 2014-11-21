blizzard-hash-slicer（data中词表为裁剪后词表）
====================
	
暴雪哈希表作为存储的切词算法

usage: python test.py slicer sentence

	例:python test.py slicer 对哈希索引表的算法行封装

性能参数:

最大词长:MAXLEN = 8

切词速度:223.32KB/s

***************************************

slicer_using_python_set 使用python自带存储哈希结构：set

最大词长:MAXLEN = 8

切词速度:1743.63KB/s

linux平台编译.so文件：

command = r'gcc blizzard_hash_linux.c -fPIC -shared -o data/blizzard_hash.so'

os.system(command)
