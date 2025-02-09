from django.db import models
from django.contrib.auth.models import User
from store.models import Book
# Create your models here.
class Order(models.Model):

    # ORDER_STATUS = (
    #     ('Pending', 'Pending'),
    #     ('Completed', 'Completed'),
    #     ('Cancelled', 'Cancelled'),
    # )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    # status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Pending')
    def __str__(self):
        return f'Order {self.transaction_id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.book.book_title