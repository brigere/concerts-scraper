from util.data import WebSource, get_web_sources, save_content
from util.scraper import Show, BerlinScraper, Scraper, ScraperFactory
from config import DOWLOADED_PAGES_PATH
from typing import List
import json


def sanitizeData(data: List[Show]) -> List[Show]:
  for item in data:
    if 'en ' in item.place:
      item.place = item.place.replace('en el ', '')
      item.place = item.place.replace('en ', '')
    
  return data

def download_HTML_pages():
  web_sources = get_web_sources()

  for web_source in web_sources:
    html_data = web_source.get_row_content()
    path = DOWLOADED_PAGES_PATH + f"/{web_source.name}.html"
    save_content(path, html_data)

def scrap_pages():
  web_sources = get_web_sources()
  total_show_result = []

  for w in web_sources:
    print(f"{w.name} | {w.url}")
    scraper = ScraperFactory.create_scraper(w)
    print(scraper)
    concerts_data = scraper.get_concerts_data()
    total_show_result = total_show_result + concerts_data

  print(f"concerts found: {len(total_show_result)}")
  total_show_result = sanitizeData(total_show_result)

  data = [x.__dict__ for x in total_show_result]

  with open("result.json", "w") as file:
    file.write(json.dumps(data))

def test():
  ws = WebSource("icarus", "https://icarusmusicstore.com/29-recitales")
  scraper = ScraperFactory.create_scraper(ws)
  scraper.get_HTML_content()

  data: List[Show] = scraper.get_concerts_data()
  
  data = [x.__dict__ for x in data]

  with open("result.json", "w") as file:
    file.write(json.dumps(data))

  print(json.dumps(data))

def test2():
  web_sources = get_web_sources()
  scraper = ScraperFactory.create_scraper(web_sources[3])
  concerts = scraper.get_concerts_data()

  for concert in concerts:
    print(concert)
    
  

scrap_pages()

