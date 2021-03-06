#!/usr/bin/env python3
#

## socoabs.py
## This is an abstaction that acts as a controller for a local Sonos installation
import soco
import time

class SocoAbs:

    masterspeaker = None
    lastToggle = 0
    config = None
    lastAction = None
    
    def __init__(self,config):
        self.config = config
        speaker = soco.discover().pop()
        speaker.partymode()
        self.masterspeaker = speaker.group.coordinator
        
    def toggle(self,payload):
        state="error"
        if self.lastToggle + 5 < time.time():
            try:
                if self.masterspeaker.get_current_transport_info()['current_transport_state'] == 'PLAYING':
                    print("Pausing Sonos")
                    self.masterspeaker.pause()
                    state = "paused"
                else:
                    print("Playing Sonos")
                    self.masterspeaker.play()
                    state = "playing"
                self.lastToggle = time.time()
                print("Done")
            except:
                print("General Sonos Failure... sorry")
        else:
            state = "waiting"
            print("Not toggling, too soon after last toggle")
        return state
        
    def playMp3Radio(self,payload):
        state="error"
        if self.lastToggle + 5 < time.time():
            try:
                if self.masterspeaker.get_current_transport_info()['current_transport_state'] == 'PLAYING' and self.lastAction == "playMp3":
                    print("Pausing Sonos")
                    self.masterspeaker.pause()
                    self.lastAction = None
                    state = "paused"
                else:
                    print("Playing Sonos")
                    self.masterspeaker.play_uri(payload['uri'], title=payload['title'])
                    self.lastAction = "playMp3"
                    state = "playing {}".format(payload['title'])
                self.lastToggle = time.time()
                print("Done")
            except:
                print("General Sonos Failure... sorry")
        else:
            state = "waiting"
            print("Not toggling, too soon after last toggle")
            
        return state
    
    def get_google_play_music_account(self,service_type):
        for key, account in soco.music_services.Account.get_accounts().iteritems():
            #print ("{}.{}".format(key,account.service_type)) 
            if account.service_type == service_type:
                return account
        raise Exception
    
    def playGoogleMusic(self,payload):
        ## Currently not working due to a service authentication error. https://github.com/SoCo/SoCo/issues/446
        
        state="error"
        if self.lastToggle + 5 < time.time():
            try:
                if self.masterspeaker.get_current_transport_info()['current_transport_state'] == 'PLAYING' and self.lastAction == "playGoogle":
                    print("Pausing Sonos")
                    self.masterspeaker.pause()
                    self.lastAction = None
                    state = "paused"
                else:
                    print("Playing Sonos")
                    play = soco.music_services.MusicService('Google Play Music',self.get_google_play_music_account('38663'))
                    result = play.search(category=payload['category'], term=payload['term'])
                    self.masterspeaker.play(result[0])
                    self.lastAction = "playGoogle"
                    state = "playing {}".format(payload['term'])
                self.lastToggle = time.time()
                print("Done")
            except:
                print("General Sonos Failure... sorry")
        else:
            state = "waiting"
            print("Not toggling, too soon after last toggle")
            
        return state