import json
from typing import List
from urllib.request import urlopen

import requests

class WebSource:
  def __init__(self, name, url) -> None:
      self.name = name
      self.url = url

  def get_row_html(self) -> str | None:
    
    if self.html: return self.html
    
    try:
      self.html = requests.get(self.url).text
      return self.html
    except:
      print(f"an error ocurrer while reading {self.url}")
      return None

def get_web_sources() -> List[WebSource]:  
  result = []
  with open("/home/btal/Documents/dev/scraper/util/sources.json") as file:
    row_data = json.load(file)
    result = [WebSource(x["name"], x["url"]) for x in row_data]
  
  return result

def save_content(path: str, data: str):
  with open(path,"w") as file:
    file.write(data)
    print(f"{path.split('/')[-1]} saved")

def download_page_content():
  pass