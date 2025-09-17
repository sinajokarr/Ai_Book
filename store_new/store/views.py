from itertools import product, count
from django.template.context_processors import request
from rest_framework.decorators import permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from config.wsgi import application
from .models import Product, Order, Comment,Cart,Category,Customer,         artItem,Discount
from django.db.models import Count, Min, Max, Avg, Q, OuterRef, Subquery,Sum
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from .models import Product, Category
from .serializers import CategorySerializer, ProductSerializer, DiscountSerializer, CommentSerializer, CartSerializer
from decimal import Decimal
from django.db.models.functions import Coalesce



class CategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet,ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):

        cheapest_id = Subquery(
            Product.objects
                   .filter(category=OuterRef('pk'))
                   .order_by('unit_price')
                   .values('id')[:1]
        )
        priciest_id = Subquery(
            Product.objects
                   .filter(category=OuterRef('pk'))
                   .order_by('-unit_price')
                   .values('id')[:1]
        )

        return (
            Category.objects
            .select_related('top_product')
            .annotate(
                product_count=Count('products', distinct=True),
                in_stock_count=Count(
                    'products',
                    filter=Q(products__inventory__gt=0),
                    distinct=True
                ),
                min_price=Min('products__unit_price'),
                max_price=Max('products__unit_price'),
                avg_price=Avg('products__unit_price'),
                cheapest_product_id=cheapest_id,
                priciest_product_id=priciest_id,
            )
        )

class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self):
        return (
            Product.objects
            .select_related("category")
            .prefetch_related("discounts")
            .annotate(
                best_discount_percent=Coalesce(Max("discounts__discount"), 0.0),

                approved_comments_count=Count(
                    "comments",
                    filter=Q(comments__status=Comment.COMMENT_STATUS_APPROVED),
                    distinct=True
                ),


                total_sold=Coalesce(Sum(
                    "order_items__quantity",
                    filter=Q(order_items__order__status=Order.ORDER_STATUS_PAID)
                ), 0),
            )
        )

class DiscountViewSet(ReadOnlyModelViewSet):
    serializer_class = DiscountSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ["description"]
    ordering_fields = ["discount","applied_product_count"]
    ordering = ["discount"]


    def get_queryset(self):
        return Discount.objects.annotate(application_count=Count("product",distinct=True))



class CommentViewSet(ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_field = ["name","body"]
    ordering = ["-datetime_created"]


    def perform_create(self, serializer):
        serializer.save(status=Comment.COMMENT_STATUS_WAITING)

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])

    def approve(self,request,pk= None):
        obj = self.get_object()
        obj.status = Comment.COMMENT_STATUS_APPROVED
        obj.save(update_fields=["status"])
        return Response({"detail":"approved"})

    @action(detail=True , methods=["post"],Permission_classes =[IsAdminUser])

    def reject(self, request , pk=None ):
        obj = self.get_object()
        obj.status = Comment.COMMENT_STATUS_NOT_APPROVED
        obj.save(update_fields=["status"])
        return Response({"detail":"rejected"})

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related("items__product")
    serializer_class = CategorySerializer

    @action(detail=True,methods=["post"])
    def add_item( self, request , pk = None):
        cart=self.get_object()
        product_id = request.data.get("product_id")
        quantity = int(request.data.get ("quantity", 1 ))
        if quantity <=0 :
            return Response({"detail":"quantity must be >0 "}, status=400)

        product = get_object_or_404(Product , pk = product_id)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        if not created:
            item.quantity = F("quantity")+ quantity
            item.save(update_fields=["quantity"])
            item.refresh_from_db()
        return Response(CartSerializer(cart, context={"request": request}).data, status=200)
