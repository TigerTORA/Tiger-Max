#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from prettytable import PrettyTable

from .dependency import Dependency
from ..util.process import Process
from ..config import Configuration
from ..tools.hhdp  import hhdp
class Hdfsbench(Dependency):
    """
    使用hadoop对系统进行基准检测
        IO bench：
            sysbench fileio --file-block-size=10 prepare
            sysbench fileio --file-total-size=10G --file-test-mode=rndrw  run
            sysbench --test=fileio --file-total-size=150G cleanup

        CPU bench:找出最大events per second，
            sysbench --test=cpu --num-threads=16 --cpu-max-prime=60000  run
        
        memory bench:每秒传输速度
            sysbench --threads=4  --memory-block-size=8k --memory-total-size=4G memory run



    """
    dependency_required = True
    dependency_name = 'hdfs'
    dependency_url = 'Not a hdfs gataway'
    
    
    @staticmethod
    def bench_io(show_command=True):
        from ..util.color import Color
        from ..util.timer import Timer
       
        clean = ["hadoop jar $(find / -name hadoop-test-mr1.jar|tail -n 1)  TestDFSIO -clean"]
        write = ["hadoop jar $(find / -name hadoop-test-mr1.jar|tail -n 1)  TestDFSIO -write -nrFiles 1 -fileSize 1GB -resFile /tmp/TestDFSIO_write.log"]
	read = ["hadoop jar $(find / -name hadoop-test-mr1.jar|tail -n 1)  TestDFSIO -read  -nrFiles 1 -fileSize 1GB -resFile /tmp/TestDFSIO_read.log"]
      	cat = ["cat /tmp/TestDFSIO_*"]

	command_list = [clean,write,read,clean,cat]
	io_res_dict = {}
	for command  in command_list:
		if show_command:
			Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command)) 
		(stdout, stderr) = Process.call(command)
		io_type = re.search('.* ----- TestDFSIO ----- : *?(\w+).*', stderr)
		io_speed = re.search('.*Average IO rate mb/sec: .*?(\d+.\d+).*', stderr)
		if io_type and io_speed:
			io_res_dict.update({io_type.group(1):io_speed.group(1)})
	print io_res_dict
