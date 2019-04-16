#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Dependency(object):
    required_attr_names = ['dependency_name', 'dependency_url', 'dependency_required']
    
    def __init_subclass__(cls):
        for attr_name in cls.required_attr_names:
            if not attr_name in cls.__dict__:
                raise NotImplementedError(
                    'Attribute "{}" has not been overridden in class "{}"' \
                    .format(attr_name, cls.__name__)
                )
    @classmethod
    def run_dependency_check(cls):
        from ..util.color import Color
        
        from .sysbench import Sysbench

        
        apps_hhdp = [
                ]

        apps = [
                ]
        #在所有机器上检查apps_hhdp上的依赖
        missing_required_all  = any([app_hhdp.fails_dependency_check_hhdp() for app_hhdp in apps_hhdp])

        #在本机上检查apps中的依赖
        missing_required = any([app.fails_dependency_check() for app in apps])

        if missing_required:
            Color.pl('{!} {O}At least 1 Required app is missing. Wifite needs Required apps to run{W}')
            import sys
            sys.exit(-1)

    @classmethod
    def fails_dependency_check_hhdp(self,dict):
	from ..util.color import Color
	from ..tools.hhdp import hhdp
        for key,name in dict.items():
            command = ['none', "-c", "which "+key]
            ress = hhdp(command)
            for res in ress:
                ip = res[0]
                stdout = res[1]
                stderr = res[2]
                if stderr:
                        Color.pl('{!} {R}Error: {W}Required app {R}%s{W} was not found in host {R}%s,{W}refer to:{R}%s{W}' % (key,ip,name))
                else:
                        Color.pl('{+} {G}Info: {W}Required app {G}%s{W} was found in host {G}%s{W}' % (key,ip))
    @classmethod
    def fails_dependency_check(self,dict):
        from ..util.color import Color
        from ..util.process import Process
	for key,name in dict.items():
	    if Process.exists(key):
	        Color.pl('{+} {G}Info: {W}Required app {G}%s{W} was found{W}' % (key))
	    else:
		Color.pl('{!} {R}Error: {W}Required app {R}%s{W} was not found{R}%s,{W}refer to:{R}%s{W}' % (key,name))

