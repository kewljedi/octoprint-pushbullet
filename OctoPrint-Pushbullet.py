#!/usr/bin/python

import sys, getopt, json, requests, yaml

#______      __
#| ___ \    / _|
#| |_/ /___| |_ ___ _ __ ___ _ __   ___ ___  ___
#|    // _ \  _/ _ \ '__/ _ \ '_ \ / __/ _ \/ __|
#| |\ \  __/ ||  __/ | |  __/ | | | (_|  __/\__ \
#\_| \_\___|_| \___|_|  \___|_| |_|\___\___||___/

#stuff I used to get here, thanks to all of these pages for the help!

#didn't know python at all before I started!
#these are the pages I used to learn and to give examples of the tasks needed
# https://docs.python.org/2/library/json.html
# https://docs.python.org/2/library/stdtypes.html#dict
# http://stackoverflow.com/questions/1006169/how-do-i-look-inside-a-python-object
# http://stackoverflow.com/questions/12592553/python-requests-multipart-http-post
# http://stackoverflow.com/questions/8127686/parsing-a-yaml-file-and-accessing-the-data


#of course I needed to know alot about the Pushbullet API
# https://docs.pushbullet.com/v2/pushes/
# https://docs.pushbullet.com/v2/upload-request/

#this will be an octoprint "plug-in" so of course
# http://docs.octoprint.org/en/master/events/index.html#configuration

#I used this for the fancy comment headers
# http://patorjk.com/software/taag/#p=display&f=Doom&t=Thanks%20for%20using%20OctoPiPushBullet

url = 'https://api.pushbullet.com/v2/';


#______                _   _
#|  ___|              | | (_)
#| |_ _   _ _ __   ___| |_ _  ___  _ __  ___
#|  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#| | | |_| | | | | (__| |_| | (_) | | | \__ \
#\_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def pushNote(title, body, authtoken, channeltag):
  result = False;
  pushdata = {
    'type':'note',
    'channel_tag':channeltag,
    'title':title,
    'body':body
  }

  jsonheaders = {'Content-Type':'application/json','Authorization':'Bearer ' + authtoken};

  pushresponse = requests.post(url + 'pushes', data=json.dumps(pushdata), headers=jsonheaders);
  if pushresponse.status_code == 200:
    result = True;

  return result;

def CaptureDone(filename, authtoken, channeltag):
  #this event uploads the finish image to the pushbullet channel!
  result = False;

  # first thing first we need to find the file that is the last image taken.
  # lucky for us there are several examples that say it is:
  # /tmp/printDone.jpg this will be a parameter on the command line.
  filepath = '/tmp/printDone.jpg';
  filemime = 'image/jpeg';

  jsonheaders = {'Content-Type':'application/json','Authorization':'Bearer ' + authtoken};


  # now we need to tell pushbullet that we are going to upload a file
  filedata = {
    'file_name':'printDone.jpg',
    'file_type':filemime
  }
  fileresponse = requests.post(url + 'upload-request', data=json.dumps(filedata), headers=jsonheaders);
  if fileresponse.status_code == 200:
    #fileresponse should now have the url I need to post the file to...
    #as well as the final resting place for the file (fileurl)
    #it also includes a data element that needs to go with the file post.
    fileresponsedata = fileresponse.json();
    fileuploadurl = fileresponsedata['upload_url'];
    fileurl = fileresponsedata['file_url'];
    uploaddata = fileresponsedata['data'];

    # So now I need to do a multipart put of data to the fileuploadurl
    files = [('file', (outputFile, open(outputFile, 'rb'), filemime ))]
    fileuploadresponse = requests.post(fileuploadurl, files=files, data=uploaddata);
    if fileuploadresponse.status_code == 204:

      #finally I just need to do a simple push of all of this as a file type, and it should appear.
      pushdata = {
        'type' : 'file',
        'file_name': 'printDone.jpg',
        'file_type': filemime,
        'file_url': fileurl,
        'body': 'Your print has finished!!!',
        'channel_tag': channeltag
      }

      pushresponse = requests.post(url + 'pushes', data=json.dumps(pushdata), headers=jsonheaders);
      if pushresponse.status_code == 200:
        result = True;

  return result;

def PrintDone(filename, origin, time, authtoken, channeltag):
  #this sends a note to the channel when a print has finished
  result = pushNote('Finished ' + filename, 'Your print of ' + filename + ' Finished after ' + time, authtoken,channeltag);
  return result;

def PrintFailed(filename, origin, authtoken, channeltag):
  result = pushNote('Failed ' + filename, 'Your print of ' + filename + ' failed', authtoken, channeltag);
  return result;

def Error(error, authtoken, channeltag):
  result = pushNote('Printer Error', error, authtoken, channeltag);
  return result;

#___  ___      _       _ _
#|  \/  |     (_)     | (_)
#| .  . | __ _ _ _ __ | |_ _ __   ___
#| |\/| |/ _` | | '_ \| | | '_ \ / _ \
#| |  | | (_| | | | | | | | | | |  __/
#\_|  |_/\__,_|_|_| |_|_|_|_| |_|\___|

def main(argv):
  event = '';
  try:
    opts, args = getopt.getopt(argv,"he:f:o:t:e:",["eventname=","filename=","origin=","time=","error="])
  except getopt.GetoptError:
    print 'OctoPrint-Pushbullet.py -e <eventname>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'OctoPrint-Pushbullet.py -e <eventname>'
      sys.exit()
    elif opt in ("-e","--eventname"):
      eventname = arg
    elif opt in ("-f","--filename"):
      filename = arg
    elif opt in ("-o","--origin"):
      origin = arg
    elif opt in ("t","--time"):
      time = arg
    elif opt in ("e","--error"):
      error = arg

  with open('config.yaml', 'r') as f:
    config = yaml.load(f)

  authtoken = config['authtoken'];
  channeltag = config['channeltag'];

  if eventname == 'PrintDone':
    PrintDone(filename,origin, time, authtoken, channeltag)
  elif eventname == 'PrintFailed':
    PrintFailed(filename,origin, authtoken, channeltag)
  elif eventname == 'Error':
    Error(error, authtoken, channeltag)
  elif eventname == 'CaptureDone':
    CaptureDone(filename, authtoken, channeltag)

if __name__ == "__main__":
  main(sys.argv[1:])