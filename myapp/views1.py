from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Publisher, Book, Member, Order

def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('id')[:10]
    publisherlist = Publisher.objects.all().order_by('city')[:5:-1]
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    heading2 = '<p>' + 'List of available publishers: ' + '</p>'
    response.write(heading2)
    for publisher in publisherlist:
        para = '<p>' + str(publisher.id) + ': ' + str(publisher.name) + ' - ' + str(publisher.city) + '</p>'
        response.write(para)
    return response

def about(request):
    response = HttpResponse()
    about_content = '<p>' + 'This is an eBook APP.' + '</p>'
    response.write(about_content)
    return response

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # book = Book.objects.get(pk=book_id)
    response = HttpResponse()

    book_detail = f'<p>Book Title : {book.title.upper()}</p>'
    response.write(book_detail)
    book_detail = f'<p>Price : ${book.price}</p>'
    response.write(book_detail)
    book_detail = f'<p>Publisher: {book.publisher.name}</p>'
    response.write(book_detail)
    return response
