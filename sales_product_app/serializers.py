from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Shop, Category, CustomUser, ProductInfo, Product, Parameter, ProductParameter, Order, Contact


class CustomUserSerializer(UserCreateSerializer):
    thumbnail = serializers.ImageField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name',
                  'company', 'position', 'type', 'thumbnail')


class ShopSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    is_active = serializers.BooleanField()

    class Meta:
        model = Shop
        fields = ('id', 'name', 'url', 'is_active')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(view_name="product-detail")

    class Meta:
        model = Product
        fields = ('url', 'name', 'category')


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('name',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')


class ProductInfoSerializer(serializers.HyperlinkedModelSerializer):
    shop = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    basket = serializers.BooleanField(required=True)
    quantity = serializers.IntegerField(required=False)
    retail_price = serializers.IntegerField(required=False)
    product_parameter = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'product_id', 'product', 'shop', 'quantity', 'retail_price',  'basket', 'thumbnail',
                  'product_parameter')


class BasketSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    shop = serializers.CharField(read_only=True)
    price = serializers.IntegerField(min_value=0, read_only=True)
    quantity_in_stock = serializers.IntegerField(read_only=True)
    sum_value = serializers.IntegerField(min_value=0, read_only=True)
    quantity = serializers.IntegerField(required=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'shop', 'price', 'quantity_in_stock', 'quantity', 'sum_value')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ThanksForOrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    name = serializers.CharField(read_only=True)
    shop = serializers.CharField(read_only=True)
    price = serializers.IntegerField(min_value=0, read_only=True)
    sum_value = serializers.IntegerField(min_value=0, read_only=True)
    email = serializers.EmailField()
    phone = serializers.CharField(read_only=True)
    street = serializers.CharField(read_only=True)
    house = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'shop', 'price', 'quantity', 'sum_value', 'user', 'email', 'phone', 'street', 'house')


class OrderListSerializer(serializers.ModelSerializer):
    sum_ = serializers.IntegerField(min_value=0)

    class Meta:
        model = Order
        fields = ('order_number', 'user_id', 'date', 'sum_', 'status',)


class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    name = serializers.CharField(read_only=True)
    shop = serializers.CharField(read_only=True)
    price = serializers.IntegerField(min_value=0, read_only=True)
    sum_ = serializers.IntegerField(min_value=0, read_only=True)
    email = serializers.EmailField(read_only=True)
    phone = serializers.CharField(read_only=True)
    street = serializers.CharField(read_only=True)
    house = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('order_number', 'date', 'status', 'name', 'shop', 'price', 'quantity',
                  'sum_', 'user', 'email', 'phone', 'street', 'house')