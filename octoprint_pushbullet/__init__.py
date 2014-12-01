# coding=utf-8
from __future__ import absolute_import

__author__ = "kewljedi <kewljedi@gmail.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License"

import flask
import logging

import octoprint.plugin
import octoprint.events

import json
import requests

default_settings = {
  "authtoken": "",
  "channeltag" : "",
}
s = octoprint.plugin.plugin_settings("Pushbullet", defaults=default_settings)

url = 'https://api.pushbullet.com/v2/';

class PushbulletPlugin(octoprint.plugin.EventHandlerPlugin,
                  octoprint.plugin.StartupPlugin,
                  octoprint.plugin.SimpleApiPlugin,
                  octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.TemplatePlugin,
                  octoprint.plugin.AssetPlugin):
  def __init__(self):
    self.logger = logging.getLogger("octoprint.plugins." + __name__)

    self.host = None
    self.port = None

  #~~ StartupPlugin API

  def on_startup(self, host, port):
    self.host = host
    self.port = port

  def on_after_startup(self):
    authtoken = s.get(["authtoken"])
    channeltag = s.getInt(["channeltag"])

  #~~ TemplatePlugin API

  def get_template_vars(self):
    return dict(
      _settings_menu_entry="Pushbullet"
    )

  def get_template_folder(self):
    import os
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")

  ##~~ AssetPlugin API

  def get_asset_folder(self):
    import os
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")

  def get_assets(self):
    return {
      "js": ["js/growl.js"],
      "css": ["css/growl.css"],
      "less": ["less/growl.less"]
    }

  #~~ SimpleApiPlugin API

  # def get_api_commands(self):
  #   return dict(
  #     test=["host", "port"]
  #   )

  # def on_api_command(self, command, data):
  #   if command == "test":
  #     import gntp.notifier
  #     growl, message = self._register_growl(data["host"], data["port"], password=data["password"])
  #     if growl:
  #       try:
  #         growl.notify(
  #           noteType=GrowlMessages.TEST,
  #           title = "This is a test message",
  #           description = "If you can read this, OctoPrint successfully registered with this Growl instance"
  #         )
  #         return flask.jsonify(dict(success=True))
  #       except Exception as e:
  #         self.logger.exception("Sending test message to Growl instance on {host}:{port} failed".format(host=data["host"], port=data["port"]))
  #         return flask.jsonify(dict(success=False, msg=str(e.message)))
  #     else:
  #       return flask.jsonify(dict(success=False, msg=str(message)))

  #   return flask.make_response("Unknown command", 400)

  # def on_api_get(self, request):
  #   if not self.zeroconf_browse:
  #     return flask.jsonify(dict(
  #       browsing_enabled=False
  #     ))

  #   browse_results = self.zeroconf_browse("_gntp._tcp", block=True)
  #   growl_instances = [dict(name=v["name"], host=v["host"], port=v["port"]) for v in browse_results]

  #   return flask.jsonify(dict(
  #     browsing_enabled=True,
  #     growl_instances=growl_instances
  #   ))

  ##~~ SettingsPlugin API

  def on_settings_load(self):
    return dict(
      authtoken=s.get(["authtoken"]),
      channeltag=s.getInt(["channeltag"])
    )

  def on_settings_save(self, data):
    if "authtoken" in data and data["authtoken"]:
      s.set(["authtoken"], data["authtoken"])
    if "channeltag" in data and data["channeltag"]:
      s.setInt(["channeltag"], data["channeltag"])

  #~~ EventPlugin API

  def on_event(self, event, payload):
    import os

    title = description = None

    if event == octoprint.events.Events.UPLOAD:
      file = payload["file"]
      target = payload["target"]
      title = "A new file was uploaded"
      description = "{file} was uploaded {targetString}".format(file=file, targetString="to SD" if target == "sd" else "locally")

    elif event == octoprint.events.Events.PRINT_STARTED:
      file = os.path.basename(payload["file"])
      origin = payload["origin"]
      title = "A new print job was started"
      description = "{file} has started printing {originString}".format(file=file, originString="from SD" if origin == "sd" else "locally")

    elif event == octoprint.events.Events.PRINT_DONE:
      file = os.path.basename(payload["file"])
      elapsed_time = payload["time"]
      title = "Print job finished"
      description = "{file} finished printing, took {elapsed_time} seconds".format(file=file, elapsed_time=elapsed_time)

    pushNote(title, body, authtoken, channeltag)

  ##~~ Helpers

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

__plugin_name__ = "Pushbullet"
__plugin_description__ = "Get Pushbullet notifications to a custom channel from OctoPrint"
__plugin_implementations__ = [PushbulletPlugin()]