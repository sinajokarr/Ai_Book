from decimal import Decimal, ROUND_HALF_UP
from django.utils.text import slugify
from rest_framework import serializers
from .models import (
    Category,
    Customer,
    Product,
    CartItem,
    Comment,
    Cart,
    Discount,
    Address,
    OrderItem,
)


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    in_stock_count = serializers.IntegerField(read_only=True)
    max_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True, read_only=True
    )
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True, read_only=True
    )
    avg_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True, read_only=True
    )
    cheapest_product_id = serializers.IntegerField(read_only=True)
    priciest_product_id = serializers.IntegerField(read_only=True)
    has_stock = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "description",
            "product_count",
            "in_stock_count",
            "min_price",
            "max_price",
            "avg_price",
            "cheapest_product_id",
            "priciest_product_id",
            "has_stock",
            "price_range",
        ]

    def get_has_stock(self, obj):
        return (getattr(obj, "in_stock_count", 0) or 0) > 0

    def get_price_range(self, obj):
        if getattr(obj, "min_price", None) is None or getattr(obj, "max_price", None) is None:
            return None
        return f"{obj.min_price} – {obj.max_price}"


class ProductSerializer(serializers.ModelSerializer):
    tax = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    best_discount_percent = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True, required=False
    )
    approved_comments_count = serializers.IntegerField(
        read_only=True, required=False
    )
    total_sold = serializers.IntegerField(
        read_only=True, required=False
    )

    short_description = serializers.SerializerMethodField()
    category_title = serializers.CharField(source="category.title", read_only=True)
    is_in_stock = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField() # New field

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",        
            "short_description",  
            "unit_price",
            "category",
            "category_title",     
            "inventory",
            "is_in_stock",
            "slug",
            "tax",
            "best_discount_percent",
            "approved_comments_count",
            "total_sold",
            "final_price", # Added
        ]

    def get_tax(self, obj):
        if obj.unit_price is None:
            return None
        return (
            Decimal(obj.unit_price) * Decimal("0.10")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_final_price(self, obj):
        price = obj.unit_price or Decimal(0)
        # Use getattr() to safely access the annotated field
        discount_pct = getattr(obj, "best_discount_percent", Decimal(0))
        final = price * (Decimal("1") - (discount_pct / Decimal("100")))
        return final.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_short_description(self, obj):
        if not obj.description:
            return ""
        text = str(obj.description).strip()
        if len(text) <= 120:
            return text
        return text[:117].rstrip() + "..."

    def get_is_in_stock(self, obj):
        try:
            return int(obj.inventory or 0) > 0
        except Exception:
            return False

    def validate(self, data):
        name = data.get("name")
        if name is not None and len(name) < 6:
            raise serializers.ValidationError({"name": "must be at least 6 characters"})
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name or "")
        product.save()
        return product

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if "name" in validated_data:
            instance.slug = slugify(instance.name or "")
        instance.save()
        return instance


class DiscountSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    application_count = serializers.IntegerField(read_only=True)
    discounted_price_preview = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = [
            "id",
            "discount",
            "description",
            "label",
            "application_count",
            "discounted_price_preview",
        ]

    def validate_discount(self, value):
        if value is None:
            raise serializers.ValidationError("Discount percent is required")
        try:
            v = float(value)
        except Exception:
            raise serializers.ValidationError("Discount percent must be a number")
        if not (0 < v < 100):
            raise serializers.ValidationError("Discount percent must be between 0 and 100")
        return value

    def get_label(self, obj):
        p = obj.discount or 0
        try:
            f = float(p)
        except Exception:
            f = 0.0
        if f.is_integer():
            return f"-{int(f)}%"
        return f"-{f:.1f}%"

    def get_discounted_price_preview(self, obj):
        request = self.context.get("request")
        base = request.query_params.get("base_price") if request else None
        if not base:
            return None
        try:
            base_dec = Decimal(str(base))
        except Exception:
            return None
        pct = Decimal(str(obj.discount or 0)) / Decimal("100")
        final = (base_dec * (Decimal("1") - pct)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return str(final)


class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "birth_date",
            "full_name",
        ]

    def get_full_name(self, obj):
        fn = obj.first_name or ""
        ln = obj.last_name or ""
        return f"{fn} {ln}".strip()


class AddressSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Address
        fields = ["id", "customer", "city", "province", "street"]

    def validate(self, attrs):
        customer = attrs.get("customer") or getattr(self.instance, "customer", None)
        if customer:
            exists = Address.objects.filter(customer=customer).exclude(
                pk=getattr(self.instance, "pk", None)
            ).exists()
            if exists:
                raise serializers.ValidationError(
                    {"customer": "An address for this customer already exists."}
                )
        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "unit_price"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "product", "name", "body", "datetime_created", "status"]


# Simple Product Serializer for embedding in CartItem
class SimpleProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "unit_price", "final_price"]
    
    def get_final_price(self, obj):
        # NOTE: This assumes the Product instance passed has 'best_discount_percent' annotated, 
        # which is usually done in the CartItem's queryset if needed for accurate price calculation
        price = obj.unit_price or Decimal(0)
        discount_pct = getattr(obj, "best_discount_percent", Decimal(0))
        final = price * (Decimal("1") - (discount_pct / Decimal("100")))
        return final.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "cart", "quantity", "total_price"]
        read_only_fields = ["cart"]

    def get_total_price(self, obj):
        # Assuming the product instance here has the final_price logic applied (via annotation in CartViewSet)
        unit_price = getattr(obj.product, "final_price", obj.product.unit_price)
        if unit_price is None:
            return Decimal("0.00")
        return (unit_price * obj.quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True) 
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "created_at", "items", "total_price", "total_items"]
        read_only_fields = ["created_at"]
    
    def get_total_price(self, obj):
        # Calculate total price by summing up the calculated total_price of all items
        total = sum([item.get_total_price(item) for item in obj.items.all()], Decimal(0))
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_total_items(self, obj):
        # Calculate total quantity of items
        return sum([item.quantity for item in obj.items.all()])