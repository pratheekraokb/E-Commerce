from django.contrib import admin
from .models import (
    CustomUser, Product, Category, Subcategory, Tag, ProductTag, Company,
    Cart, CartItem, Order, OrderItem, OrderTracking, Address, Comment, ProductImage
)

# Register your models here.

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_of_birth')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'mrp_price', 'selling_price', 'stock_quantity','company')
    list_filter = ('company','category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('product', 'tag')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'calculate_subtotal')
    def calculate_subtotal(self, obj):
        return obj.calculate_subtotal()  
    calculate_subtotal.short_description = 'Subtotal'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total_amount', 'status', 'transaction_id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'subtotal')

@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('order', 'status_date', 'location')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'city', 'state', 'Zip_code', 'country')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'timestamp')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

