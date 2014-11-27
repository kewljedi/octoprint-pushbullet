octoprint-pushbullet
====================

Script to be used with Octoprint, that will send notifications to Pushbullet.

Well it will once it is done, this is still in developement and isn't even close to alpha quality.
I am learning python with this project, so Um... not the best pratices I am sure. 
I will try to clean it up once I get it working. 

You must edit your ~/.octoprint/config.yaml file to add the events that you want to push to PushBullet.
I plan on supporting:
- CaptureDone
- PrintDone
- PrintFailed
- Error

Config File
============
A config file needs to be created inside your ~/OctoPrint-Pushbullet directory named config.yaml
It holds two values:
- authtoken 
  which is your Pushbullet access token found here https://www.pushbullet.com/account
- chaneltag
  which is the channel tag for the channel you created in your Pushbullet configuration
  
OctoPrint Event Setup
=======================
if you wanted to use all of these this would need to be added to your config.
```
events:
  enabled: True
  subscriptions:
  - event: PrintDone
    command: python ~/OctoPrint-Pushbullet/OctoPrint-Pushbullet.py -e PrintDone
    type: system
  - event: PrintFailed
    command: python ~/OctoPrint-Pushbullet/OctoPrint-Pushbullet.py -e PrintFailed
    type: system
  - event: Error
    command: python ~/OctoPrint-Pushbullet/OctoPrint-Pushbullet.py -e Error
    type: system
  - event: CaptureDone
    command: python ~/OctoPrint-Pushbullet/OctoPrint-Pushbullet.py -e CaptureDone
```
