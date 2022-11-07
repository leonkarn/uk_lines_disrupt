from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
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


def print_firstdag():
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    req = requests.get(
        "https://api.tfl.gov.uk/Line/central,bakerloo,circle,district,hammersmith-city,jubilee,metropolitan,northern,piccadilly,victoria,waterloo-city/Disruption")
    res = req.json()
    for item in res:
        lines = lines_parser(item["description"])
        data = {"time": time_now, "lines": lines, "description": item["description"], "type": item["type"],
                "updated": item.get("lastUpdate")}
        requests.post("http://instashop_main:5555/tasks", json=data)

dag = DAG('first_dag', description='HevoData Dag',
          schedule_interval='0 8 * * *',
          start_date=datetime(2022, 2, 24), catchup=False)

print_operator = PythonOperator(task_id='new_task_name', python_callable=print_firstdag, dag=dag)

print_operator