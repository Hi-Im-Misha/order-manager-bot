FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "start.py"]

# # настроить рэбит на сервере
# sudo rabbitmqctl add_queue -p myvhost myqueue

# #запуск докера
# docker run -d -p 80:80 misha4123/myproject:latest
# http://91.184.252.77:15672/.

# ssh -L 15672:localhost:15672 root@91.184.252.77