#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..util.color import Color
from ..tools.hhdp import *
from ..tools.nav  import *
from ..util.process import Process
import os

class System_init():
    dependency_required = True
    dependency_name = {
			"ifconfig":"yum install net-tools -y",
			}
    """
    此类用来做集群主机初始化话操作
    """

    def __init__(self):
        self._check_string = "&&echo $(hostname)' --> OK'||echo $(hostname)' --> Failed'"
        self.hhdp_file = "/etc/hosts_list"
	self.dependency_required = True
	self.dependency_name = {
				"ifconfig":"yum install net-tools -y",
				}
	self.config_dict = {"hhdp":[
			        {"init_name":"configure hostname"
				,"conf_command":
						{"Change hostname temporary":"hostname $(grep -s $(ifconfig  | grep -s  'inet ' | awk '{ print $2}') /etc/hosts |awk '{print $2}')"
						,"Change hostname permanent":"hostnamectl set-hostname  $(grep -s $(ifconfig  | grep -s  'inet ' | awk '{ print $2}') /etc/hosts |awk '{print $2}')"
						}
				,"check_command":
						{"Hostname":"hostname -f"}
				}
			       ,{"init_name":"Close SElinux"
			       ,"conf_command":
					       {"Close SElinux temporary":"setsetenforce  0"
					       ,"Close SElinux permanent":"sed -i 's@\(SELINUX=\).*@\1disabled@g' /etc/selinux/config"
						}
			       ,"check_command":
						{"SElinux status":"getenforce"}
				}
				,{"init_name":"Close firewall"
                               ,"conf_command":
                                               {"Close firewall temporary":"systemctl stop firewalld.service"
                                               ,"Close firewall permanent":"isystemctl disable firewalld.service"
                                                }
                               ,"check_command":
                                               {"Firewall status":"systemctl status firewalld|grep Active"}
				}
			   ]}
    
    def fails_dependency_check_hhdp(self,dict):
        for key,name in self.dependency_name.items():
            command = ['none', "-c", "which "+key]
            ress = hhdp(command)
            for res in ress:
		ip = res[0]
		stdout = res[1]
		stderr = res[2]
                if stderr:
                        Color.pl('{!} {R}Error: {W}Required app {R}%s{W} was not found in host {R}%s,refer to:%s{W}' % (key,ip,name))
                else:
                        Color.pl('{+} {G}Info: {W}Required app {R}%s{W} was  found in host {G}%s{W}' % (key,ip))

    def check_input(self,input):
	if input == "Y" or input == "y":
            pass
	else:
            os._exit(0)
	
    def _cnf_method(self,command_dict):
        for command,notes in command_dict.items():
            Color.pl("{+}{O} Begin: {W}%s{W}" %notes)
            hhdp(["none","-c",command])

    def _check_method(self,check_command):
	for notes,command in check_command.items():
            ress = hhdp(["None","-c",command])
            for res in ress:
                ip = res[0]
                status = res[1]
                Color.p("{+} {G}Info: {W}IP:%s ==> %s:%s{W}"%(ip,notes,status))

    def step_manger(self,step_num,step_name):
	for dict in  self.config_dict["hhdp"]:
	    if dict["init_name"] == step_name:
		self._check_method(dict["check_command"])
	        input = raw_input(Color.s("{+} {B}Step(%s/10): {G}Next will %s,is it OK?[y/n]:{W}"%(step_num,step_name)))	
		if input == "Y" or input == "y":
	            for notes,command in dict["conf_command"].items():
			 Color.pl("{+}{O} Begin: {W}%s{W}" %notes)
			 hhdp(["none","-c",command])
		else:
	    	    pass
		self._check_method(dict["check_command"])
                Color.pl("{+} {B}Step(%s/10): {G}%s finished(you can check the above info)"%(step_num,step_name))

    def cnf_check(self):
	#Step 01
        self.fails_dependency_check_hhdp(self.dependency_name)
	Color.pl("{+} {B}Step(0/10): {G}let begin init linux system for hdp cloudera{W}")
	input = raw_input(Color.s("{+} {B}Step(1/10): {G}do you have add the /etc/hosts to all cluster host?[y/n]:{W}"))
        self.check_input(input)	

	#Step 02
	if os.path.exists(self.hhdp_file):
	    command = """cat /etc/hosts_list|grep '^ip:'|awk '{print "{+} {G}Info  {W}"$1}'"""
	    (stdout, stderr) = Process.call(command)
	    Color.p(stdout)
	    input = raw_input(Color.s("{+} {B}Step(2/10): {G}I  will apply the change to the above list,is it OK?[y/n]:{W}"))
            self.check_input(input)
	else:
	    Color.pl("{+}Error: {R}I cannot file %s find {W}" %self.hhdp_file)
	    os._exiti(0)
	
	self.step_manger("03","configure hostname")
        self.step_manger("04","Close SElinux")
        self.step_manger("05","Close firewall")
	
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
