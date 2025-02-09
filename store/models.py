from django.db import models
from django.urls import reverse
# Create your models here.
class Book(models.Model):
    book_title = models.TextField(max_length=255, unique=True)
    author = models.TextField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=255, blank=True)
    images = models.ImageField(upload_to='photos/books')
    stock = models.IntegerField()
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_data = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.book_title

    def get_url(self):
        return reverse('book_detail', args=[self.category.slug, self.slug])
    
class Category(models.Model):
    category_name = models.TextField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=True, blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.category_name