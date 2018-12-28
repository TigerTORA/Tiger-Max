#!/usr/bin/env python
 # -*- coding: utf-8 -*-
from prettytable import PrettyTable
from .datacollector  import *
from ..util.color import Color
from ..config import Configuration
from .heuristics import *

class MR_analyser():
    def __init__(self):
        self.check_items = Configuration.check_items

    def check_job(self,job_id):
        heuristic  = Heuristic(job_id)
        data_list = heuristic.run_all_heuristic()
        for data in data_list:
            ptable = PrettyTable([Color.s('{C}iterm{W}'),
                                  Color.s('{C}value{W}')
                                 ])
            for iterm in data:
                if "结果" in iterm["name"]:
                    Color.pl("{+}*****{O}%s   :%s " % (iterm["name"],iterm["value"]))
                else:
                    value_list=[Color.s("{B}"+iterm["name"]+"{W}"),Color.s("{R}"+str(iterm["value"])+"{W}")]
                    ptable.add_row(value_list)
            print(ptable)

