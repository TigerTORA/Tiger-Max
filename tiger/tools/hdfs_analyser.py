#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from ..util.color import Color
from ..util.process import Process


class Hdfs_analyser():
    def __init__(self):
	self.tmp_dir = "/tmp/"
	self.file_list = self.tmp_dir + "hdfs_flie_list.report"
	self.file_user = self.tmp_dir + "hdfs_file_user.report"
	self.file_size_01 = self.tmp_dir + "hdfs_file_size_128.report"
	self.file_size_02 = self.tmp_dir + "hdfs_file_size_64.report"
	
    def get_file_list(self):
	command =  "hdfs dfs -ls -R  /  > %s" %self.file_list
	Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command))
	(stdout, stderr) = Process.call(command)
	

    def user_analyser(self):
	command = '''grep '^-rw' %s | awk '{print $3" "$5}' | awk '{count[$1]++;sum[$1]=sum[$1]+$2}END{for(pol in sum)printf("%%-30s%%-15s%%-15s\\n","USER:"pol,count[pol],sum[pol]/1024^4)}'|sort -rnk 2 > %s''' % (self.file_list, self.file_user)
	Color.pl('{+} {D}Running: {W}{P}%s{W}' % ' '.join(command))
	(stdout, stderr) = Process.call(command)	
	print(stdout)

    def size_analyser(self):
	command_total = "grep '^-rw' %s|wc -l" %self.file_list
	command_small = "grep '^-rw' %s|awk '$5 <= 134217728'|wc -l"  %self.file_list
	command_small_1 = "grep '^-rw' %s|awk '$5 <= 67108864'|wc -l"  %self.file_list
	command_small_2 = "grep '^-rw' %s|awk '$5 <= 10485760'|wc -l"  %self.file_list
	(stdout_01, stderr) = Process.call(command_total)
	(stdout_02, stderr) = Process.call(command_small)
 	(stdout_03, stderr) = Process.call(command_small_1)
 	(stdout_04, stderr) = Process.call(command_small_2)
	Color.pl('{+} {W}The total files in hdfs is:{G}%d{W}' %float(stdout_01))
	Color.pl('{+} {W}The files  < 128M in hdfs is:{G}%d(%.3f){W}' % (float(stdout_02), float(int(stdout_02) / float(stdout_01))))
	Color.pl('{+} {W}The files  < 64 M in hdfs is:{G}%d(%.3f){W}' % (float(stdout_03), float(int(stdout_03) / float(stdout_01))))
	Color.pl('{+} {W}The files  < 10 M in hdfs is:{G}%d(%.3f){W}' % (float(stdout_04), float(int(stdout_04) / float(stdout_01))))
	

    def run_check(self):
	str = raw_input("Do you want to update the hdfs file list[y/n]:");
	if str == 'y':
	    self.get_file_list()
	    Color.pl('{+} {G}hdfs file list save in %s{W}' %self.file_list)
	else:
	    pass
	str = raw_input("Do you want to analyse hdfs file by own[y/n]:");
	if str == 'y':
	    self.user_analyser()
	    Color.pl('{+} {G}hdfs file own report save in %s, show the top 10:{W}' %self.file_user)
	    (stdout, stderr) = Process.call("head  -10  %s" %self.file_user)
	    print(stdout)
	self.size_analyser()
