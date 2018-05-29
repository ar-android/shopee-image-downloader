#!/usr/bin/env python
import os
import sys
import requests
import json
import shutil
from urllib.parse import urlparse

version = 'Version 1.0.0'

def log_red(str):
  log("\033[91m{}\033[00m".format(str))

def log_green(str):
  log("\033[92m{}\033[00m".format(str))

def log_yelow(str):
  log("\033[93m{}\033[00m".format(str))

def log(msg):
  print(msg)

def tab(str = ''):
  return "    " + str

def tabs(str = ''):
  return tab() + tab(str)

def greeting():
  log('\n')
  log_green(tab('Welcome to Shopee image downloader cli.\n'))
  log(tab("Usage: "))
  log_yelow(tabs("sopi-dl <shopee-product-url> -o <image-dir>\n"))
  log(tab("Options :"))
  log_yelow(tabs("-V,  --version        Display application version"))
  log_yelow(tabs("-o,  --output         Output directory download image"))
  log_yelow(tabs("-nn, --nonumbering    Enable auto numbering image name"))
  log_yelow(tabs("-h,  --help           Display help command\n"))
  log(tab('Example : '))
  log_yelow(tab('sopi-dl https://shopee.co.id/Koko-Azura-Satu-set-baju-lebaran-anak-baju-koko-anak-sarung-anak-baju-lebaran-murah-i.31767369.1198797017 -o images -nn'))
  log('\n')

def run_download():
  url = urlparse(sys.argv[1])
  if not url.scheme:
    log("Url is invalid.")
  apiUrl = "https://shopee.co.id/api/v2/item/get?itemid={0}&shopid={1}".format(url.path.split('.')[2], url.path.split('.')[1])
  response = requests.get(apiUrl)
  if not response:
    log('Failed load shopee url.')
  else:
    downloadImages(response.content)

def downloadImages(jsonString):
  data = json.loads(jsonString)
  images = data['item']['images']
  haveOutDir = len(sys.argv) > 3 and sys.argv[2] == '-o'
  imgDir = sys.argv[3] + '/' if haveOutDir else ''
  is_numbering = len(sys.argv) > 4 and sys.argv[4] == '-nn' or sys.argv[4] == '--nonumbering'
  for number, image in enumerate(images, start=1):
    if haveOutDir:
      create_dir_if_needed(imgDir)
    imageName = imgDir
    imageName += '{}.jpg'.format(number) if is_numbering else image + '.jpg'
    url = 'https://cf.shopee.co.id/file/{}'.format(image)
    log('{} image downloaded.'.format(number))
    response = requests.get(url, stream=True)
    with open(imageName, 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    del response

def create_dir_if_needed(directory):
  if not os.path.exists(directory):
        os.makedirs(directory)

def enter(msg):
  log('\n')
  log(msg)
  log('\n')

def displayVersion():
  log_green('Shopee image downloader cli :')
  log_yelow(version)

def run():
  if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help' :
      greeting()
    elif sys.argv[1] == '-V' or sys.argv[1] == '--version' :
      displayVersion()
    else:
      url = urlparse(sys.argv[1])
      if not url.scheme and not len(url.path.split('.')) > 2:
        enter(tab() + "Your url input is incorrect.")
      else:
        run_download()
  else:
    greeting()
