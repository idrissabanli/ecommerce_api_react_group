from rest_framework import serializers
from accounts.serializers import UserCreateSerializer
from products.models import Category, Product, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'icon_svg', 'icon_png', 'created_at']

class ProductRetrieveSerializer(serializers.ModelSerializer):
    owner = UserCreateSerializer()
    class Meta:
        model = Product
        fields = ['id', 'title', 'owner', 'description', 'price', 'discount_price', 'amount_by_unit', 'unit', 'main_image',  'created_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'owner', 'description', 'price', 'discount_price', 'amount_by_unit', 'unit', 'main_image',  'created_at']

    def validate(self, data):
        request = self.context.get('request')
        data['owner'] = request.user
        return super().validate(data)

class OrderRetrieveSerializer(serializers.ModelSerializer):
    product = ProductRetrieveSerializer()
    customer = UserCreateSerializer()

    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'count', 'created_at']



class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'count', 'created_at']
    
    def validate(self, data):
        request = self.context.get('request')
        data['customer'] = request.user
        return super().validate(data)





        