# coding=utf-8
import setuptools

def package_data_dirs(source, sub_folders):
  import os
  dirs = []

  for d in sub_folders:
    for dirname, _, files in os.walk(os.path.join(source, d)):
      dirname = os.path.relpath(dirname, source)
      for f in files:
        dirs.append(os.path.join(dirname, f))

  return dirs

def params():
  name = "OctoPrint-Pushbullet"
  version = "0.0.1"

  description = "Adds support to push OctoPrint events to a Pushbullet channel"
  long_description = "TODO"
  author = "kewljedi"
  author_email = "kewljedi@gmail.com"
  url = "https://github.com/kewljedi/octoprint-pushbullet"
  license = "GPLv3"

  packages = ["octoprint_pushbullet"]
  package_data = {"octoprint_pushbullet": package_data_dirs('octoprint_pushbullet', ['static', 'templates'])}

  include_package_data = True
  zip_safe = False
  install_requires = open("requirements.txt").read().split("\n")

  entry_points = {
    "octoprint.plugin": [
      "pushbullet = octoprint_pushbullet"
    ]
  }

  return locals()

setuptools.setup(**params())