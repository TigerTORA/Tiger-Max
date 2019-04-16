#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..util.color import Color
from ..tools.hhdp import *
from ..tools.nav  import *
from ..util.process import Process
import os
from ..tools.dependency import *

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
	self.ntpserver = "cn.pool.ntp.org"
	self.dependency_name = {
				"ifconfig":"yum install net-tools -y"
				,"lsb_release":"yum install -y redhat-lsb"
				,"ntpd":"yum install -y ntpd"
				}
	self.config_dict = {"hhdp":[
			        {"init_name":"configure hostname"
				,"conf_command":[
						{"Change hostname temporary":"hostname $(grep -s $(ifconfig  | grep -s  'inet ' | awk '{ print $2}') /etc/hosts |awk '{print $2}')"}
					       ,{"Change hostname permanent":"hostnamectl set-hostname  $(grep -s $(ifconfig  | grep -s  'inet ' | awk '{ print $2}') /etc/hosts |awk '{print $2}')"}
						]
				,"check_command":
						{"Hostname":"hostname -f"}
				}
			       ,{"init_name":"Close SElinux"
			       ,"conf_command":[
					       {"Close SElinux temporary":"setsetenforce  0"}
					       ,{"Close SElinux permanent":"sed -i 's@\(SELINUX=\).*@\\1disabled@g' /etc/selinux/config"}
						]
			       ,"check_command":
						{"SElinux status":"getenforce"}
				}
				,{"init_name":"Close firewall"
                               ,"conf_command":[
                                               {"Close firewall temporary":"systemctl stop firewalld.service"}
                                               ,{"Close firewall permanent":"isystemctl disable firewalld.service"}
                                                ]
                               ,"check_command":
                                               {"Firewall status":"systemctl status firewalld|grep Active"}
				}
				,{"init_name":"Turning swap"
                               ,"conf_command":[
                                               {"Turnign swap temporary":"sysctl vm.swappiness=0"}
                                               ,{"Turning swap permanent":"sed -i '/swappiness/d' /etc/sysctl.conf;sed -i '$a\\vm.swappiness = 0' /etc/sysctl.conf"}
                                                ]
                               ,"check_command":
                                               {"swap status":"grep 'swappiness' /etc/sysctl.conf"}
				}
				,{"init_name":"Close transparent hugepage"
                               ,"conf_command":[
                                               {"Close transparent hugepage temporary":"echo never > /sys/kernel/mm/transparent_hugepage/enabled;echo never > /sys/kernel/mm/transparent_hugepage/defrag"}
                                               ,{"Close transparent hugepage permanent":"sed -i '/transparent_hugepage/d' /etc/sysctl.conf;echo 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' >> /etc/rc.local&&echo 'echo never > /sys/kernel/mm/transparent_hugepage/defrag' >> /etc/rc.local"}
					       ,{"change /etc/rc.d/rc.local mod":"chmod +x /etc/rc.d/rc.local"}
                                                ]
                               ,"check_command":
                                               {"transparent hugepage status":'''echo -ne "$(cat /sys/kernel/mm/transparent_hugepage/enabled) $(cat /sys/kernel/mm/transparent_hugepage/defrag )\n"'''}
                                }
				,{"init_name":"Configure NTP"
                               ,"conf_command":[
                                               {"Annotate active server":"sed -i 's/^server/#&/' /etc/ntp.conf"}
					       ,{"Add ntp server":'''echo "server %s perfer" >> /etc/ntp.conf'''%self.ntpserver}
                                               ,{"Add backup server":"echo 'server 127.127.0.1' >> /etc/ntp.conf"}
					       ,{"One time rsync time":"systemctl stop ntpd;ntpdate %s"%self.ntpserver}
					       ,{"Enable and stat ntp":"systemctl enable ntpd;systemctl start ntpd"}
                                                ]
                               ,"check_command":
                                               {"ntp status":"ntpq -p"}
                                }	
			   ]}
    
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
                Color.p("{+} {G}Info: {W}IP:%s ==> %s:{G}%s{W}"%(ip,notes,status))

    def step_manger(self,step_num,step_name):
	for dict in  self.config_dict["hhdp"]:
	    if dict["init_name"] == step_name:
		self._check_method(dict["check_command"])
	        input = raw_input(Color.s("{+} {B}Step(%s/10): {G}Next will %s,is it OK?[y/n]:{W}"%(step_num,step_name)))	
		if input == "Y" or input == "y":
		    for command_dict in dict["conf_command"]:
	            	for notes,command in command_dict.items():
			     Color.pl("{+}{O} Begin: {W}%s{W}" %notes)
			     hhdp(["none","-c",command])
		else:
	    	    pass
		self._check_method(dict["check_command"])
                Color.pl("{+} {B}Step(%s/10): {G}%s finished(you can check the above info)"%(step_num,step_name))

    def cnf_check(self):
	#Step 01
        Dependency.fails_dependency_check_hhdp(self.dependency_name)
	Color.pl("{+} {B}Step(0/10): {G}let begin init linux system for hdp cloudera{W}")
	input = raw_input(Color.s("{+} {B}Step(0/10): {G}Plesse keyin the NTP server hostname or ip:{W}"))
	self.ntpserver = input 
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
        self.cm_server()	
	self.step_manger("03","configure hostname")
        self.step_manger("04","Close SElinux")
        self.step_manger("05","Close firewall")
	self.step_manger("06","Turning swap")
	self.step_manger("07","Close transparent hugepage")
	self.step_manger("08","Configure NTP")	

    def cm_server(self):
	dependency_name = {
                          "wget":"yum install wget -y"
                                }
	
	Color.pl("{+} {B}Step(0/5): {G}let begin install cm sercer{W}")
	Color.pl("{+} {B}Step(1/5): {G}donwload cm server repo{W}")
	command = ""
