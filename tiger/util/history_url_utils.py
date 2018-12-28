#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
from ..config import Configuration
from ..util.process import Process

class History_util():
    history_host = Configuration.history_host
    history_port = Configuration.history_port
    history_url = "http://%s:%s" %(history_host,history_port)
    job_api = "%s/ws/v1/history/mapreduce/jobs/" %history_url 
    
    @staticmethod
    def get_task_id(job_id):
        """
        获取job的task id 列表
        """
        command = "curl %s" %(History_util.job_api+job_id+"/tasks")
        (stdout,stderr) = Process.call(command)
        tasks_dict = json.loads(stdout)
        task_id_list = []
        for task  in tasks_dict["tasks"]["task"]:
            task_id_list.append(task['id'])
        
        return task_id_list

    @staticmethod
    def get_task_attempt_id(job_id):
        """
        获取job的task id和attempt id的映射字典
        """
        task_attempt_dicks= {}
        task_id_list = History_util.get_task_id(job_id)
        for task_id in task_id_list:
            command = "curl "+History_util.job_api+job_id+"/tasks/"+task_id+"/attempts"
            print command
            (stdout,stderr) = Process.call(command)
            attempt_dict = json.loads(stdout)
            attempt_id_list = []
            for attempt in attempt_dict["taskAttempts"]["taskAttempt"]:
                attempt_id_list.append(attempt['id'])
            task_attempt_dicks.update({task_id:attempt_id_list})
        return task_attempt_dicks

    @staticmethod        
    def get_success_task_attempt_id(job_id):
        """
        获取job的task id和success attempt id的映射字典
        """
        success_task_attempt_dicks= {}
        task_id_list = History_util.get_task_id(job_id)
        for task_id in task_id_list:
            command = "curl "+History_util.job_api+job_id+"/tasks/"+task_id+"/attempts"
            print command
            (stdout,stderr) = Process.call(command)
            attempt_dict = json.loads(stdout)
            attempt_id_list = []
            for attempt in attempt_dict["taskAttempts"]["taskAttempt"]:
                if attempt['state'] == "SUCCEEDED":
                    attempt_id_list.append(attempt['id'])
            success_task_attempt_dicks.update({task_id:attempt_id_list})
        print success_task_attempt_dicks
        return success_task_attempt_dicks

    @staticmethod
    def get_task_conter(job_id):
        """
        获取job的task_id和conter信息的映射字典
        {id:,
         taskCounterGroup:
            [{counter:[{},{},{},{}],{counterGroupName:},{}]
        """
        conter_list = []
        task_id_list = History_util.get_task_id(job_id)
        for task_id in task_id_list:
            command = ("curl "+History_util.job_api+job_id+"/tasks/"+task_id+"/counters")
            (stdout,stderr) = Process.call(command)
            conter_dict = json.loads(stdout)
            conter_list.append(conter_dict)
        return conter_list
    
    @staticmethod
    def get_task_base(job_id):
        base_list = []
        task_id_list = History_util.get_task_id(job_id)
        for task_id in task_id_list:
            command = ("curl "+History_util.job_api+job_id+"/tasks/"+task_id)
            (stdout,stderr) = Process.call(command)
            base_dict = json.loads(stdout)
            base_list.append(base_dict)
        return base_list

    @staticmethod
    def get_job_conf(job_id):
        command = ("curl "+History_util.job_api+job_id+"/conf")
        print command
        (stdout,stderr) = Process.call(command)
        print stdout
        conf_dict = json.loads(stdout)
        return conf_dict
