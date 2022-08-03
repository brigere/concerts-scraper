from email.mime import base
from platform import platform
from unittest import result
import requests
from util.data import WebSource
from bs4 import BeautifulSoup
from typing import List
import json

dates_enum = {
  "MAR": "03",
  "AGO": "08",
  "SEP": "09",
  "OCT": "10",
  "NOV": "11",
  "DIC": "12",
  "Agosto": "08",
  "Septiembre": "09",
  "Octubre": "10",
  "Noviembre": "11",
  "Diciembre": "12"
}

class Show:
  def __init__(self, band_name, date, place, description_link, tickets_link, image_link) -> None:
      self.band_name = band_name
      self.date = date
      self.place = place
      self.description_link = description_link
      self.tickets_link = tickets_link 
      self.image_link = image_link
  def __str__(self) -> str:
      return f"Artist: {self.band_name} | {self.place} | {self.date} | {self.place}"

  def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class Scraper:
  def __init__(self, platform_name: str, platform_url: str) -> None:
    self.platform_name = platform_name
    self.platform_url = platform_url

    self.html_row_content: str | None = None
    self.soup: str | None = None
    self.html_row_content: str | None = None  

  def get_HTML_content(self) -> str | None:
    if self.html_row_content != None: 
      return self.html_row_content
    
    try:
      page_content = requests.get(self.platform_url).text
      self.html_row_content = page_content
      return page_content
    except:
      print(f"An error ocurred fetching data from {self.platform_url}")
      return None
  
  def get_concerts_data(self):
    pass

  def create_soup(self):
    html = self.get_HTML_content()
    return BeautifulSoup(html, "html.parser")

class BerlinScraper(Scraper):
  def __init__(self, platform_name: str, platform_url: str) -> None:
      Scraper.__init__(self, platform_name, platform_url)

  def get_concerts_data(self) -> List[Show]:
    result: List[Show] = []
    soup = self.create_soup()

    concert_links = soup.find_all("a", class_="eg-item-skin-1-element-16")

    for link in concert_links:
      description_link = link["href"]
      date = link.text
      place = "Cafe Berlin"

      data = requests.get(description_link).text
      soup = BeautifulSoup(data, "html.parser")
      
      band_name = soup.find("h1", class_="elementor-heading-title elementor-size-default").text
      image_link = soup.find("img")["src"]
      tickets_link = self.get_tickets_link(soup.find_all("strong"))

      result.append(Show(band_name, date, place, description_link, tickets_link, image_link))
    
    return result

  def get_tickets_link(self, strong_tags):
    for item in strong_tags:
      if "http" in item.text:
        return item.text
    return None

class LivapassScraper(Scraper):
  def __init__(self, platform_name: str, platform_url: str) -> None:
      super().__init__(platform_name, platform_url)

  def sanitizeDate(self, date: str) -> str:
    [day, month] = date.split(' ')
    if dates_enum[month]:
      month = dates_enum[month]

    return f"{day}/{month}/2022"

  def get_concerts_data(self) -> List[Show]:
    result = []
    soup = self.create_soup()
    data = soup.find_all("div", class_="event-home starred item box-shadow-none p-a-xs")
    data = data + soup.find_all("div", class_="event-home starred w-full item box-shadow-none")
    
    for item in data:
      link = self.get_description_link(item)
      image_link = item.find("img")["src"]
      date = item.find("p").text
      date = self.sanitizeDate(date)
      artist_name: str = self.get_artist_name(item.find("h1").text)
      place: str = self.get_place(item.find("h1").text)

      result.append(Show(artist_name, date, place, link, link, image_link))

    return result
  
  def get_description_link(self, item):
    base_url = "https://livepass.com.ar/events"
    path = item.a["href"]

    return base_url + path

  def get_artist_name(self, text: str) -> str:
    return text.split('en')[0].rstrip()

  def get_place(self, text: str) -> str:
    if ' en ' in text:
      place = text[text.index(' en '):]
      return place.lstrip()
    else:
      return ""

class GranrexScraper(Scraper):
  def __init__(self, platform_name: str, platform_url: str) -> None:
      super().__init__(platform_name, platform_url)

  def get_concerts_data(self) -> List[Show]:
    result = []
    soup = self.create_soup()
    data = soup.find_all("article", class_="itemSearch showList")

    for item in data:
      image = item.find("img")["src"] 
      description_link = item.find("a")["href"]
      artist_name = item.find("p", class_="itemSearchTitle").a.text
      dates = item.find("p", class_="date")
      date = dates.span.text
      place = "Teatro Gran Rex"

      result.append(Show(artist_name, date, place, description_link, description_link, image))

    return result

class TrastiendaScraper(Scraper):
  def __init__(self, platform_name: str, platform_url: str) -> None:
      super().__init__(platform_name, platform_url)

  def sanitizeDate(self, date: str) -> str:
    [day, month] = date.split('/')
    if dates_enum[month]:
      month = dates_enum[month]

    return f"{day}/{month}/2022"
  
  def get_concerts_data(self) -> List[Show]:
    result = []
    soup = self.create_soup()
    data = soup.find_all("div", class_="fs-item")
    
    for item in data:
      artist_name = item.find("h5").a.text
      date = self.get_date(item)
      date = self.sanitizeDate(date)
      image = self.get_image(item)
      place = "La trastienda"
      description_link = self.get_description_link(item)
      result.append(Show(artist_name, date, place, description_link, description_link, image))

    return result
      
  def get_date(self, parent_item):
    partial_date = parent_item.find("div", class_="fs-date").find_all("span")
    return partial_date[0].text + "/" + partial_date[1].text  
  
  def get_description_link(self, item):
    a_tag = item.find("a")
    return a_tag["href"]

  def get_image(self, parent_item):
    return parent_item.find("div", class_="fs-thumb").a.img["src"]

class IcarusScraper(Scraper):
  def __init__(self, platform_name: str, platform_url: str) -> None:
      super().__init__(platform_name, platform_url)
  
  def get_concerts_data(self) -> List[Show]:
    result = []
    soup = self.create_soup()
    data = soup.find_all("article", class_="product-container product-style")
    
    for item in data:
      image_link = self.get_image_url(item)
      artist_name = self.get_artist_name(item)
      date = self.get_date(item)

      result.append(Show(artist_name, date, None, None, None, image_link))

  def get_image_url(self, parent_item):
    return parent_item.find("div", class_="product-thumbnail").a.img["data-original"]
  
  def get_artist_name(self, parent_item):
    return parent_item.find("h5").a.text

  def get_date(self, parent_item):
    return None    

class ScraperFactory:
  def create_scraper(platform: WebSource) -> BerlinScraper | None:
    if platform.name == "cafeberlin":
      return BerlinScraper(platform.name, platform.url)
    
    if platform.name == "livepass":
      return LivapassScraper(platform.name, platform.url)
    
    if platform.name == "granrex":
      return GranrexScraper(platform.name, platform.url)
    
    if platform.name == "trastienda":
      return TrastiendaScraper(platform.name, platform.url)

    if platform.name == "icarus":
      return IcarusScraper(platform.name, platform.url)

