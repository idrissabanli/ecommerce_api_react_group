from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from products.models import Category, Product, Order
from products.apis.serializers import CategorySerializer, ProductRetrieveSerializer, ProductCreateSerializer, OrderSerializer, OrderRetrieveSerializer
from rest_framework import permissions
from url_filter.integrations.drf import DjangoFilterBackend

class IsAuthenticatedForCreate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return super(IsAuthenticatedForCreate, self).has_permission(request, view)

class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedForCreate,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedForCreate,]
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['category',]
    serializer_classes = {
        'list': ProductRetrieveSerializer,
        'retrieve': ProductRetrieveSerializer,
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

class OwnProductsAPIView(ReadOnlyModelViewSet):
    serializer_class = ProductRetrieveSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
        
