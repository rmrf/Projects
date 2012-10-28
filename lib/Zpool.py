#!/usr/bin/python

# This script used for 
#

import os
import re
import sys
import Disk
import logging

logger = logging.getLogger("SolO.Zpool")

PFEXEC =  "/usr/bin/pfexec"
ZPOOL_LIST = "/usr/sbin/zpool list -H" 
ZPOOL_STATUS = "/usr/sbin/zpool status" 

class Zpool:

    def __init__(self):
        self.zpool_list = self.get_zpool_list()

    def get_zpool_list(self):
        zpool_list = {}
        CMD = PFEXEC + " " + ZPOOL_LIST

        try:
            # Example 
            # NAME    SIZE  ALLOC   FREE  CAP  DEDUP  HEALTH  ALTROOT
            # data   1.98G    85K  1.98G   0%  1.00x  ONLINE  -
            str_zpool_all = ''.join(os.popen(CMD).readlines())
        except e:
            logger.error("Failed to get zpool with command %s,%s" % (CMD,str(e))) 


        for line in str_zpool_all.split('\n'):
            if line:
                (pname, psize, palloc, pfree, pcap, pdedup, phealth, paltroot) = \
                    line.split()
                zpool_list[pname] = {'pname':pname,'psize':psize,'pfree':pfree\
                    ,'pcap':pcap,'pdedup':pdedup,'phealth':phealth}

        return zpool_list
            

    def _is_system_zpool(self,pname=""):
        """ Tell whether this pool is used for boot OS """
        

if __name__ == '__main__':
    P = Zpool()
    print P.zpool_list
