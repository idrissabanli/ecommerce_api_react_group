from rest_framework import serializers
from accounts.serializers import UserCreateSerializer
from products.models import Category, Product, Order, BasKet
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'icon_svg', 'icon_png', 'created_at']

class ProductRetrieveSerializer(serializers.ModelSerializer):
    owner = UserCreateSerializer()
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'owner', 'description', 'price', 'discount_price', 'amount_by_unit', 'unit', 'main_image',  'created_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'owner', 'description', 'price', 'discount_price', 'amount_by_unit', 'unit', 'main_image',  'created_at']

    def validate(self, data):
        request = self.context.get('request')
        data['owner'] = request.user
        attrs = super().validate(data)
        if data.get('discount_price') and float(data['discount_price']) > float(data['price']):
            raise ValidationError("Discount price must be small than price")
        return attrs


class ProductUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    main_image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'owner', 'description', 'price', 'discount_price', 'amount_by_unit', 'unit', 'main_image',  'created_at']

    def validate(self, data):
        request = self.context.get('request')
        data['owner'] = request.user
        attrs = super().validate(data)
        if data.get('discount_price') and float(data['discount_price']) > float(data['price']):
            raise ValidationError("Discount price must be small than price")
        return attrs

class OrderRetrieveSerializer(serializers.ModelSerializer):
    product = ProductRetrieveSerializer()
    customer = UserCreateSerializer()

    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'count', 'created_at']



class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'count', 'created_at']
    
    def validate(self, data):
        request = self.context.get('request')
        data['customer'] = request.user
        return super().validate(data)


class BasKetRetrieveSerializer(serializers.ModelSerializer):
    product = ProductRetrieveSerializer()
    customer = UserCreateSerializer()

    class Meta:
        model = BasKet
        fields = ['id', 'product', 'customer', 'count', 'created_at']


class BasKetSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = BasKet
        fields = ['id', 'product', 'customer', 'count', 'created_at']
    
    def validate(self, data):
        request = self.context.get('request')
        data['customer'] = request.user
        return super().validate(data)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product = validated_data['product']
        instance = BasKet.objects.filter(customer=user, product=product).first()
        if instance:
            instance.count = validated_data['count']
            instance.save()
        else:
            instance = super().create(validated_data)
        return instance
            
        