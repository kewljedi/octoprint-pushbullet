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

Pushbullet Channel Setup
========================
I created a channel so that my friends could subscribe to the channel and see these pushes as well. Use this page https://www.pushbullet.com/my-channels to create your channel and note the channel tag, because it will be needed in the Config file.

Pip installs
============
'''
sudo pip install pyyaml
sudo pip install requests
'''

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
    command: python ~/OctoPrint-Pushbullet/OctoPrint-Pushbullet.py --eventname PrintDone --filename {file} --origin {origin} --time {time}
    type: system
  - event: PrintFailed
    command: python ~/OctoPrint-Pushbullet/OctoPrint-Pushbullet.py --eventname PrintFailed --filename {file} --origin {origin}
    type: system
  - event: Error
    command: python ~/OctoPrint-Pushbullet/OctoPrint-Pushbullet.py --eventname Error --error {error}
    type: system
  - event: CaptureDone
    command: python ~/OctoPrint-Pushbullet/OctoPrint-Pushbullet.py --eventname CaptureDone --filename {file}
```
