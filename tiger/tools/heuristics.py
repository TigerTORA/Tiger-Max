#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .datacollector  import *
from ..util.color import Color
from ..config import Configuration

class Heuristic():
    def __init__(self,job_id):
        self.job_id = job_id
        Color.pl("{+}    {C}获取 map 任务 read 数据{W}")
        self.m_read_list = MRdataCollector.base_task_Collector(job_id,"m","org.apache.hadoop.mapreduce.FileSystemCounter","HDFS_BYTES_READ")
        Color.pl("{+}    {C}获取 map 任务 cpu 时间  数据{W}")
        self.m_cpu_list = MRdataCollector.base_task_Collector(job_id,"m","org.apache.hadoop.mapreduce.TaskCounter","CPU_MILLISECONDS")
        Color.pl("{+}    {C}获取 map 任务 GC 时间 数据{W}")
        self.m_gc_list = MRdataCollector.base_task_Collector(job_id,"m","org.apache.hadoop.mapreduce.TaskCounter","GC_TIME_MILLIS")
        Color.pl("{+}    {C}获取 map 任务 运行总时间 数据{W}")
        self.m_time_list = MRdataCollector.info_task_Collector(job_id,"m","elapsedTime")
        Color.pl("{+}    {C}获取 map 任务 output record 数据{W}")
        self.m_out_r_list = MRdataCollector.base_task_Collector(job_id,"m","org.apache.hadoop.mapreduce.TaskCounter","MAP_OUTPUT_RECORDS")
        Color.pl("{+}    {C}获取 map 任务 spill record 数据{W}")
        self.m_spilled_r_list = MRdataCollector.base_task_Collector(job_id,"m","org.apache.hadoop.mapreduce.TaskCounter","SPILLED_RECORDS")
        Color.pl("{+}    {C}获取 map 任务 使用物理内存 数据{W}")
        self.m_ph_memory_list = MRdataCollector.base_task_Collector(job_id,"m","org.apache.hadoop.mapreduce.TaskCounter","PHYSICAL_MEMORY_BYTES")
        Color.pl("{+}    {C}获取 map 任务 使用虚拟内存 数据{W}")
        self.m_vi_memory_list = MRdataCollector.base_task_Collector(job_id,"m","org.apache.hadoop.mapreduce.TaskCounter","VIRTUAL_MEMORY_BYTES")

        Color.pl("{+}    {C}获取 reduce 任务 read 数据{W}")
        self.r_read_list = MRdataCollector.base_task_Collector(job_id,"r","org.apache.hadoop.mapreduce.FileSystemCounter","FILE_BYTES_READ")
        Color.pl("{+}    {C}获取 reduce 任务 cpu 时间  数据{W}")
        self.r_cpu_list = MRdataCollector.base_task_Collector(job_id,"r","org.apache.hadoop.mapreduce.TaskCounter","CPU_MILLISECONDS")
        Color.pl("{+}    {C}获取 reduce 任务 GC 时间 数据{W}")
        self.r_gc_list = MRdataCollector.base_task_Collector(job_id,"r","org.apache.hadoop.mapreduce.TaskCounter","GC_TIME_MILLIS")
        Color.pl("{+}    {C}获取 reduce 任务 运行总时间 数据{W}")
        self.r_time_list = MRdataCollector.info_task_Collector(job_id,"r","elapsedTime")
        Color.pl("{+}    {C}获取 reduce 任务 output record 数据{W}")
        self.r_out_r_list = MRdataCollector.base_task_Collector(job_id,"r","org.apache.hadoop.mapreduce.TaskCounter","REDUCE_OUTPUT_RECORDS")
        Color.pl("{+}    {C}获取 reduce 任务 spill record 数据{W}")
        self.r_spilled_r_list = MRdataCollector.base_task_Collector(job_id,"r","org.apache.hadoop.mapreduce.TaskCounter","SPILLED_RECORDS")
        Color.pl("{+}    {C}获取 reduce 任务 使用物理内存 数据{W}")
        self.r_ph_memory_list = MRdataCollector.base_task_Collector(job_id,"r","org.apache.hadoop.mapreduce.TaskCounter","PHYSICAL_MEMORY_BYTES")
        Color.pl("{+}    {C}获取 reduce 任务 使用虚拟内存 数据{W}")
        self.r_vi_memory_list = MRdataCollector.base_task_Collector(job_id,"r","org.apache.hadoop.mapreduce.TaskCounter","VIRTUAL_MEMORY_BYTES")
        #self.conf_m_memeory = MRdataCollector.conf_job_Collector(job_id,"mapreduce.map.memory.mb") 
        self.conf_m_memeory = 0
        self.conf_yarn_mix_memory = 1024
        self.resouce_sec = 3  * 1024 * 86400
    def check_required_memory(self):
        if self.conf_m_memeory <= self.conf_yarn_mix_memory:
            return self.conf_yarn_mix_memory
        else:
            return self.conf_m_memeory

    def check_severity(self,val,severity):
        """
        一个通用方法用来比较一个值在阈值列表中的区间位置，并给出相应等级
        """
        severity_levels =  Configuration.severity_levels
        if val <= severity[0] and val >= severity[1]:
            return severity_levels[0]
        if val <= severity[1] and val >= severity[2]:
            return severity_levels[1]
        if val <= severity[2] and val >= severity[3]:
            return severity_levels[2]
        if val <= severity[3] and val >= severity[4]:
            return severity_levels[3]

    def byte_MB(self,byte):
        """
        讲byte转化成MB
        """
        return float(byte) / 1024.00 /1024.00

    def check_group_avg(self,val_list):
        """
        一个非常垃圾的分组算法，需要改进
        """
        val_list.sort()
        mid = len(val_list) / 2
        group_a = val_list[:mid]
        group_b = val_list[mid:]
        avg_a  = sum(group_a) / len(group_a)
        avg_b  = sum(group_b) / len(group_b)
        result = float(avg_a) / float(avg_b)
        return [len(group_a),len(group_b),avg_a,avg_b,result]

    def get_median(self,data):
        """
        通用办法用来获取list表中的中位数
        """
        data = sorted(data)
        size = len(data)
        if size % 2 == 0:   # 判断列表长度为偶数
            median = (data[size//2]+data[size//2-1])/2
            data[0] = median
        if size % 2 == 1:   # 判断列表长度为奇数
            median = data[(size-1)//2]
            data[0] = median
        return data[0]

    def mapperSkewHeuristic(self):
        
        #计算数据倾斜
        val_list_1 = self.m_read_list
        result_list_1 = self.check_group_avg(val_list_1)

        val_list_2 = self.m_time_list 
        result_list_2 = self.check_group_avg(val_list_2)

        mapperSkew_severity  = Configuration.mapperSkew_severity
        level_1 = self.check_severity(result_list_1[4],mapperSkew_severity)
        level_2 = self.check_severity(result_list_2[4],mapperSkew_severity)

        result_list = [
                        {"name":"Mapper Data Skew检测结果","value":level_1+level_2},
                        {"name":"Data skew (Group A)","value":(result_list_1[0],result_list_1[2])},
                        {"name":"Data skew (Group A)","value":(result_list_1[1],result_list_1[3])},
                        {"name":"Data time (Group A)","value":(result_list_2[0],result_list_2[2])},
                        {"name":"Data time (Group B)","value":(result_list_2[1],result_list_2[3])},
                                      ]
        return result_list

    def mapperGCHeuristic(self):
        val_list_1 = self.m_cpu_list
        val_list_2 = self.m_gc_list
        val_list_3 = self.m_time_list
        avg_CPU  = sum(val_list_1) / len(val_list_1) 
        avg_GC  = sum(val_list_2) / len(val_list_2)
        avg_time = sum(val_list_3) / len(val_list_3)
        ratio = 1.00 - (float(avg_GC) / float(avg_CPU))
        mapperGC_severity = Configuration.mapperGC_severity
        level = self.check_severity(ratio,mapperGC_severity)
        result_list = [
                        {"name":"Mapper GC检测结果","value":level},
                        {"name":"Avg task CPU time","value":avg_CPU},
                        {"name":"Avg task GC time","value":avg_GC},
                        {"name":"Avg task runtime","value":avg_time},
                        {"name":"Task GC/CPU ratio","value":(1 - ratio)},
                                      ]
        return result_list
    def mapperTimeHeuristic(self):
        val_list_1 = self.m_read_list
        val_list_2 = self.m_time_list 
        avg_input  =  self.byte_MB(sum(val_list_1) / len(val_list_1))
        avg_time = float(sum(val_list_2) / len(val_list_2)) / 1000.00
        max_time = float(max(val_list_2)) / 1000.00
        min_time = float(min(val_list_2)) / 1000.00
        time_val =  min_time / max_time
        mapperTime_severity  = Configuration.mapperTime_severity
        level = self.check_severity(time_val,mapperTime_severity)
        result_list = [
                        {"name":"Mapper Time检测结果","value":level},
                        {"name":"Average task input size","value":avg_input},
                        {"name":"Average task runtime","value":avg_time},
                        {"name":"Max task runtime","value":max_time},
                        {"name":"Min task runtime","value":min_time}
                                      ]
        return result_list

    def mapperSpeedHeuristic(self):
        input_list =  self.m_read_list
        time_list = self.m_time_list 
        mid_input =  self.byte_MB(self.get_median(input_list))
        mid_time = self.get_median(time_list)
        mid_speed = float(mid_input / mid_time)
        total_input =  self.byte_MB(sum(input_list)) 
        level = "良好"
        result_list = [
                        {"name":"Reducer Speed检测结果","value":level},
                        {"name":"Median task input size","value":mid_input},
                        {"name":"Median task runtime","value":mid_time},
                        {"name":"Median task speed","value":mid_speed},
                        {"name":"Total input size","value":total_input},
                                      ]
        return result_list

    def mapperSpillHeuristic(self):
        out_r_list = self.m_out_r_list
        spilled_r_list = self.m_spilled_r_list
        avg_out_r  = float(sum(out_r_list) / len(out_r_list))
        avg_spilled_r  = float(sum(spilled_r_list) / len(spilled_r_list))
        ratio = avg_spilled_r / avg_out_r
        mapperSpill_severity = Configuration.mapperSpill_severity
    
        level = self.check_severity(ratio,mapperSpill_severity)
        result_list = [
                       {"name":"Mapper Spill检测结果","value":level},
                       {"name":"Avg output records","value":avg_out_r},
                       {"name":"Avg spilled records","value":avg_spilled_r},
                       {"name":"Ratio spilled/output","value":avg_spilled_r}
                      ]
        return result_list

    def mapperMemoryHeuristic(self):
       ph_memory_list = self.m_ph_memory_list 
       vi_memory_list = self.m_vi_memory_list
       time_list =  self.m_time_list
       
       avg_ph_memory =  self.byte_MB(sum(ph_memory_list) / len(ph_memory_list))
       avg_vi_memory =  self.byte_MB(sum(ph_memory_list) / len(ph_memory_list))
       avg_time = sum(time_list) / len(time_list)

       max_ph_memory = max(ph_memory_list)
       min_py_memory = min(ph_memory_list)
       required_memory = self.check_required_memory()
       waste_reouse = (required_memory - avg_ph_memory) * (avg_time / 1000)
       level = float(waste_reouse) / float(self.resouce_sec)
       result_list = [
                       {"name":"Mapper Memory检测结果","value":level},
                       {"name":"Avg Physical Memory","value":avg_ph_memory},
                       {"name":"Avg Virtual Memory","value":avg_vi_memory},
                       {"name":"Min Physical Memory","value":max_ph_memory},
                       {"name":"Mix Physical Memory","value":min_py_memory},
                       {"name":"Container Memory","value":required_memory},
                       {"name":"waste resource","value":waste_reouse},
                       {"name":"waste Total resource","value":self.resouce_sec}
                      ]
       return result_list

    def reducerSkewHeuristic(self):
        #计算数据倾斜
        val_list_1 = self.r_read_list
        result_list_1 = self.check_group_avg(val_list_1)

        val_list_2 = self.r_time_list
        result_list_2 = self.check_group_avg(val_list_2)

        mapperSkew_severity  = Configuration.mapperSkew_severity
        level_1 = self.check_severity(result_list_1[4],mapperSkew_severity)
        level_2 = self.check_severity(result_list_2[4],mapperSkew_severity)


        #计算时间倾斜
        result_list = [
                        {"name":"Reducer Data Skew检测结果","value":level_1+level_2},
                        {"name":"Data skew (Group A)","value":(result_list_1[0],result_list_1[2])},
                        {"name":"Data skew (Group A)","value":(result_list_1[1],result_list_1[3])},
                        {"name":"Data time (Group A)","value":(result_list_2[0],result_list_2[2])},
                        {"name":"Data time (Group B)","value":(result_list_2[1],result_list_2[3])}
                                      ]
        return result_list
    
    def reducerGCHeuristic(self):
        val_list_1 = self.r_cpu_list
        val_list_2 = self.r_gc_list
        val_list_3 = self.r_time_list
        avg_CPU  = sum(val_list_1) / len(val_list_1)
        avg_GC  = sum(val_list_2) / len(val_list_2)
        avg_time = sum(val_list_3) / len(val_list_3)
        ratio = 1.00 - (float(avg_GC) / float(avg_CPU))
        mapperGC_severity = Configuration.mapperGC_severity
        level = self.check_severity(ratio,mapperGC_severity)
        result_list = [
                        {"name":"Reducer GC检测结果","value":level},
                        {"name":"Avg task CPU time","value":avg_CPU},
                        {"name":"Avg task GC time","value":avg_GC},
                        {"name":"Avg task runtime","value":avg_time},
                        {"name":"Task GC/CPU ratio","value":(1 - ratio)}
                                      ]
        return result_list 
    def reducerTimeHeuristic(self):
        val_list_1 = self.r_read_list
        val_list_2 = self.r_time_list
        avg_input  =  self.byte_MB(sum(val_list_1) / len(val_list_1))
        avg_time = float(sum(val_list_2) / len(val_list_2)) / 1000.00
        max_time = float(max(val_list_2)) / 1000.00
        min_time = float(min(val_list_2)) / 1000.00
        time_val =  min_time / max_time
        mapperTime_severity  = Configuration.mapperTime_severity
        level = self.check_severity(time_val,mapperTime_severity)
        result_list = [
                        {"name":"Reducer Time检测结果","value":level},
                        {"name":"Average task input size","value":avg_input},
                        {"name":"Average task runtime","value":avg_time},
                        {"name":"Max task runtime","value":max_time},
                        {"name":"Min task runtime","value":min_time}
                                      ]
        return result_list

    def reducerSpeedHeuristic(self):
        input_list =  self.r_read_list
        time_list = self.r_time_list
        mid_input =  self.byte_MB(self.get_median(input_list))
        mid_time = self.get_median(time_list)
        mid_speed = float(mid_input / mid_time)
        total_input =  self.byte_MB(sum(input_list))
        level = "良好"
        result_list = [ 
                        {"name":"Reducer Speed检测结果","value":level},
                        {"name":"Median task input size","value":mid_input},
                        {"name":"Median task runtime","value":mid_time},
                        {"name":"Median task speed","value":mid_speed},
                        {"name":"Total input size","value":total_input}
                                      ]
        return result_list
    def reducerSpillHeuristic(self):
        out_r_list = self.r_out_r_list
        spilled_r_list = self.r_spilled_r_list
        avg_out_r  = float(sum(out_r_list) / len(out_r_list))
        avg_spilled_r  = float(sum(spilled_r_list) / len(spilled_r_list))
        ratio = avg_spilled_r / avg_out_r
        mapperSpill_severity = Configuration.mapperSpill_severity
        level = self.check_severity(ratio,mapperSpill_severity)
        if Configuration.job_check_detail:
            Color.pl("{+}    {C}Avg output records      {B} %s {W}" % avg_out_r)
            Color.pl("{+}    {C}Avg spilled records     {B} %s {W}" % avg_spilled_r)
            Color.pl("{+}    {C}Ratio spilled/output    {B} %s {W}" % ratio)
        result_list = [
                        {"name":"Reducer Spill检测结果","value":level},
                        {"name":"Avg output records","value":avg_out_r},
                        {"name":"Avg spilled records","value":avg_spilled_r},
                        {"name":"Ratio spilled/output","value":ratio}
                                      ]
        return result_list

    def reducerMemoryHeuristic(self):
       ph_memory_list = self.r_ph_memory_list
       vi_memory_list = self.r_vi_memory_list
       time_list =  self.m_time_list

       avg_ph_memory =  self.byte_MB(sum(ph_memory_list) / len(ph_memory_list))
       avg_vi_memory =  self.byte_MB(sum(ph_memory_list) / len(ph_memory_list))
       avg_time = sum(time_list) / len(time_list)

       max_ph_memory = max(ph_memory_list)
       min_py_memory = min(ph_memory_list)
       required_memory = self.check_required_memory()
       waste_reouse = (required_memory - avg_ph_memory) * (avg_time / 1000)
       level = float(waste_reouse) / float(self.resouce_sec)
       result_list = [
                       {"name":"Reduceer Memory检测结果","value":level},
                       {"name":"Avg Physical Memory","value":avg_ph_memory},
                       {"name":"Avg Virtual Memory","value":avg_vi_memory},
                       {"name":"Min Physical Memory","value":max_ph_memory},
                       {"name":"Mix Physical Memory","value":min_py_memory},
                       {"name":"Container Memory","value":required_memory},
                       {"name":"waste resource","value":waste_reouse},
                       {"name":"waste Total resource","value":self.resouce_sec}
                      ]
       return result_list

    def run_all_heuristic(self):
        data_list = [self.reducerMemoryHeuristic(),
                     self.mapperSkewHeuristic(),
                     self.mapperGCHeuristic(),
                     self.mapperTimeHeuristic(),
                     self.mapperSpeedHeuristic(),
                     self.mapperSpillHeuristic(),
                     self.mapperMemoryHeuristic(),
                     self.reducerSkewHeuristic(),
                     self.reducerGCHeuristic(),
                     self.reducerTimeHeuristic(),
                     self.reducerSpeedHeuristic(),
                     self.reducerSpillHeuristic(),
                     self.reducerMemoryHeuristic(),
                    ]
        return data_list
