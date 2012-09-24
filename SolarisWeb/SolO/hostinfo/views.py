import os
import sys
from struct import pack
from socket import inet_ntoa
from django.http import HttpResponse
from django.shortcuts import render_to_response




def calcDottedNetmask(mask):
    bits = 0xffffffff ^ (1 << 32 - mask) - 1
    return inet_ntoa(pack('>I', bits))


def _hostname():
    """ Show hostname """
    hostname_cmd = "hostname"
    return  os.popen(hostname_cmd).read().rstrip()


def _ipaddr():
    """ Show IP Address  """
    ipaddr_cmd = "ipadm show-addr"  
    network_array = []
    all_lines = os.popen(ipaddr_cmd)
    for line in all_lines:
        if "ok" in line and ":" not in line:
            t = line.split()
            nic = t[0].split('/')[0]
            ip = t[3].split('/')[0]
            netmask = t[3].split('/')[1]
            netmask = calcDottedNetmask(int(netmask))
            network_array.append({"Network Interface": nic,"IP Address":ip, 
                    "Netmask":netmask})
    return network_array


def _gateway():
    """ Show IP Address  """
    gateway_cmd = "netstat -rn |grep default | awk '{print $2}'"
    return  os.popen(gateway_cmd).read().rstrip()

def index(request):
    """ Front Page, show All information"""
    if request.method == "GET":
        gateway = _gateway()
        hostname = _hostname()
        ipaddr_array  = _ipaddr()
        return render_to_response("hostinfo/index.html", {
                                'ipaddr_array': ipaddr_array,
                                'hostname': hostname,
                                'gateway': gateway,
                                })


def main():
    print _hostname()
    print _gateway()
    print _ipaddr()

if __name__ == '__main__':
    main()
