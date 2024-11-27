from django.db import models
from django.urls import reverse_lazy


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість товару')
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.title}"

    def get_preview(self):
        return self.image.url if self.image else 'https://via.placeholder.com/300'

    def get_absolute_url(self):
        return reverse_lazy('goods:product', kwargs={'product_slug': self.slug})
