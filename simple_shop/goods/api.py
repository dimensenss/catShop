from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from goods.models import Product
from goods.serializers import ProductSerializer


class ProductViewModel(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_summary="Отримати список продуктів",
        operation_description="Повертає список усіх продуктів у системі.",
        responses={200: ProductSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Створити продукт",
        operation_description="Додає новий продукт до системи.",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: openapi.Response(description="Помилка валідації"),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Отримати продукт за ID",
        operation_description="Повертає дані про продукт за його ID.",
        responses={200: ProductSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Оновити продукт",
        operation_description="Повне оновлення даних продукту.",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: openapi.Response(description="Помилка валідації"),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частково оновити продукт",
        operation_description="Часткове оновлення даних продукту.",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: openapi.Response(description="Помилка валідації"),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Видалити продукт",
        operation_description="Видаляє продукт із системи.",
        responses={204: openapi.Response(description="Продукт видалено")}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)