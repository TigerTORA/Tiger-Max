#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..util.history_url_utils import *

class MRdataCollector():
    @staticmethod
    def base_task_Collector(job_id,task_type,conter_type,conter_name):
        conter_list = History_util.get_task_conter(job_id)
        values = []
        for conter in  conter_list:
             if task_type  in conter["jobTaskCounters"]["id"]:
                counterGroup  = conter["jobTaskCounters"]["taskCounterGroup"]
                for iterms in counterGroup:
                    if iterms["counterGroupName"] == conter_type:
                        for iterm in iterms["counter"]:
                            if iterm["name"] == conter_name:
                                val = iterm["value"]
                                values.append(val)
        return values               

    @staticmethod
    def info_task_Collector(job_id,task_type,base_type_type):
        base_list =  History_util.get_task_base(job_id)
        values = []
        for base in  base_list:
             if task_type  in base["task"]["id"]:
                 val = base["task"][base_type_type]
                 values.append(val)
        return values

    @staticmethod    
    def conf_job_Collector(job_id,conf_name):
        conf_dict =  History_util.get_job_conf(job_id)
        values = conf_dict["conf"]["property"]
        for value in values:
            print value["name"]
            if value["name"] == conf_name:
                return value["value"]
    
