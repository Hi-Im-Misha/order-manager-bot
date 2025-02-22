import pika
import threading
import json
import pandas as pd

def send_to_queue(data, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Создание очереди
    channel.queue_declare(queue=queue_name, durable=True)

    # Отправка сообщения в очередь
    print(data, 'вводимые данные')
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(data))

    print("Сообщение успешно отправлено в очередь")

    # Закрытие соединения с RabbitMQ
    connection.close()

def consume_from_queue(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Создание очереди
    channel.queue_declare(queue=queue_name, durable=True)

    # Подписка на очередь и указание callback-функции для обработки сообщений
    def callback(ch, method, properties, body):
        print("Получено сообщение:", json.loads(body.decode()))
        # Обработка полученного сообщения
        order_data = json.loads(body.decode())
        product = order_data['product']
        user_id = order_data['user_id']
        # Обработка заказа
        try:
            df = pd.read_excel(r'Git_project\telegram_bot\create_cart_bot_telegram\bot_forwarder_telegram\catalog-1730980449.xlsx')
        except Exception as e:
            print(f"Ошибка чтения файла Excel: {e}")
            # ...

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Запуск цикла ожидания сообщений
    channel.start_consuming()

def start_consuming_thread(queue_name):
    threading.Thread(target=consume_from_queue, args=(queue_name,)).start()

start_consuming_thread('orders_queue')