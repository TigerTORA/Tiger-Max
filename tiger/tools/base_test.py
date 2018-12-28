#!/usr/bin/env python2.7
# coding: utf-8
import os
import re
from prettytable import PrettyTable
from .dependency import Dependency
from ..util.process import Process
from ..config import Configuration
from ..tools.hhdp  import hhdp
def color_print(msg, color='red', exits=False):
    """
    Print colorful string.
    颜色打印字符或者退出
    """
#    color_msg = {
#        'blue': '\033[1;36m%s\033[0m',
#        'green': '\033[1;32m%s\033[0m',
#        'yellow': '\033[1;33m%s\033[0m',
#        'red': '\033[1;31m%s\033[0m',
#        'title': '\033[30;42m%s\033[0m',
#        'info': '\033[32m%s\033[0m'
#    }
#    msg = color_msg.get(color, 'red') % msg
#    print msg
#    if exits:
#        time.sleep(2)
#        sys.exit()
#    return msg

class manger_hdfs():
    @staticmethod
    def hdfs_base_test():

	color_print("开始：清除读写测试数据")
	os.system('hadoop jar $(find / -name hadoop-test-mr1.jar)  TestDFSIO -clean > /tmp/TestDFSIO_clean.log  2>&1')
	color_print("开始：hdfs IO 写入测试")
	os.system('hadoop jar $(find / -name hadoop-test-mr1.jar)  TestDFSIO -write -nrFiles 1 -fileSize 16GB -resFile TestDFSIO_write_result > /tmp/TestDFSIO_write.log 2>&1 && echo  -e "\033[32m $(cat TestDFSIO_write_result)\033[0m"')
	color_print("开始：hdfs IO 读取测试")
	os.system('hadoop jar $(find / -name hadoop-test-mr1.jar)  TestDFSIO -read  -nrFiles 1 -fileSize 16GB -resFile TestDFSIO_read_result > /tmp/TestDFSIO_read.log 2>&1 && echo  -e "\033[32m $(cat TestDFSIO_read_result)\033[0m"')
	color_print("开始：清除读写测试数据")
        os.system('hadoop jar $(find / -name hadoop-test-mr1.jar)  TestDFSIO -clean')
	color_print("开始： namenode SliveTest")
	os.system("hadoop jar $(find / -name hadoop-mapreduce-client-jobclient-tests.jar)   SliveTest")

class manger_yarn():
    @staticmethod
    def yarn_base_test():
	color_print("开始：清除wordcount测试数据")
	os.system("hadoop fs -rmr -skipTrash /tmp/wordcount-input;hadoop fs -rmr -skipTrash /tmp/wordcount-output")
	color_print("开始：生成wordcount测试数据")
	os.system("hadoop jar $(find / -name  hadoop-examples.jar|tail -n 1)  randomtextwriter  /tmp/wordcount-input")
	color_print("开始：执行wordcount程序")
	os.system("hadoop jar $(find / -name  hadoop-examples.jar|tail -n 1)  wordcount /tmp/wordcount-input /tmp/wordcount-output")
	color_print("开始：清除wordcount测试数据")
        os.system("hadoop fs -rmr -skipTrash /tmp/wordcount-input;hadoop fs -rmr -skipTrash /tmp/wordcount-output")

	color_print("开始：清除teragen测试数据")
	os.system("hadoop fs -rmr -skipTrash /tmp/teragen-input;hadoop fs -rmr -skipTrash /tmp/teragen-output;hadoop fs -rmr -skipTrash /tmp/teragen-teravalidate")
	color_print("开始：生成teragen测试数据")
	os.system("hadoop jar $(find / -name  hadoop-examples.jar|tail -n 1)  teragen 1000000  /tmp/teragen-input")
	color_print("开始：执行tersort程序")
        os.system("hadoop jar $(find / -name  hadoop-examples.jar|tail -n 1)  terasort  /tmp/teragen-input /tmp/teragen-output")
	color_print("开始：执行tervalidate程序")
	os.system("hadoop jar $(find / -name  hadoop-examples.jar|tail -n 1)  teravalidate   /tmp/teragen-output /tmp/teragen-teravalidate")
	color_print("开始：清除teragen测试数据")
        os.system("hadoop fs -rmr -skipTrash /tmp/teragen-input;hadoop fs -rmr -skipTrash /tmp/teragen-output;hadoop fs -rmr -skipTrash /tmp/teragen-teravalidate")

class manger_hbase():
    @staticmethod
    def hbase_base_test():
	color_print("开始：hbase 顺序写测试")
	os.system("hbase pe  --nomapred sequentialWrite 1")
	color_print("开始：hbase 顺序读测试")
	os.system("hbase pe  --nomapred sequentialRead 1")
	color_print("开始：hbase 随机写测试")
	os.system("hbase pe  --nomapred randomWrite 1")
	color_print("开始：hbase 随机读测试")
	os.system("hbase pe  --nomapred randomRead 1")
	color_print("开始：hbase 并发顺序写测试")
	os.system("hbase pe  --nomapred sequentialWrite 100")
	color_print("开始：hbase 并发顺序读测试")
	os.system("hbase pe  --nomapred sequentialRead 100")
	color_print("开始：hbase 并发随机写测试")
	os.system("hbase pe  --nomapred randomWrite 100")
	color_print("开始：hbase 并发随机读测试")
	os.system("hbase pe  --nomapred randomRead 100")
	color_print("开始：hbase randomRead测试")
