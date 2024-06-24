"""
URL configuration for REST_API_DIPLOM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.conf import settings


from sales_product_app.views import ShopView, CategoryView, ProductInfoView, ProductViewSet, BasketView, \
    account_activation, ContactView, ThanksForOrderView, OrderListView, ShopUpdateUserView, SupplierOrdersView, \
    UserView
router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
print(router)

app_name = 'sales_product_app'
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^auth/', include('djoser.urls.authtoken'), name='token-login-logout'),
    path('activate/<str:uid>/<str:token>/', account_activation, name='account_activation_success'),
    path('api/v1/', include('djoser.urls'), name='user-create-password-reset'),
    path('api/v1/', include(router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api/v1/users-list/', UserView.as_view(), name='users-list'),
    # path('api/v1/users-create/', UserView.as_view(), name='create-user'),
    path('api/v1/shops/', ShopView.as_view(), name='shops-list'),
    path('api/v1/shops/<int:pk>/', ShopView.as_view(), name='shop-status-update'),
    path('api/v1/categories/', CategoryView.as_view(), name='category-list'),
    path('api/v1/products/<int:product_id>/detail/', ProductInfoView.as_view(), name='productinfo-detail'),
    path('api/v1/basket/', BasketView.as_view(), name='basket'),
    path('api/v1/basket/<int:pk>/', BasketView.as_view(), name='order-update'),
    path('api/v1/contact/', ContactView.as_view(), name='contact'),
    path('api/v1/contact/<int:pk>/', ContactView.as_view(), name='contact-detail'),
    path('api/v1/thanks-for-order/', ThanksForOrderView.as_view(), name='thanks-for-order'),
    path('api/v1/orders/', OrderListView.as_view(), name='orders'),
    path('api/v1/orders/<str:order_number>/', OrderListView.as_view(), name='order-detail'),
    path('api/v1/shops-update-user/', ShopUpdateUserView.as_view(), name='supplier-status-update'),
    path('api/v1/supplier-orders/', SupplierOrdersView.as_view(), name='supplier-orders'),
    path('api/v1/supplier-orders/<str:order_number>/', SupplierOrdersView.as_view(), name='supplier-orders-detail'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)