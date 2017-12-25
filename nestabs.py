#!/usr/bin/env python3
#

## nestabs.py
## This is an abstaction that acts as a controller for a local Sonos installation
import nest
import time
import sys

class NestAbs:
    lastToggle = 0
    config = None
    napi = None
    
    def __init__(self,config):
        self.config = config
        self.napi = nest.Nest(client_id=self.config['id'], client_secret=self.config['secret'], access_token_cache_file='nest.cache')
        if self.napi.authorization_required:
            print('Go to ' + self.napi.authorize_url + ' to authorize, then enter PIN below')
            if sys.version_info[0] < 3:
                pin = raw_input("PIN: ")
            else:
                pin = input("PIN: ")
            self.napi.request_token(pin)
        
    def toggle(self,payload):
        state= "error"
        if self.lastToggle + 5 < time.time():
            for structure in self.napi.structures:
                if structure.name == payload['location']:
                    #print 'Before: %s' % structure.away
                    if structure.away == "away":
                        structure.away = False
                        state = "nest home"
                    elif structure.away == "home":
                        structure.away = True
                        state = "nest away"
                    #print 'After: %s' % structure.away
                    self.lastToggle = time.time()
        else:
            print("Not toggling, too soon after last toggle")
            state = "waiting"
        return state

