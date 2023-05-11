import csv
import os
import sys
import requests
from pprint import pprint

import pandas as pd
from bs4 import BeautifulSoup

webhook = 'enter your webhook'

def scraping():
  url = 'https://pixiv-waengallery.com/'
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  result = []
  for top_exhibition in soup.find_all(class_='u-list_type2_item_inner'):
    result.append([
      top_exhibition.find(class_='u-list_type2_text1').text,
      top_exhibition.find(class_='u-list_type2_text2').text,
      top_exhibition.get('href')
    ])
  return result

def output_csv(result):
  with open('last_log.csv', 'w', newline='',encoding='utf_8') as file:
    headers = ['Date', 'Title', 'URL']
    writer = csv.writer(file)
    writer.writerow(headers)
    for row in result:
      writer.writerow(row)

def read_csv():
  if not os.path.exists('last_log.csv'):
    raise Exception('ファイルがありません。')
  if os.path.getsize('last_log.csv') == 0:
    raise Exception('ファイルの中身が空です。')
  csv_list = pd.read_csv('last_log.csv', header=None).values.tolist()
  return csv_list

def list_diff(result, last_result):
  return_list = []
  for tmp in result:
    if tmp not in last_result:
      return_list.append(tmp)
  return return_list

def send_message(list):
  content = {
    "username": "pixiv WAEN GALLARY",
    "avatar_url": "https://pbs.twimg.com/profile_images/1096355393666568192/zSsiT4RS_400x400.png",
    "content": "展示予定が更新されました",
    "embeds": [
      {
        "title": "pixiv WAEN GALLARY",
        "description": list[0]+"\n"+list[1],
        "url": list[2]
      }
    ]
  }
  header = {
    "Content-Type": "application/json"
  }
  r = requests.post(webhook, headers=header, json=content)
  print(r.text)

result = scraping()
pprint(result)
try:
  oldcsv = read_csv()
except:
  output_csv(result)
  exit()

diff = list_diff(result, oldcsv)
pprint(diff)

if diff:
  for topic in diff:
    send_message(topic)

output_csv(result)

