To run the service  run this command:
~~~
docker-compose build
~~~
and after 
~~~
docker-compose up
~~~
The service is up after the steps above.

If we want to trigger API calls we open a new terminal and run this command:
~~~
docker exec -it instashop_main /bin/bash
~~~
and inside the container we run 

~~~
python make_api_calls.py
~~~

For testing we ran
~~~
pytest
~~~

To see all the task we go to:
http://localhost:5555/tasks

If want to see a specific task_id
http://localhost:5555/tasks/<task_id>

