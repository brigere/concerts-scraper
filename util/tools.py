from inspect import _void
from typing import List
from util.scraper import Show
import json


def sanitizeData(data: List[Show]) -> List[Show]:
  for item in data:
    if 'en ' in item.place:
      item.place = item.place.replace('en el ', '')
      item.place = item.place.replace('en ', '')
    
  return data
  
def write_result(source_name: str, data: List[Show]) -> None:
  data = [x.__dict__ for x in data]

  with open(f"result_data/_{source_name}.json", "w") as file:
    file.write(json.dumps(data))

  print(f"{source_name}: {len(data)}")