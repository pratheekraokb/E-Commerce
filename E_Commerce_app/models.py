from django.db import models
from django.utils import timezone

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)  # Store hashed passwords
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    profile_image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = 'User'

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')  # Specify the upload path

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Product'
    
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Category'
    
class Subcategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Subcategory'

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Tag'

class ProductTag(models.Model):
    product_tag_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    class Meta:
        db_table = 'ProductTag'

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Company'

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    def __str__(self):
        return f"Cart {self.cart_id} - User: {self.user.username}"
    def calculate_total(self):
        cart_items = CartItem.objects.filter(cart=self)
        total = sum(item.subtotal for item in cart_items)
        return total
    class Meta:
        db_table = 'Cart'

class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"CartItem {self.cart_item_id} - Product: {self.product.name}"

    def calculate_subtotal(self):
        return self.product.selling_price * self.quantity

    class Meta:
        db_table = 'CartItem'

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return f"Order {self.order_id} - User: {self.user.username}"
    def update_status(self, new_status):
        self.status = new_status
        self.save()
    class Meta:
        db_table = 'Order'

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem {self.order_item_id} - Product: {self.product.name}"

    def calculate_subtotal(self):
        return self.product.selling_price * self.quantity
    class Meta:
        db_table = 'OrderItem'

class OrderTracking(models.Model):
    tracking_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status_date = models.DateTimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"OrderTracking {self.tracking_id} - Order: {self.order.order_id}"

    def update_location(self, new_location):
        self.location = new_location
        self.save()
    class Meta:
        db_table = 'OrderTracking'

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    Zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"Address {self.address_id} - User: {self.user.username}"
    class Meta:
        db_table = 'Address'

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Comment {self.comment_id} - User: {self.user.username}"

    def add_reply(self, user, text):
        reply = Comment.objects.create(
            user=user,
            product=self.product,
            parent_comment=self,
            text=text,
            timestamp=timezone.now()
        )
        return reply
    class Meta:
        db_table = 'Comment'

class ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"ProductImage {self.image_id} - Product: {self.product.name}"
    class Meta:
        db_table = 'ProductImage'

