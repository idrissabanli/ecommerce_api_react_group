from rest_framework.routers import DefaultRouter
from .viewsets import CategoryViewSet, ProductViewSet, OrderViewSet
router = DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)