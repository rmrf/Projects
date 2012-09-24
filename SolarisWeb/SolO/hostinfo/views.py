import os
import sys
from django.shortcuts import render_to_response
from django.http import HttpResponse


# Solaris System command for get detail
cmd_all_smf = "/usr/bin/svcs -a"
cmd_smf_children = "/usr/bin/svcs -d"
cmd_smf_parent = "/usr/bin/svcs -D"
cmd_smf_issue = "/usr/bin/svcs -xv"
cmd_smf_log = "/usr/bin/svcs -l"
banner = "STATE          STIME    FMRI"



def show_all(dict_smf_status,dict_smf_time,dict_status_smf):
    """ List all system services """
# The number of All status
    all_lines = os.popen(cmd_all_smf)
    stat_num = {}
    for line in all_lines:
        if banner in line:
            continue
        (smf_status, smf_time, smf_name) = line.split()
        dict_smf_status[smf_name] = smf_status
        dict_smf_time[smf_name] = smf_time

        if smf_status in dict_status_smf.keys():
            dict_status_smf[smf_status].append(smf_name)
        else:
            dict_status_smf[smf_status] = [smf_name]

    for status in dict_status_smf:
        stat_num[status] = len(dict_status_smf[status])

    return(stat_num)



def show_status(smf_list=[]):
    """ Show status """
    if smf_list is not []:
        for smf in smf_list:
            print smf, "\t", dict_smf_status[smf]


def show_relations(smf, relation):
    """ Show SMF service's dependency """
    relationship = []
    if relation == 'parent':
        all_lines = os.popen(cmd_smf_parent + " " + smf)
    elif relation == 'children':
        all_lines = os.popen(cmd_smf_children + " " + smf)
    else:
        print "it's not Parent or Children, what do you want "
        return relationship

    for line in all_lines:
        if banner in line:
            continue
        (smf_status, smf_time, smf_name) = line.split()
        relationship.append(smf_name)

    # return a list
    return relationship


def show(request):
    """ Show children or parent service """
    if request.method == "GET":
        smf_name =  request.GET.get("smf_name","").strip("\"")
        smf_relation =  request.GET.get("relation","").strip("\"")

        if smf_name is not "":
            # Dictonary of smf service and status, key is service name, value is status
            dict_smf_status = {}
            dict_smf_time = {}
            dict_status_smf = {}
            show_all(dict_smf_status=dict_smf_status, \
                dict_smf_time=dict_smf_time, dict_status_smf=dict_status_smf)

            smf_dep = show_relations(smf=smf_name, relation=smf_relation)
            return render_to_response("svcs/show.html", {
                                    'smf_name': smf_name,
                                    'smf_relation': smf_relation,
                                    'dict_smf_status':dict_smf_status,
                                    'smf_dep': smf_dep
                                    })

def index(request):
    """ Front Page, show all services status """
    if request.method == "GET":

        #print PROJECT_PATH ,"00000000000000"
        # Dictonary of smf service and status, key is service name, value is status
        dict_smf_status = {}
        dict_smf_time = {}
        dict_status_smf = {}
        stat_num =  show_all(dict_smf_status=dict_smf_status, \
            dict_smf_time=dict_smf_time, dict_status_smf=dict_status_smf)

        return render_to_response("svcs/index.html", {
                                'dict_status_smf': dict_status_smf,
                                'stat_num': stat_num
                                })


def main():
    show_all()
    for smf in dict_status_smf['maintenance']:
        smf_list = show_relations(smf=smf, relation='children')
        print "the Dependency of " + smf + " are: "
        show_status(smf_list=smf_list)
        print


#if __name__ == '__main__':
    #main()
