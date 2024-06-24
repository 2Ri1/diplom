from django.contrib import admin
from .models import Product, Category, Shop, CustomUser, ProductInfo, Contact, Order

# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(CustomUser)
admin.site.register(ProductInfo)
admin.site.register(Contact)
admin.site.register(Order)