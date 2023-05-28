from flask import Flask, request, jsonify, Response
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import mysql.connector
import requests
from bs4 import BeautifulSoup
from flask_login import login_required
from flask import render_template, redirect, url_for
from flask_sqlalchemy import Pagination


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


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.disable_buffering()
    return rv


def generate():
    # # rightmove web scrapper
    mydb = mysql.connector.connect(
        host="mydb_new",
        user="root",
        password="testroot",
        database="newdb"
    )
    mycursor = mydb.cursor()

    url = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=1&maxPrice=1750&minPrice=1500&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="
    newset = set()
    x = requests.get(url)

    soup = BeautifulSoup(x.text, 'html.parser')
    for link in soup.find_all('div', class_="propertyCard-details"):
        newset.add(link.find(class_="propertyCard-link").find(class_="propertyCard-address").find("meta")["content"])

    # try next pages
    index = 0

    url_next_page = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=1&maxPrice=1750&minPrice=1500&index={}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=".format(
        index)
    x = requests.get(url_next_page)

    while x.status_code == 200:
        soup = BeautifulSoup(x.text, 'html.parser')
        for link in soup.find_all('div', class_="propertyCard-details"):
            newitem = link.find(class_="propertyCard-link").find(class_="propertyCard-address").find("meta")["content"]
            if newitem != "":
                newset.add(newitem)
                yield str(newitem)

                newitem = newitem.replace("'", " ")

                query = f"""

                        insert ignore into houses
                         values
                        (
                        '{newitem}',
                        'no_rightmove_link',
                        'no_zoopla_link'
                        
                        )

                        """
                mycursor.execute(query)
                mydb.commit()

        index += 24
        url_next_page = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=1&maxPrice=1750&minPrice=1500&index={}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=".format(
            index)
        x = requests.get(url_next_page)


@app.route('/stream', methods=["GET", "POST"])
def stream_view():
    if request.method == "POST":
        rows = generate()
        return Response(stream_template('template.html', rows=rows))
    else:
        mydb = mysql.connector.connect(
            host="mydb_new",
            user="root",
            password="testroot",
            database="newdb"
        )
        mycursor = mydb.cursor()
        query = "select property_name from houses "
        mycursor.execute(query)
        x = mycursor.fetchall()

        num_records = len(x)

        page = int(request.args.get('page', 1))
        per_page = 15

        # Calculate offset
        offset = (page - 1) * per_page

        x = x[offset:offset+per_page]

        return Response(render_template('template.html', rows=x, page=page, per_page=per_page, total_count=num_records))


# --------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('new_houses'))


@login_required
@app.route("/newhouses", methods=['GET', 'POST'])
def new_houses():
    return render_template('newhouses.html')


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
        newdict = dict(sorted(newdict.items()))
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
        newdict = dict(sorted(newdict.items(), reverse=True))
        newtable_vals = [

            {"id": 1, "name": "John", "country": "greece", "city": "athens"},
            {"id": 2, "name": "Leo", "country": "usa", "city": "athens"},
            {"id": 3, "name": "philip", "country": "uk", "city": "London"},
            {"id": 4, "name": "james", "country": "greece", "city": "larisa"},

        ]

        return render_template('comments.html', comments=newdict, newvals=newtable_vals)


@app.route("/tasks/<string:task_id>", methods=["GET", "DELETE", "PUT"])
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
