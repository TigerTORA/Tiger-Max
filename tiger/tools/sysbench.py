#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from prettytable import PrettyTable

from .dependency import Dependency
from ..util.process import Process
from ..config import Configuration
from ..tools.hhdp  import hhdp
class Sysbench(Dependency):
    """
    使用sysbench对系统进行基准检测
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
    dependency_name = 'sysbench'
    dependency_url = 'yum  install sysbench'
    
    
    @staticmethod
    def bench_fileio(show_command=True):
        from ..util.color import Color
        from ..util.timer import Timer
        ress_dict = {}
        command_pre = [
                'none',
                '-c',
                "sysbench fileio --file-total-size=3G prepare"
                ]

        command_run = [
                'none',
                '-c',
                "sysbench fileio --file-total-size=3G --file-test-mode=rndrw run"
                ]

        command_cleanup = [
                'none',
                '-c',
                "sysbench fileio --file-total-size=3G cleanup "
                ]
        
        if show_command:
            Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command_pre))
        hhdp(command_pre)

        if show_command:
            Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command_run))
        ress = hhdp(command_run)

        if show_command:
            Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command_cleanup))
        hhdp(command_run)

        for res in ress:
            hostname = res[0]
            stdout = res[1]
            stderr = res[2]
            io_read = re.search('.*read, MiB/s:.*?(\d+.\d+).*', stdout)
            io_write = re.search('.*written, MiB/s:.*?(\d+.\d+).*', stdout)
            res_dict =  {hostname:
                            {"io_read":io_read.group(1),
                             "io_write":io_read.group(1)
                            }
                        }
            ress_dict.update(res_dict)

        return ress_dict

    @staticmethod
    def bench_cpu(show_command=True):
        from ..util.color import Color
        from ..util.timer import Timer
        ress_dict = {}
        command = [
                'hhdp',
                '-c',
                "sysbench cpu --threads=8 --cpu-max-prime=50000 run"
                ]

        if show_command:
            Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command))
        ress = hhdp(command)


        for res in ress:
            hostname = res[0]
            stdout = res[1]
            stderr = res[2]
            cpu_speed = re.search('.*events per second:.*?(\d+.\d+).*', stdout)
            res_dict =  {hostname:
                            {"cpu_speed":cpu_speed.group(1)
                            }
                        }
            ress_dict.update(res_dict)

        return ress_dict

    @staticmethod
    def bench_memory(show_command=True):
        from ..util.color import Color
        from ..util.timer import Timer
        ress_dict = {}
        command = [
                'hhdp',
                '-c',
                "sysbench memory --threads=8  --memory-block-size=8k --memory-total-size=4G  run"
                ]

        if show_command:
            Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command))
        ress = hhdp(command)


        for res in ress:
            hostname = res[0]
            stdout = res[1]
            stderr = res[2]
            memory_speed = re.search('.*transferred \\(.*?(\d+.\d+).*', stdout)
            res_dict =  {hostname:
                            {"memory_speed":memory_speed.group(1)
                            }
                        }
            ress_dict.update(res_dict)

        return ress_dict

    @staticmethod
    def bench_all(show_command=True):
        ress_dict_all = {}

        ress_dict_io = Sysbench.bench_fileio()        
        ress_dict_cpu = Sysbench.bench_cpu()
        ress_dict_memory = Sysbench.bench_memory()
            
        for k in ress_dict_io:
            if k in ress_dict_cpu:
                ress_dict_io[k].update(ress_dict_cpu[k])

        for k in ress_dict_io:
            if k in ress_dict_memory:
                ress_dict_io[k].update(ress_dict_memory[k])
        
        ress_dict_all = ress_dict_io
        Sysbench.display(ress_dict_all)

    @staticmethod    
    def display(ress_dict_all):
        from ..util.color import Color
        ptable = PrettyTable([Color.s('{G}hostname{W}'),
                              Color.s('{G}IO_read{W}'), 
                              Color.s('{G}IO_write{W}'), 
                              Color.s('{G}CPU_speed{W}'), 
                              Color.s('{G}Meomery_speed{W}')])

        for key in ress_dict_all:
            io_read = ress_dict_all[key]['io_read']
            io_write = ress_dict_all[key]['io_write']
            cpu_speed = ress_dict_all[key]['cpu_speed']
            memory_speed = ress_dict_all[key]['memory_speed']
            value_list=[Color.s("{R}"+key+"{W}"),io_read,io_write,cpu_speed,memory_speed]
            ptable.add_row(value_list)
        print(ptable)

if __name__ == '__main__':
    Sysbench.fileio()
