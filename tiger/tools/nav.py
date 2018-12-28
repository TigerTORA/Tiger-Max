#!/usr/bin/env python
# -*- coding: utf-8 -*-
import textwrap
from ..util.color import Color

class Nav():
    @staticmethod
    def print_main():
        """
        Print prompt
        打印提示导航主页
        """

        msg = Color.s("""\n{G}###    欢迎使用tiger max大数据集群管理工具   ### {W}
        1) 输入 {G}1{W}     大数据集群主机初始化
        2) 输入 {G}2{W}     管理 hdfs   服务
        3) 输入 {G}3{W}     管理 Yarn   服务
        4) 输入 {G}4{W}     管理 hbase  服务
        5) 输入 {G}5{W}     管理 hive   服务
        6) 输入 {G}6{W}     管理 spark  服务
        7) 输入 {G}7{W}     管理 impala 服务
       11) 输入 {G}a{W}     管理 linux  系统

        0) 输入 {G}q{W} 退出.
        """)
        print textwrap.dedent(msg)

    @staticmethod
    def print_system_init():
        """
        打印提示导航栏大数据集群初始化
        """
        msg = Color.s("""\n{G}###    tiger-max当前页面:大数据集群主机初始化    ###{W}

        1) 输入 {G}11{W}    集群配置hosts文件
        2) 输入 {G}12{W}    集群配置hostname
        3) 输入 {G}13{W}    集群关闭SElinux
        4) 输入 {G}14{W}    集群关闭iptbales
        5) 输入 {G}15{W}    关闭集群交换内存
        6) 输入 {G}16{W}    修改 transparent_hugepage 参数
        7) 输入 {G}17{W}    配置ntp服务
        8) 输入 {G}18{W}    安装java和jce文件
        8) 输入 {G}19{W}    安装mysql jdbc


        9) 输入 {G}p{W}    返回上一页
        0) 输入 {G}q{W}    退出
        """)
        print textwrap.dedent(msg)

    @staticmethod
    def print_manager_hdfs():
        """
        打印提示导航栏管理hdfs服务
        """
        msg = Color.s("""\n{G}###    tiger-max当前页面:管理hdfs服务    ###{W}

        1) 输入 {G}21{W}    hdfs基准检测
        2) 输入 {G}22{W}    hdfs性能参数优化

        9) 输入 {G}p{W}    返回上一页
        0) 输入 {G}q{W}    退出
        """)

        print textwrap.dedent(msg)

    @staticmethod
    def print_manager_yarn():
        """
        打印提示导航栏管理yarn服务
        """
        msg = Color.s("""\n{G}###    tiger-max当前页面:管理hive服务    ###{W}

        1) 输入 {G}31{W}    mapreduce基准检测
        2) 输入 {G}32{W}    mapreduce性能参数优化
        3) 输入 {G}33{W}    mapreduce任务检查

        9) 输入 {G}p{W}    返回上一页
        0) 输入 {G}q{W}    退出
        """)

        print textwrap.dedent(msg)

    @staticmethod
    def print_manager_hbase():
        """
        打印提示导航栏管理hbaes服务
        """
        msg = Color.s("""\n{G}###    tiger-max当前页面:管理hbase服务    ###{W}

        1) 输入 {G}41{W}    hbase基准检测
        2) 输入 {G}42{W}    hbase性能参数优化

        9) 输入 {G}p{W}    返回上一页
        0) 输入 {G}q{W}    退出
	""")
	print textwrap.dedent(msg)
	
    @staticmethod
    def print_manager_linux():
	"""
	打印提示导航栏管理linux服务
	"""
	msg = Color.s("""\n{G}###    tiger-max当前页面:管理linux系统    ###{W}

        1) 输入 {G}a1{W}    linux基准检测
        2) 输入 {G}a2{W}    linux性能参数优化

        9) 输入 {G}p{W}    返回上一页
        0) 输入 {G}q{W}    退出
        """)
        print textwrap.dedent(msg)