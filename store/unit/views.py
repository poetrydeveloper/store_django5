# views.py в приложении sales
from django.shortcuts import render
from .models import Product, Preorder, UnitProduct


def create_preorder(request, product_id, quantity, price):
    product = Product.objects.get(id=product_id)

    # Создаем предварительную заявку
    preorder = Preorder.objects.create(product=product, quantity=quantity)

    # Создаем unitProduct для отслеживания товара
    unit_product = UnitProduct.objects.create(
        product=product,
        status='preorder',
        preorder_price=price,
        preorder_date=timezone.now()
    )

    return HttpResponse(f"Товар {product.name} добавлен в предварительную заявку.")
