from django.contrib import admin
from store.models import Book, Category
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('book_title',)}
admin.site.register(Book, BookAdmin)



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
admin.site.register(Category, CategoryAdmin)
    

    
 