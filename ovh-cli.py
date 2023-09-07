#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################################################
#############################################################################
#############################################################################
# pip3 install ovh --user
# pip3 install tabulate --user
#
# Token          https://api.ovh.com/createToken/?GET=/*&PUT=/*&POST=/*&DELETE=/*
# Documentation: https://eu.api.ovh.com/console/#/dedicated/server
#############################################################################
import ovh
import argparse
from tabulate import tabulate
#Built-in
import json
import sys, os.path

import urllib.parse
#############################################################################
def ovh_credentials():
  #credentials = client.get('/me/api/credential', status='validated')
  credentials = client.get('/me/api/credential')
  table = []
  for credential_id in credentials:
    #credential_method = '/me/api/credential/'+str(credential_id)
    #credential = client.get(credential_method)
    #application = client.get(credential_method+'/application')
    credential = client.get('/me/api/credential/%s' % credential_id)
    if not (args.noverbose) or (args.debug):
      print(credential_id)
    application = client.get('/me/api/credential/%s/application' % credential_id)
    table.append([
      credential_id,
      '[%s] %s' % (application['status'], application['name']),
      application['description'],
      credential['creation'],
      credential['expiration'],
      credential['lastUse'],
    ])
  if (args.json):
    print(json.dumps(table, indent=2))
  else:
    headers=['ID', 'App Name', 'Description', 'Token Creation', 'Token Expiration', 'Token Last Use']
    print(tabulate(table, headers=headers))
#############################################################################
def ovh_servers():
  servers = client.get('/dedicated/server/')
  table = []
  for server in servers:
    details = client.get('/dedicated/server/%s' % server)
    if not (args.noverbose) or (args.debug):
      print(details['name'])
    if (args.serviceinfos):
      service_details = client.get('/dedicated/server/%s/serviceInfos' % server)
      serviceId=service_details['serviceId']
      services = client.get('/services/%s' % serviceId)
      if services['billing']['engagement'] is None:
        service_engagement=''
      else:
        service_engagement= services['billing']['engagement']['endRule']['strategy']
      table.append([
        details['reverse'],
        details['name'],
        details['commercialRange'],
        details['state'],
        details['monitoring'],
        service_details['status'],
        service_details['serviceId'],
        #domain
        #contactTech
        #contactBilling
        #contactAdmin
        service_details['renew']['period'],
        #renew_manualPayment
        #renew_deleteAtExpiration
        service_details['renew']['automatic'],
        service_details['renew']['forced'],
        service_details['creation'],
        service_details['expiration'],
        service_details['engagedUpTo'],
        service_engagement,
        #canDeleteAtExpiration
      ])
    else:
      table.append([
        details['reverse'],
        details['name'],
        details['commercialRange'],
        details['ip'],
        details['datacenter'],
        details['rack'],
        details['serverId'],
        details['state'],
        details['linkSpeed'],
        details['monitoring'],
        details['noIntervention'],
      ])
  if (args.serviceinfos):
    print(tabulate(sorted(table), headers=['reverse', 'name', 'commercialRange', 'ip', 'datacenter', 'rack', 'serverId', 'state', 'linkSpeed', 'monitoring', 'noIntervention'], tablefmt="github"))
  else:
    print(tabulate(sorted(table), headers=['reverse', 'name', 'commercialRange', 'state', 'monitoring', 'status',  'serviceId', 'renew_period', 'renew_automatic','renew_forced', 'creation', 'expiration', 'engagedUpTo', 'endRule_Strategy'], tablefmt="github"))
#############################################################################
#############################################################################
# To do:
# /dedicated/server/{serviceName}/networkInterfaceController
# /dedicated/server/{serviceName}/specifications/hardware
# /dedicated/server/{serviceName}/virtualMac
# /dedicated/server/{serviceName}/vrack
# /ip/{ip}/reverse
# /ip/{ip}/reverse/{ipReverse}
# /dedicated/server/{serviceName}/ips
# /dedicated/server/{serviceName}/plannedIntervention
#############################################################################
#############################################################################
parser = argparse.ArgumentParser(description="https://github.com/osgpcq/ovh-cli-py",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--client",               default="exo",       help="Config file selection")
parser.add_argument("--credentials",          action="store_true", help="List credentials")
parser.add_argument("--debug",                action="store_true", help="Debug information")
parser.add_argument("--ips",                  action="store_true", help="List ips")
parser.add_argument("--reverse",              action="store_true", help="List ips reverse")
parser.add_argument("--json",                 action="store_true", help="JSON output")
parser.add_argument("--servers",              action="store_true", help="List servers")
parser.add_argument("--serviceinfos",         action="store_true", help="List serviceinfos")
parser.add_argument("--noverbose",            action="store_true", default=False, help="Verbose")
args = parser.parse_args()

config_file='./config-'+args.client+'.conf'
if os.path.isfile(config_file):
  client = ovh.Client(config_file=config_file)
else:
  sys.exit('Configuration file not found!')
# Print nice welcome message
print('Welcome',client.get('/me')['firstname']+",")
#
if (args.credentials):
  ovh_credentials()
if (args.servers):
  ovh_servers()
if (args.ips):
  ovh_ips()
#############################################################################
#############################################################################
#############################################################################
