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
    def fails_dependency_check(cls):
        from ..util.color import Color
        from ..util.process import Process

        if Process.exists(cls.dependency_name):
            return False

        if cls.dependency_required:
            Color.p('{!} {O}Error: Required app {R}%s{O} was not found' % cls.dependency_name)
            Color.pl('. {W}install @ {C}%s{W}' % cls.dependency_url)
            return True

        else:
            Color.p('{!} {O}Warning: Recommended app {R}%s{O} was not found' % cls.dependency_name)
            Color.pl('. {W}install @ {C}%s{W}' % cls.dependency_url)
            return False

    @classmethod
    def fails_dependency_check_hhdp(cls):
        from ..util.color import Color
        from ..tools.hhdp import hhdp

        #unexists_list = Process.exists_hhdp(cls.dependency_name)
	for key,name in cls.dependency_namei.keys():
	    command = ['hhdp', "-c", "which "+key]
	    ress = hhdp(command)
	    for res in ress:
		hostname = res[0]
		sdout = res[1]
		sderr = res[2]
		if sderr:
			Color.pl('{!} {R}Error: {W}Required app {R}%s{O} was not found in host {R}%s{W}' % (key,hostname))
		else:
			Color.pl('{+} {G}Info: {W}Required app {R}%s{O} was  found in host {R}%s{W}' % (key,hostname))
        
	#if cls.dependency_required:
        #    for host in unexists_list:
        #        Color.pl('{!} {O}Error: Required app {R}%s{O} was not found in host {R}%s' % (cls.dependency_name,host))
