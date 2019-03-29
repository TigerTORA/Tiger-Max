#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml.etree import ElementTree
import os
import sys
from ..util.color import Color
from pprint import pprint



class hdfs_tuner():
    def __init__(self):
        self.hdfs_site = "/etc/hadoop/conf/hdfs-site.xml"

    def get_property(self,conf,name):
        dom = ElementTree.parse(conf)
        property = dom.findall('property')
        for p in property:
            n = p.find('name').text
            v = p.find('value').text
            if n == name:
                return v
    
    def checker(self,conf,avalue,rvalue):
        if avalue == rvalue:
            Color.pl("{+}    {C}conf:{O}%s, {C}actual values:{G}%s{W}" % (conf,avalue))
        else:
            Color.pl("{!}    {C}conf:{O}%s, {C}actual values:{R}%s, {C}recommended value:{G}%s{W}" %(conf,avalue,rvalue))

    def check_blocksize(self):
        conf = "dfs.blocksize"
        a_blocksize = self.get_property(self.hdfs_site,conf)
        r_blocksize = "134217728"
        self.checker(conf,a_blocksize,r_blocksize)

    def check_replication(self):
        conf = "dfs.replication"
        a_replication = self.get_property(self.hdfs_site,conf)
        r_replication = "3"
        self.checker(conf,a_replication,r_replication)

    def run_check(self):
        self.check_blocksize()
	self.check_replication()

