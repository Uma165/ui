from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock_quantity', 'created_by')
    search_fields = ('name', 'created_by__username')  # Поиск по имени товара и создателя
    list_filter = ('price', 'stock_quantity', 'created_by')  # Фильтрация по цене, количеству и создателю
    ordering = ('name', 'price')  # Сортировка по имени и цене

    def save_model(self, request, obj, form, change):
        if not change:
            # Если объект создается, установите пользователя создателя на текущего пользователя
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Product, ProductAdmin)
