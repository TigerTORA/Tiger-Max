#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .util.color import Color

class Configuration(object):
    ''' Stores configuration variables and functions for Wifite. '''
    version = '2.2.5'

    initialized = False # Flag indicating config has been initialized
    temp_dir = None     # Temporary directory
    interface = None
    verbose = 0
    run_as_root = False
    hostnm = "echo -n $(hostname)###&&"

    #historyserver
    history_host = "luohu-cdh-pro-01.cs1hypers.com"
    history_port = "19888"
    

    #job任务性能检测
    check_items = [
                    #mapperSkewHeuristic,
                    #mapperGCHeuristic,
                    #mapperTimeHeuristic,
                    #mapperSpeedHeuristic,
                    #mapperSpillHeuristic,
                    #mapperMemoryHeuristic,
                    #reducerSkewHeuristic,
                    #reducerGCHeuristic,
                    #reducerTimeHeuristic,
                    #reducerSpeedHeuristic,
                    #reducerSpillHeuristic,
                    #reducerMemoryHeuristic,
                    ]
    severity_levels = ["{G}良好{W}","{W}一般{W}","{O}警告{W}","{R}严重{W}","{R}超级严重{W}"]
    job_check_detail = True
    mapperSkew_severity = [1.0,0.8,0.7,0.6,0.5] 
    mapperGC_severity = [1.0,0.9,0.8,0.7,0.6]
    mapperTime_severity = [1.0,0.8,0.6,0.4,0.2]
    mapperSpill_severity = [1.0,0.8,0.6,0.4,0.2]
    @classmethod
    def initialize(cls, load_interface=True):
        '''
            Sets up default initial configuration values.
            Also sets config values based on command-line arguments.
        '''
        # TODO: categorize configuration into separate classes (under config/*.py)
        # E.g. Configuration.wps.enabled, Configuration.wps.timeout, etc

        # Only initialize this class once
        if cls.initialized:
            return
        cls.initialized = True

        cls.verbose = 8 # Verbosity of output. Higher number means more debug info about running processes.
