from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from products.models import Category, Product, Order, BasKet
from products.apis.serializers import CategorySerializer, ProductRetrieveSerializer, ProductCreateSerializer, OrderSerializer, OrderRetrieveSerializer, BasKetRetrieveSerializer, BasKetSerializer, ProductUpdateSerializer
from rest_framework import permissions
from products.apis.pagination import CustomPageNumberPaginationWithPageNumber
from url_filter.integrations.drf import DjangoFilterBackend
from accounts.utils import CustomSwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.pagination import _positive_int
from rest_framework import filters

class IsAuthenticatedForCreate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return super(IsAuthenticatedForCreate, self).has_permission(request, view)


class MultiSerializerViewSet(ModelViewSet):
    serializers = {
        'default': None,
    }
    result_keyword = ""
    limit_query_param = 'limit'
    max_limit = None

    def get_limit(self):
        if self.limit_query_param:
            try:
                return _positive_int(
                    self.request.query_params[self.limit_query_param],
                    strict=True,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                return None
        return None

    def get_queryset(self):
        queryset = super(MultiSerializerViewSet, self).get_queryset()
        limit = self.get_limit()
        if limit:
            queryset = queryset[:limit]
        return queryset

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['default'])

    def get_paginated_response_with_result_keyword(self, data, result_keyword):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        if 'get_paginated_response_with_result_keyword' in dir(self.paginator):
            return self.paginator.get_paginated_response_with_result_keyword(data, self.result_keyword)
        return self.get_paginated_response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if self.result_keyword:
                return self.get_paginated_response_with_result_keyword(serializer.data, self.result_keyword)
            else:
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if self.result_keyword:
            return Response({self.result_keyword: serializer.data})
        return Response(serializer.data)



class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedForCreate,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def get(self, *args, **kwargs):
    #     return super().get(self, *args, **kwargs)

    # def post(self, *args, **kwargs):
    #     return super().post(self, *args, **kwargs)



class ProductViewSet(MultiSerializerViewSet):
    permission_classes = [IsAuthenticatedForCreate,]
    pagination_class = CustomPageNumberPaginationWithPageNumber
    queryset = Product.objects.all()
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ['category',]
    result_keyword = "products"
    serializers = {
        'list': ProductRetrieveSerializer,
        'retrieve': ProductRetrieveSerializer,
        'update': ProductUpdateSerializer,
        'partial_update': ProductUpdateSerializer,
        'default': ProductCreateSerializer
    }


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
    http_method_names = ("get", "post", "delete", "options")

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
    
        
