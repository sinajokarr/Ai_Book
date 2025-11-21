from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import CategoryViewSet, ProductViewSet, DiscountViewSet, CommentViewSet, CartViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"discounts", DiscountViewSet, basename="discount")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"carts", CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]