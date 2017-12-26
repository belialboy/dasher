# dasher
This is (yet another) server that makes use of your Amazon Dash buttons to trigger other actions. I originally wrote this back in November 2016, and didn't touch it again till now. I've freshened it up a bit to make it a little more extensable, but moreover I needed to change the trigger mechanism; it seems that Amazon have updated the buttons so that they no longer send ARP packets, so I've moved to monitoring for DHCP requests (UDP 67-68) which they now use. The shell still _can_ trigger on ARP packets, but that's not how you'll get your Dash buttons working with it.

You need to pair your Amazon Dash button to your WiFi, but *DO NOT* link it to a product... simply quit out of the process at that point.

Run up the arpprobe and click your button. You'll see a MAC address show up. This is the MAC you'll need to copy into your buttons.json file to have it then trigger an event. It makes a call out to macvendors.co to try to work out who the vendor of the network device is to help you a little.

I've provided two such interfaces;
* Soco - This is a Sonos integration and allows you to trigger "play" and "pause", as well as playing the URI of a provided internet radio station. There is a method which will play a Google Music Station, but the underlying API's recently broke after a Google update, so I'm waiting for this to get fixed.
* Nest - This is an integration with the thermostats and allows you to manually set "away" or "home" for a given location. I use this as a button next to my home alarm, so that I can set away and home if the system hasn't caught up with me. Your "location" must match the structure location used by Nest. This is a string that you will have set in Nest when you set up your system

There is also a Maker (WebHook) for IFTTT integrated so that you get notified when buttons are pressed... and this got me to thinking. It's not just the Amazon Dash buttons making DHCP requests on the network when they are _turned on_. So why not have notifications and actions performed when other devices send these requests? So, yes, you can do that too. I've got mine set up so that I get alerted when my Playstation is turned on. Handy for tracking how much time the kids spend on it.

## Requirements
This is python3, so should work anywhere where you can install python. I've got it running both on Win10 and on a QNAP virtual machine (I'm about to build it into a docker container too). There are some library requirements though:
* requests - https://github.com/requests/requests
* scapy - https://github.com/secdev/scapy
* python-nest - https://github.com/jkoelker/python-nest 
* soco - https://github.com/SoCo/SoCo
