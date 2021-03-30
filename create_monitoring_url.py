#!/usr/bin/python3
from pyzabbix import ZabbixAPI
import json
import sys
import csv

zapi = ZabbixAPI(sys.argv[1])
zapi.login(user=sys.argv[2], password=sys.argv[3])

groupname = 'Monitoramento - URL'
hostname = 'Monitoramento URL'
hostid = ''
hostgroupid = ''
applicationid = ''
httptestid = ''
triggerid = ''
webscenarioname = ''
hostgroup = zapi.hostgroup.get(output='extend',filter={'name':groupname})
try:
    hostgroupid = hostgroup[0]['groupid']
    print('hostgroupid : '+hostgroupid)
except Exception as error:
    hostgroup = zapi.hostgroup.create(
    name= groupname
    )
    hostgroupid = hostgroup['groupids'][0]
    print('hostgroupid : '+hostgroupid)

host = zapi.host.get(output='extend',filter={'host':hostname})
try:
    hostid = host[0]['hostid']
    print('hostid : '+hostid)
except Exception as error:
    host = zapi.host.create(
        host= hostname,
        status= 0,
        interfaces=[{
            "type": 1,
            "main": "1",
            "useip": 1,
            "ip": "127.0.0.1",
            "dns": "",
            "port": 10050
        }],
        groups=[{
            "groupid": hostgroupid
        }]
    )
    hostid = host['hostids'][0]
    print('hostid : '+hostid)

f = open('urls.txt')
for web_names in f:
    web_name = web_names.rstrip()
    name = web_name.split("://")[1]
    application = zapi.application.get(output='extend',hostids=hostid, filter={'name':name})
    try:
        applicationid = application[0]['applicationid']
        print('applicationid : '+applicationid)
    except Exception as error:
        application = zapi.application.create(
            hostid= hostid,
            name= name
        )
        applicationid = application['applicationids'][0]
        print('applicationid : '+applicationid)

    webscenarioname = 'Check '+name
    if len(webscenarioname) > 60:
        webscenarioname = webscenarioname[0:60]
    webscenario = zapi.httptest.get(output='extend', hostids=hostid, filter={'name':webscenarioname})
    try:
        httptestid = webscenario[0]['httptestid']
        print('httptestid : '+httptestid)
    except Exception as error:
        webscenario = zapi.httptest.create(
            hostid= hostid,
            name= webscenarioname,
            applicationid= applicationid,
            steps=[
                {
                    'name': 'Web '+webscenarioname,
                    'url': str(web_name),
                    'status_codes': '200',
                    'no': '1'

                }
            ]
        )
        httptestid = webscenario['httptestids'][0]
        print('httptestid : '+httptestid)

    triggername = 'Web Check '+name+' falhou'
    trigger = zapi.trigger.get(output='extend',hostids=hostid, filter={'description': triggername})
    try:
        triggerid = trigger[0]['triggerid']
        print('triggerid : '+triggerid)
    except Exception as error:
        trigger = zapi.trigger.create(
            hostid= hostid,
            description= triggername,
            expression='{'+hostname+':web.test.fail['+webscenarioname+'].sum(#3)}>=3',
            priority = 5
        )
        triggerid = trigger['triggerids'][0]
        print('triggerid : '+triggerid) 

print('Monitoramento finalizado')   
