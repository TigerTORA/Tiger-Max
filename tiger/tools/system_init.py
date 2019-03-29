#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..util.color import Color
from ..tools.hhdp import *
from ..tools.nav  import *
from ..util.process import Process
import os
def hhdp(args):
    instance = Base('/etc/hosts_list', args)
    work_manager = WorkManager(instance, 10)
    work_manager.wait_all_complete()

class System_init():
    """
    此类用来做集群主机初始化话操作
    """

    def __init__(self):
        self._check_string = "&&echo $(hostname)' --> OK'||echo $(hostname)' --> Failed'"
        self.hhdp_file = "/etc/hosts_list"
    def check_input(self,input):
	if input == "Y" or input == "y":
            pass
	else:
            os._exit(0)

    def cnf_check(self):
	#Step 01
	Color.pl("{+}Step(0/10): {G}let begin init linux system for hdp cloudera{W}")
	input = raw_input(Color.s("{+}Step(1/10): {G}do you have add the /etc/hosts to all cluster host?[y/n]:{W}"))
        self.check_input(input)	

	#Step 02
	if os.path.exists(self.hhdp_file):
	    command = """cat /etc/hosts_list|grep '^ip:'|awk '{print "{+}Info  "$1}'"""
	    (stdout, stderr) = Process.call(command)
	    Color.pl(stdout)
	    input = raw_input(Color.s("{+}Step(2/10): {G}I  will apply the change to the above list,is it OK?[y/n]:{W}"))
            self.check_input(input)
	else:
	    Color.pl("{+}Error: {R}I cannot file %s find {W}" %self.hhdp_file)
	    os._exiti(0)
	
	#step 03
        input = raw_input(Color.s("{+}Step(3/10): {G}i will config  the hostname,is it OK?[y/n]:{W}"))	
	if input == "Y" or input == "y":
	    self.cnf_hostname()
	else:
	    pass

	#step 04   
    def cnf_host(self):
        Color.pl("{R}备份: /etc/hosts文件{W}")
        hhdp(['none','-c',"cp /etc/hosts /etc/host_bak_$(date '+%Y%m%d%H%M%S')"+self._check_string])
        color_print("开始: 配置集群hosts文件")
        hhdp(['none','-f','/etc/hosts'])
        color_print("结束: 配置集群hosts文件")
        Nav.print_system_init()

    def cnf_hostname(self):
        Color.pl("{+}{Y}Begin:{W}Change hostname temporary{W}")
        hhdp(["none","-c","hostname $(grep -s $(ifconfig  | grep -s  'inet ' | awk '{ print $2}') /etc/hosts |awk '{print $2}')"+self._check_string])
	Color.pl("{+}{Y}Begin:{W}Change hostname permanent{W}")
        hhdp(["none","-c","hostnamectl set-hostname  $(grep -s $(ifconfig  | grep -s  'inet ' | awk '{ print $2}') /etc/hosts |awk '{print $2}')"+self._check_string])
	Color.pl("{+}{Y}End:{W}Change hostname{W}")

    def cnf_selinux(self):
        color_print("开始：临时关闭SElinux")
        hhdp(["none","-c","setenforce  0"+self._check_string])
        color_print("开始：永久关闭SElinux")
        hhdp(["none","-c","sed -i 's@\(SELINUX=\).*@\1disabled@g' /etc/selinux/config"+self._check_string])
        color_print("结束：配置SElinux")
        Nav.print_system_init()

    def cnf_iptables(self):
        color_print("开始：临时关闭iptables")
        hhdp(["none","-c","systemctl stop firewalld.service"+self._check_string])
        color_print("开始：禁止开机启动iptables")
        hhdp(["none","-c","systemctl disable firewalld.service"+self._check_string])
        color_print("结束：关闭iptables")
        Nav.print_system_init()

    def cnf_swap(self):
        color_print("开始：调整swap参数")
        hhdp(["none","-c",r"sed -i '$a\vm.swappiness = 0' /etc/sysctl.conf&&sysctl -p"+self._check_string])
        color_print("结束: 调整swap参数")
        Nav.print_system_init()

    def cnf_hugpage(self):
        color_print("开始：关闭redhat—tansparent")
        hhdp(["none","-c","echo never > /sys/kernel/mm/redhat_transparent_hugepage/defrag&&echo never > /sys/kernel/mm/redhat_transparent_hugepage/enabled"+self._check_string])

        color_print("开始：关闭transparent")
        hhdp(["none","-c","echo never > /sys/kernel/mm/transparent_hugepage/enabled;echo never > /sys/kernel/mm/transparent_hugepage/defrag"+self._check_string])

        color_print("开始：设置开机关闭transparent")
        hhdp(["none","-c","sed -i '$a\echo never > /sys/kernel/mm/redhat_transparent_hugepage/defrag' /etc/rc.local&&sed -i '$a\echo never > /sys/kernel/mm/redhat_transparent_hugepage/enabled' /etc/rc.local&&sed -i '$a\echo never > /sys/kernel/mm/transparent_hugepage/enabled' /etc/rc.local&&sed -i '$a\echo never > /sys/kernel/mm/transparent_hugepage/defrag' /etc/rc.local"+self._check_string])

        color_print("结束: 关闭transparent")
        Nav.print_system_init()

    def cnf_ntp(self):
        color_print("开始：配置ntp")
        hhdp(["none","-c",""+self._check_string])

        color_print("开始：停止ntp")
        hhdp(["none","-c","systemctl stop  ntpd"+self._check_string])

        color_print("开始: 同步一次时间")
        hhdp(["none","-c","systemctl stop  ntpd"+self._check_string])

        color_print("开始：开始ntp")
        hhdp(["none","-c","systemctl start  ntpd"+self._check_string])
        Nav.print_system_init()    
