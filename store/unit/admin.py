# admin.py в приложении unit
from django.contrib import admin
from .models import UnitProduct
from django.utils.translation import gettext_lazy as _

class UnitProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'serial_code', 'status', 'preorder_date', 'request_date', 'arrival_date', 'sale_date', 'return_date')
    list_filter = ('status', 'product', 'preorder_date', 'request_date', 'arrival_date', 'sale_date', 'return_date')
    search_fields = ('serial_code', 'product__name')  # Поиск по коду и имени товара
    ordering = ('status', 'product')  # Сортировка по статусу и товару

    # Для отображения статуса как читаемых значений (например, "Продан" вместо "sold")
    def status_display(self, obj):
        return obj.get_status_display()

    status_display.short_description = _('Статус')  # Заголовок для нового поля в таблице

    # Функция для отображения стоимости товара в магазине
    def store_price(self, obj):
        return obj.arrival_price if obj.status == 'in_store' else None

    store_price.short_description = _('Цена в магазине')

    # Функция для отображения цены продажи
    def sale_price_display(self, obj):
        return obj.sale_price if obj.status == 'sold' else None

    sale_price_display.short_description = _('Цена продажи')

    # Добавим инлайн для отображения списка карточек товара, привязанных к товару
    class UnitProductInline(admin.TabularInline):
        model = UnitProduct
        extra = 1
        fields = ['serial_code', 'status', 'preorder_date', 'request_date', 'arrival_date', 'sale_date', 'return_date']
        readonly_fields = ['serial_code', 'status', 'preorder_date', 'request_date', 'arrival_date', 'sale_date', 'return_date']

    # Регистрация inline для просмотра связанной модели
    inlines = [UnitProductInline]

# Регистрация модели UnitProduct в админке
admin.site.register(UnitProduct, UnitProductAdmin)
