from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from products.models import Category, Product, Order, BasKet
from products.apis.serializers import (
    CategorySerializer, CategoryRetrieveSerializer,
    ProductRetrieveSerializer, ProductCreateSerializer, OrderSerializer, 
    OrderRetrieveSerializer, BasKetRetrieveSerializer, BasKetSerializer, ProductUpdateSerializer
)
from rest_framework import permissions, filters
from url_filter.integrations.drf import DjangoFilterBackend
from accounts.utils import CustomSwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator


class IsAuthenticatedForCreate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return super(IsAuthenticatedForCreate, self).has_permission(request, view)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedForCreate,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    serializer_classes = {
        'retrieve': CategoryRetrieveSerializer,
        'default': CategorySerializer
    }

    # def get(self, *args, **kwargs):
    #     return super().get(self, *args, **kwargs)

    # def post(self, *args, **kwargs):
    #     return super().post(self, *args, **kwargs)



class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedForCreate,]
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category',]
    search_fields = ['title__icontains', 'category__title__icontains']
    serializer_classes = {
        'list': ProductRetrieveSerializer,
        'retrieve': ProductRetrieveSerializer,
        'update': ProductUpdateSerializer,
        'partial_update': ProductUpdateSerializer,
        'default': ProductCreateSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action,self.serializer_classes.get('default'))

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_classes = {
        'list': OrderRetrieveSerializer,
        'retrieve': OrderRetrieveSerializer,
        'default': OrderSerializer
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes.get('default'))

    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user)


class BasKetViewSet(ModelViewSet):
    queryset = BasKet.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_classes = {
        'list': BasKetRetrieveSerializer,
        'retrieve': BasKetRetrieveSerializer,
        'default': BasKetSerializer
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_classes.get('default'))

    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user)

class OwnProductsAPIView(ReadOnlyModelViewSet):
    serializer_class = ProductRetrieveSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['category',]
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
        
