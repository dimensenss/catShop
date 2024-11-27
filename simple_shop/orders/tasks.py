# orders/tasks.py
from celery import shared_task
import pika
import json

from orders.models import Order

@shared_task
def send_order_to_queue(order_id):
    order = Order.objects.get(id=order_id)
    order_data = {
        "order_id": order.id,
        "user_name": order.user.get_full_name() if order.user.get_full_name() else order.user.username,
        "items": [{"product_name": str(item.name), "quantity": item.quantity, "price": str(item.price)} for item in
                  order.orderitem_set.all()],
        "total_amount": str(sum(item.price * item.quantity for item in order.orderitem_set.all())),
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='orders')

    channel.basic_publish(
        exchange='',
        routing_key='orders',
        body=json.dumps(order_data, ensure_ascii=False)
    )
    connection.close()

@shared_task
def send_to_topic(exchange_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    channel.basic_publish(exchange=exchange_name, routing_key='', body=json.dumps(message))
    connection.close()