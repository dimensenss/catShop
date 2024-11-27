from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from rest_framework.routers import SimpleRouter

from .api import RabbitMQChannelViewSet
from .views import *

app_name = 'orders'

router = SimpleRouter()
router.register(r'api/v1/channels', RabbitMQChannelViewSet, basename='rabbitmq-channel')
urlpatterns = [
    path('create-order/', create_order, name = 'create_order'),
    path('success-order/<int:order_id>/', success_order, name = 'success_order'),
] + router.urls
