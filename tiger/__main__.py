#!/usr/bin/env python
# -*- coding: utf-8 -*-
import textwrap
import os
import sys
import paramiko
import logging
from .util.color import Color
from .tools.hhdp import * 
from .tools.base_test  import *
from .tools.system_init import *
from .config import Configuration
from .tools.sysbench import *
from .tools.hdfsbench import *
from .tools.mapreduce_analyser import *
from .tools.hdfs_analyser import *
from .tools.hdfs_tuning import *

class Tiger():
    def __init__(self):
        """
        初始化操作：
            1）输出logo
            2）检查时候root运行
            3) 检查依赖
        """
        
        self.print_banner()
        if Configuration.run_as_root:
            if os.getuid() != 0:
                Color.pl('{!} {R}error: {O}tiger{R} must be run as {O}root{W}')
                Color.pl('{!} {R}re-run with {O}sudo{W}')
                Configuration.exit_gracefully(0)

        from .tools.dependency import Dependency
        Dependency.run_dependency_check()

    def print_banner(self):
        Color.pl(r'{W}***************************************************')
        Color.pl(r'{B}*▀▛▘ {O}▗  {G}    {R}    {P}   *  {B}tiger {D}1.0{W}')
        Color.pl(r'{B}* ▌  {O}▄  {G}▞▀▌ {R}▞▀▖ {P}▙▀▖*  {B}Bigdata Cluster Manager Tool')
        Color.pl(r'{B}* ▌  {O}▐  {G}▚▄▌ {R}▛▀  {P}▌  *  {B}https://github.com/tiger{W}')
        Color.pl(r'{B}* ▘  {O}▀▘ {G}▗▄▘ {R}▝▀▘ {P}▘  *  {B}Author:LUOHU')
        Color.pl(r'{W}***************************************************')

def main():
    """
    he he
    主程序
    """
    tiger = Tiger()
    nav = Nav()
    nav.print_main()
    system_init = System_init()
    while True:
        try:
            option = raw_input(("\033[1;32mOpt or ID>:\033[0m ").strip())
        except EOFError:
            nav.print_main()
            contnue
        except KeyboardInterrupt:
                sys.exit(0)

        if option in  ['1']:
            nav.print_system_init()
        elif option in ['2']:
            nav.print_manager_hdfs()
        elif option in ['3']:
            nav.print_manager_yarn()
        elif option in ['5']:
            nav.print_manager_hive()
        elif option in ['4']: 
            nav.print_manager_hbase()
        elif option in ['a']:
            nav.print_manager_linux()
	elif option in ['00']:
	    system_init.cnf_check()
        elif option in ['11']:
            system_init.cnf_host()
        elif option in ['12']:
            system_init.cnf_hostname()
        elif option in ["13"]:
            system_init.cnf_selinux()
        elif option in ['14']:
            system_init.cnf_iptables()
        elif option in ['15']:
            system_init.cnf_swap()
        elif option in ['16']:
            system_init.cnf_hugpage()
        elif option in ['17']:
            system_init.cnf_ntp()
        elif option in ['21']:
            Hdfsbench.bench_io()
        elif option in ['22']:
            analyser  = Hdfs_analyser()
            analyser.run_check()
        elif option in ['31']:
            manger_yarn.yarn_base_test()
        elif option in ['33']:
            mr_analyser = MR_analyser()
            mr_analyser.check_job("job_1543555458144_0102")
        elif option in ['41']:
            manger_hbase.hbase_base_test()
        elif option in ['a1']:
            Sysbench.bench_all()
if __name__=="__main__":
    main()
