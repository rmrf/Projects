#!/bin/bash

PWD=$(pwd)
ROOT=$PWD/..
export PYTHONPATH=$ROOT:/usr/lib/python2.6:/usr/lib/python2.6/site-packages:/usr/lib/python2.6/vendor-packages:.

export DJANGO_SETTINGS_MODULE=SolO.settings
export PATH=$PATH:$ROOT/django/bin

ipaddr=`/usr/sbin/ifconfig -a |grep -w inet |grep -v 127.0.0.1|awk '{print $2}'|head -1`
port="8080"

echo "#########################################"
echo "Please open http://$ipaddr:$port"
echo "#########################################"

django-admin.py runserver  0.0.0.0:8080
