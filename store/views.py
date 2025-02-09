from django.shortcuts import render
from store.models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.db.models import Q
# Create your views here.
def store(request):
    books = Book.objects.all().order_by('-created_date')
    paginator = Paginator(books, 4)
    paged_books = paginator.get_page(request.GET.get('page'))
    context = {
        'books': paged_books
    }
    return render(request, 'shop-list.html', context)   

def book_detail(request, category_slug, book_slug):
    try:
        single_book = Book.objects.get(category__slug=category_slug, slug=book_slug)
    except Exception as e:
        raise e
    context = {
        'single_book': single_book
    }
    return render(request, 'shop-product-detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            books = Book.objects.order_by('-created_date').filter(Q(book_title__icontains=keyword) | Q(description__icontains=keyword))
            book_count = books.count()
            context = {
                'books': books,
                'book_count': book_count
            }
            return render(request, 'shop-list.html', context)
    
    return render(request, 'shop-list.html')

