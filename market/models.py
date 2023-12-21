from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


class CustomUser(AbstractUser):
    isAdmin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions'
    )

    def __str__(self):
        return self.username


class Product(models.Model):
    created_by = models.CharField(max_length=250, null=True)
    image = models.ImageField()  # Поле для изображения товара
    name = models.CharField(max_length=255)  # Название товара
    description = models.TextField()  # Полное описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Стоимость товара
    stock_quantity = models.IntegerField()  # Количество товаров на складе

    def __str__(self):  # Представление ввиде строки, необходимо для сортировок
        return self.name


class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    positions = models.JSONField()
