#!/usr/bin/python

# This script used for 
#

import os
import re
import sys
import logging

logger = logging.getLogger("SolO.Disk")

PFEXEC =  "/usr/bin/pfexec"
DISK_FORMAT= "/usr/sbin/format < /dev/null" 
DISK_ZPOOL = "/usr/sbin/zpool status" 

class Disk:

    def __init__(self):
        self.all_disk = self.get_all_disk()
        self.free_disk = self.get_free_disk()
        self.zpool_used_disk = self.get_zpool_used_disk()
   
    """ Solaris Disk related functions here"""    
    def _get_disk(self, scope=""):
        """used for get all disk , return a array contain all disk names"""
        # find disk from format command or from zpool 
        if scope == "zpool":
            CMD = PFEXEC + " " + DISK_ZPOOL
        else:
            CMD = PFEXEC + " " + DISK_FORMAT
        
        disk_all = []
            
        # filer the cXtXdX disk using format command
        pattern_disk = re.compile('c\d+t\d+d\d+')
        try:
            str_disk_all = ''.join(os.popen(CMD).readlines())
            disk_all = pattern_disk.findall(str_disk_all)
        except e:
            logger.error("Failed to get disk with command %s,%s" % (CMD,str(e))) 

        return disk_all


    def get_zpool_used_disk(self):
        """used for get zpool disk , return a array contain all disk names"""
        return self._get_disk("zpool")

    def get_all_disk(self):
        """used for get all disk , return a array contain all disk names"""
        return self._get_disk("system")

    def get_free_disk(self):
        """used for get zpool all disk , return a array contain all disk names"""
        zdisk = self.get_zpool_used_disk()
        alldisk = self.get_all_disk()
        free_disk = [ i for i in alldisk if i not in zdisk]
        return free_disk

if __name__ == '__main__':
    D = Disk()
    print "Free disks are:", D.free_disk

