import requests
from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import mysql.connector



def lines_parser(description):
  lines_list = ["central", "bakerloo", "circle", "district", "hammersmith-city", "jubilee", "metropolitan",
                  "northern",
                  "piccadilly", "victoria", "waterloo and city"]
  newlines = []
  for line in lines_list:
    if line in description.lower():
      newlines.append(line)

  return newlines


def sensor():
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    req = requests.get(
        "https://api.tfl.gov.uk/Line/central,bakerloo,circle,district,hammersmith-city,jubilee,metropolitan,northern,piccadilly,victoria,waterloo-city/Disruption")
    res = req.json()
    for item in res:
        lines = lines_parser(item["description"])
        data = {"time": time_now, "lines": lines, "description": item["description"], "type": item["type"],
                "updated": item.get("lastUpdate")}
        requests.post("http://46.101.79.249/tasks", json=data)


sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor, 'interval', hours=24, start_date='2022-07-01 16:00:00')

sched.start()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/", methods=['GET', 'POST'])
def home_page():
   
    if request.method == 'POST':
        mydb = mysql.connector.connect(
        host="mydb_new",
        user="root",
        password="testroot",
        database="newdb"
        )
        mycursor = mydb.cursor()
        # Then get the data from the form
        tag = request.form['tag']
        mycursor.execute(

            """
           SELECT distinct * FROM lines_uk where line ='{tag}'
                             """.format(tag=tag)
        )
        x = mycursor.fetchall()
        newdict = {}
        for item in x:
            if item[1] not in newdict:
                newdict[item[1]] = [item[4]]
            else:
                newdict[item[1]].append(item[4])
        return render_template('comments.html', comments=newdict)

    else:
        mydb = mysql.connector.connect(
        host="mydb_new",
        user="root",
        password="testroot",
        database="newdb"
        )
        mycursor = mydb.cursor()
        mycursor.execute(""" SELECT distinct * FROM lines_uk  """)
        x = mycursor.fetchall()
        newdict = {}
        for item in x:
            if item[1] not in newdict:
                newdict[item[1]] = [item[4]]
            else:
                newdict[item[1]].append(item[4])
        return render_template('comments.html', comments=newdict)


@app.route("/tasks/<string:task_id>", methods=["GET", "DELETE","PUT"])
def find_specific_task(task_id):
    mydb = mysql.connector.connect(
    host="mydb_new",
    user="root",
    password="testroot",
    database="newdb"
)
    mycursor = mydb.cursor()
    if request.method == "GET":
        mycursor.execute(

            """
           SELECT * FROM lines_uk where task_id ='{task_id}'
                             """.format(task_id=task_id)
        )
        results = mycursor.fetchall()
        final = []
        for item in results:
            content = {
                "line": item[2],
                "type": item[3],
                "description": item[4],
                "updated": item[5]}
            final.append(content)

        return jsonify(final)

    elif request.method == "DELETE":
        mycursor.execute(

            """
           DELETE * FROM lines_uk where task_id= '{task_id}'
                             """.format(task_id=int(task_id))
        )
        return "DELETE RECORD", task_id


@app.route("/tasks", methods=["GET", "POST"])
def find_tasks():
    mydb = mysql.connector.connect(
    host="mydb_new",
    user="root",
    password="testroot",
    database="newdb"
    )
    mycursor = mydb.cursor()
    if request.method == "POST":
        res = request.get_json()
        schedule = res["time"]
        lines = res["lines"]
        description = res["description"].replace("'", " ")
        incident_type = res["type"]
        last_update = res["updated"]

        task_id = "".join(schedule.split()[0].split(("-")))

        lines = ",".join(lines)

        query = f"""

        insert into lines_uk
         values
        (
        '{task_id}',
        '{schedule}',
        '{lines}',
        '{incident_type}',
        '{description}',
        '{last_update}'
        )
        
        """
        mycursor.execute(query)
        mydb.commit()

        return "inserted record into db"

    elif request.method == "GET":

        mycursor.execute(""" SELECT * FROM lines_uk """)
        x = mycursor.fetchall()
        final = []
        task_incidents = []
        if len(x) >= 1:
            new_task_id = x[0][0]
            new_schedule_time = x[0][1]

            for result in x:
                if result[0] == new_task_id:

                    task_incidents.append(
                        {
                            "line": result[2],
                            "type": result[3],
                            "description": result[4],
                            "updated": result[5]
                        }
                    )

                else:
                    content = {
                        "task_id": new_task_id,
                        "scheduler_time": new_schedule_time,
                        "incidents": task_incidents

                    }
                    final.append(content)

                    new_task_id = result[0]
                    # new_schedule_time = result[0]
                    task_incidents = [{
                        "line": result[2],
                        "type": result[3],
                        "description": result[4],
                        "updated": result[5]
                    }]

            content = {
                "task_id": result[0],
                "scheduler_time": result[1],
                "incidents": task_incidents

            }
            final.append(content)

            return jsonify(final)
        return "empty table"


if __name__ == '__main__':
    app.debug = True
    app.run(port=5555, host="0.0.0.0")
