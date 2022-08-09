from inspect import _void
from typing import List
from util.scraper import Show
import json


def write_result(source_name: str, data: List[Show]) -> None:
  data = [x.__dict__ for x in data]

  with open(f"{source_name}.json", "w") as file:
    file.write(json.dumps(data))

  print(f"_{source_name}: {len(data)}")