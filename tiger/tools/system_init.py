#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..util.color import Color
from ..tools.hhdp import *
from ..tools.nav  import *

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

    def cnf_host(self):
        Color.pl("{R}备份: /etc/hosts文件{W}")
        hhdp(['none','-c',"cp /etc/hosts /etc/host_bak_$(date '+%Y%m%d%H%M%S')"+self._check_string])
        color_print("开始: 配置集群hosts文件")
        hhdp(['none','-f','/etc/hosts'])
        color_print("结束: 配置集群hosts文件")
        Nav.print_system_init()

    def cnf_hostname(self):
        color_print("开始：临时更改主机名")
        hhdp(["none","-c","hostname $(grep -s $(ifconfig  | grep -s  'inet ' | awk '{ print $2}') /etc/hosts |awk '{print $2}')"+self._check_string])
        color_print("开始：永久更改主机名")
        hhdp(["none","-c","hostnamectl set-hostname  $(grep -s $(ifconfig  | grep -s  'inet ' | awk '{ print $2}') /etc/hosts |awk '{print $2}')"+self._check_string])
        color_print("结束：配置主机名")
        Nav.print_system_init()

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
