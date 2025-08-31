from itertools import product

from django.template.context_processors import request
from django.template.defaultfilters import slugify
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from decimal import Decimal
from .models import Category,Customer,Product,CartItem,Comment,Cart,Discount,Address,OrderItem,Order


class CategorySerializer(serializers.ModelSerializer):
    product_count=serializers.IntegerField(read_only=True)
    in_stock_count=serializers.IntegerField(read_only=True)
    max_price= serializers.DecimalField(max_digits=10,decimal_places=2,allow_null=True)
    min_price=serializers.DecimalField(max_digits=10,decimal_places=2,allow_null=True)
    avg_price=serializers.DecimalField(max_digits=10,decimal_places=2,allow_null=True)

    cheapest_product_id=serializers.IntegerField(read_only=True)
    priciest_product_id=serializers.IntegerField(read_only=True)


    has_stock=serializers.SerializerMethodField()
    price_range=serializers.SerializerMethodField()

    num_of_product=serializers.IntegerField(source="product.count",read_only=True)
    class Meta :
        model = Category
        fields =  [
            "id", "title", "description",
            "product_count", "in_stock_count",
            "min_price", "max_price", "avg_price",
            "cheapest_product_id", "priciest_product_id",
              "has_stock", "price_range",
        ]

        def get_has_stock(self, obj):
            return (obj.in_stock_count or 0) > 0

        def get_price_range(self, obj):
            if obj.min_price is None or obj.max_price is None:
                return None
            return f"{obj.min_price} – {obj.max_price}"

class ProductSerializer(serializers.ModelSerializer):
    name= serializers.CharField(max_length=255)
    unit_price=serializers.DecimalField(max_digits=3,decimal_places=1)
    tax =serializers.SerializerMethodField()
    slug=serializers.SlugField(read_only=True)
    class Meta :
        model = Product
        fields = ["id", "name", "unit_price", "category", "inventory", "tax", "slug"]
    def get_tax (self,Product):
        return Product.unit_price*Decimal(0.1)
    def validate(self,data):
        if len(data["name"])<6:
            raise serializers.ValidationError("true")
        return data


    def create(self, validated_data):
        product=Product(**validated_data)
        product.slug=slugify(product.name)
        product.save()
        return product





class DiscountSerializer(serializers.ModelSerializer):
    label =serializers.SerializerMethodField()
    applied_products_count=serializers.SerializerMethodField(read_only=True)
    discount_price_preview= serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ['id','discounts', 'description',"label","applied_products_count","discount_price_preview"]
    def validate_discount(self,value):
        if value is None :
            raise serializers.ValidationError("Discount percent is required")
        if not (0 < value<100):
            raise serializers.ValidationError("Discount percent must be between 0 and 100")
        return value


    def get_label(self, obj):
        p = obj.discount or 0
        return f"-{p:.1f}%" if (p % 1) else f"-{int(p)}%"


    def get_discounted_price_preview(self,obj):
        request =self.context.get("request")
        base =request.query_params.get("base_price") if  request else None
        if not base :
            return None
        try:
            base_dec= Decimal(str(base))
        except Exception:
            return None
        pct = Decimal(str(obj.discount  or 0 )) / Decimal("100 ")
        final = (base_dec * (Decimal("1") - pct)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return str(final)


class CustomerSerializer(serializers,ModelSerializer):
    full_name= serializers.SerializerMethodField()
    class Meta:
       model =Customer
       fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'birth_date','full_name']

    def get_full_name(self,obj):
        return f"{obj.first_name} {obj.last_name}".strip()



class AddressSerializer(serializers,ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta :
        model = Address
        fields =['customer','city','province','street']
    def validate(self, attrs):
        customer=attrs.get("customer")or getattr(self.instance,"customer",None)
        if customer:
            exists = Address.objects.filter(customer=customer).exclude(pk=getattr(self.instance, 'pk', None)).exists()
            if exists:
                raise serializers.ValidationError({'customer': 'An address for this customer already exists.'})
            return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']


class CommentSerializer(serializers.ModelSerializer):
    class Meta :
        model = Comment
        fields = ['id','product','name','body','datetime_created','status']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta :
        model = CartItem
        fields = ['id','product','cart','quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta :
        model = Cart
        fields = ["id", "created_at", "items"]
        read_only_fields = ["created_at"]

