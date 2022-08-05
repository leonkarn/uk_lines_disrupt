schema = \
    """
task_id varchar(255),
     scheduler_time varchar(255),
     line varchar(255),
     type varchar(255),
     description LONGTEXT,
     last_update varchar(255)

"""
from datetime import datetime
import requests


def lines_parser(description):
    lines_list = ["central", "bakerloo", "circle", "district", "hammersmith-city", "jubilee", "metropolitan",
                  "northern",
                  "piccadilly", "victoria", "waterloo and city"]
    newlines = []
    for line in lines_list:
        if line in description.lower():
            newlines.append(line)

    return newlines


time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
req = requests.get(
    "https://api.tfl.gov.uk/Line/central,bakerloo,circle,district,hammersmith-city,jubilee,metropolitan,northern,piccadilly,victoria,waterloo-city/Disruption")
res = req.json()
print ("newresult",res)
for item in res:
    lines = lines_parser(item["description"])
    data = {"time": time_now, "lines": lines, "description": item["description"], "type": item["type"],
            "updated": item.get("lastUpdate")}
    requests.post("http://46.101.79.249/tasks", json=data)
