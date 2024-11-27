from django.urls import path
from rest_framework.routers import SimpleRouter

from goods.api import ProductViewModel
from goods.views import *

app_name = 'goods'

router = SimpleRouter()
router.register('api/v1/cats-api', ProductViewModel)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('catalog', CatalogView.as_view(), name='catalog'),
    path('product/<slug:product_slug>/', ProductView.as_view(), name='product'),
] + router.urls
