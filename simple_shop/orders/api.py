import json

import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

RABBITMQ_API_URL = "http://rabbitmq:15672/api"
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"


class RabbitMQChannelViewSet(ViewSet):
    def list(self, request):
        try:
            # Запит до RabbitMQ API для отримання списку каналів
            response = requests.get(
                f"{RABBITMQ_API_URL}/channels",
                auth=(RABBITMQ_USER, RABBITMQ_PASSWORD)
            )
            response.raise_for_status()
            data = response.json()
            for message in data:
                if 'payload' in message:
                    message['payload'] = json.loads(message['payload'])
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def get_orders_messages(self, request):
        try:
            url = f"{RABBITMQ_API_URL}/queues/%2F/orders/get"
            payload = {
                "count": 10,
                "ackmode": "ack_requeue_true",
                "encoding": "auto",
                "truncate": 50000
            }
            response = requests.post(
                url,
                auth=(RABBITMQ_USER, RABBITMQ_PASSWORD),
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def get_cancelled_orders(self, request):
        try:
            url = f"{RABBITMQ_API_URL}/exchanges/%2F/canceled_orders"
            response = requests.get(
                url,
                auth=(RABBITMQ_USER, RABBITMQ_PASSWORD),
            )
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def get_confirmed_orders(self, request):
        try:
            url = f"{RABBITMQ_API_URL}/exchanges/%2F/confirmed_orders"
            response = requests.get(
                url,
                auth=(RABBITMQ_USER, RABBITMQ_PASSWORD),
            )
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)