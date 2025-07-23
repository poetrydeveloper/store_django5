# models.py в приложении products
import uuid
from django.db import models
from django.utils import timezone
from products.models import Product


class UnitProduct(models.Model):
    STATUS_CHOICES = [
        ('preorder', 'Предварительная заявка'),
        ('requests', 'Заявка'),
        ('in_store', 'В магазине'),
        ('sold', 'Продан'),
        ('returned', 'Возврат')
    ]

    # Связь с товаром
    product = models.ForeignKey(Product, related_name="unit_products", on_delete=models.CASCADE)
    serial_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="Уникальный код")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True, verbose_name="Статус")

    # Даты для отслеживания событий
    preorder_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата предварительного заказа")
    request_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата заявки")
    arrival_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата прихода товара")
    sale_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата продажи")
    return_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата возврата")

    # Цены
    preorder_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                         verbose_name="Цена в предварительной заявке")
    request_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                        verbose_name="Цена в заявке")
    arrival_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                        verbose_name="Цена прихода")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                     verbose_name="Цена продажи")

    # Рекомендованная цена для магазина
    recommended_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                            verbose_name="Рекомендованная цена")

    def __str__(self):
        return f"{self.product.name} ({self.serial_code}) - {self.get_status_display()}"

    def change_status(self, new_status):
        """Изменяем статус товара и соответствующие даты"""
        self.status = new_status

        if new_status == 'preorder':
            self.preorder_date = timezone.now()  # Устанавливаем дату для предварительного заказа

        elif new_status == 'requests':
            self.request_date = timezone.now()  # Устанавливаем дату для заявки

        elif new_status == 'in_store':
            self.arrival_date = timezone.now()  # Устанавливаем дату прихода товара

        elif new_status == 'sold':
            self.sale_date = timezone.now()  # Устанавливаем дату продажи товара

        elif new_status == 'returned':
            self.return_date = timezone.now()  # Устанавливаем дату возврата товара

        self.save()

    class Meta:
        verbose_name = "Карточка товара"
        verbose_name_plural = "Карточки товаров"
