FROM python:3.8
WORKDIR /app
COPY main_task/ .
EXPOSE 5555
RUN pip install requests flask apscheduler mysql.connector pytest
CMD python main.py
