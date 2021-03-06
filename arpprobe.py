#!/usr/bin/env python3
#
##
## This was a small PoC I wrote in 2016 to test the usefulness of using Amazon Dash buttons as "smart" buttons to trigger other events besides just ordering stuff through Amazon. It does work, but given the battery wears out fairly quickly, it's not good for actions you expect o happen frequently.
## I used it for controlling the Sonos devices in my home, and the Nest Devices, but I now have a bunch more smart devices, so am now looking to generalise the "trigger" element so that it can work with any API.
## This script needs to run perpetually on a server on your LAN such that it can see the Amazon Dash button WLAN ARP packets.
## This has been adapted from the script available here : https://github.com/calebmadrigal/network-hacking-scripts/blob/master/scapy-arpprobe.py
##

import argparse
from scapy.all import *
import time
import socoabs, nestabs
import requests
import json

def findButtonInConfig(mac):
    for button in config['buttons']:
        if button['mac'] == mac:
            return button
            
    if mac not in macs:
        url = "http://macvendors.co/api/" + mac
        reply = requests.get(url).json()
        vendor = "Unknown vendor"
        if 'company' in reply['result']:
            vendor = reply['result']['company']

        print ("Didn't find button with MAC of '"+mac+"' "+ vendor)
        macs[mac] = vendor
    return None

def arp_display(pkt):
    button = None
    result = None
    
    if pkt.haslayer(ARP) and pkt[ARP].op == 1: #who-has (request)
        ##if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
        button = findButtonInConfig(pkt[ARP].hwsrc)
    elif pkt.haslayer(UDP) and pkt[UDP].sport in [68]:
        #print ("Got UDP packet {}:{}".format(pkt[Ether].src,pkt[UDP].sport))
        button = findButtonInConfig(pkt[Ether].src)
        
    if button is not None:
        print(button['name']+" button pressed")
        module, function = button['action'].split(".")

        if module == 'socoabs':
            result = getattr(sonosInstance, function)(button['payload'])
        elif module == 'nestabs':
            result = getattr(nestInstance, function)(button['payload'])
        else:
            print("Module "+module+" not found")
            
    if result is not None and result is not "waiting" and "maker" in config:
        url = "https://maker.ifttt.com/trigger/" + config['maker']['action'] + "/with/key/" + config['maker']['key']
        requests.post(url, data={'value1': button['name'], 'value2': result})

def sniff_arpprobe(config_file):
    try:
        ## load in the button config
        print ("Loading Button Config")
        global config
        config = json.load(open(config_file))
        ## build out the helper instances
        print ("Building Sonos Instance")
        global sonosInstance
        sonosInstance = socoabs.SocoAbs(config['sonosabs'])
        print ("Building Nest Instance")
        global nestInstance
        nestInstance = nestabs.NestAbs(config['nestabs'])
        print ("Ready")
        
        global macs
        macs = dict()
        
        if config['scan']['type'] == "udp":
            filter_text = "udp and portrange 68"
        elif config['scan']['type'] == "arp":
            filter_text = "arp"
        else:
            filter_text = "arp or (udp and portrange 68)"
            
        
        
        sniff(
            iface=config['scan']['interface'],
            prn=arp_display, 
            filter=filter_text,
            store=0)
        
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, dest='config_file', default='buttons.json',
                        help='Location of the button config file')                
    args = parser.parse_args()
    sniff_arpprobe(args.config_file)

