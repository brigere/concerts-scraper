from util.data import get_web_sources
from util.scraper import ScraperFactory
from util.tools import write_result

def scrap_pages():
  web_sources = get_web_sources()
  total_show_result = []

  for w in web_sources:
    print(f"{w.name} | {w.url}")
    scraper = ScraperFactory.create_scraper(w)
    print(scraper)
    concerts_data = scraper.get_concerts_data()
    total_show_result = total_show_result + concerts_data
    write_result(w.name, concerts_data)

  write_result("total", total_show_result)

    
scrap_pages()
