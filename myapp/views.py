from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from myapp.models import Book, Publisher, Member, Order, Review
from .forms import FeedbackForm, SearchForm, ReviewForm
from django.shortcuts import render, redirect
from myapp.forms import OrderForm


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})


def about_view(request):
    return render(request, 'myapp/about.html')


#for lab6 evaluation:
# def about_view(request):
#     booklist = Book.objects.all().order_by('id')[:10]
#     return render(request, 'myapp/about.html', {'booklist': booklist})

def detail_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {'book': book}
    return render(request, 'myapp/detail.html', context)


def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            choices = []
            if 'B' in feedback:
                choices.append('borrow books')
            if 'P' in feedback:
                choices.append('purchase books')
            if not choices:
                choices.append('None of the options')
            return render(request, 'myapp/fb_results.html', {'choices': choices})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})




def findbooks(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        return render(request, 'myapp/findbooks.html', {'form': form})
    elif request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']

            if category:
                booklist = Book.objects.filter(category=category, price__lte=max_price)
            else:
                booklist = Book.objects.filter(price__lte=max_price)

            context = {
                'name': name,
                'category': category,
                'booklist': booklist
            }
            return render(request, 'myapp/results.html', context)
        else:
            return HttpResponse('Invalid data')

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()
            order.books.set(books)
            if type == 1:
                for b in books:
                    member.borrowed_books.add(b)
            return render(request, 'myapp/order_response.html', {'books': books, 'order':order})
        else:
            return render(request, 'myapp/placeorder.html', {'form':form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form':form})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save()
                book = review.book
                book.num_reviews += 1
                book.save()
                return redirect('index')  # Redirect to the main page
            else:
                form.add_error('rating', 'You must enter a rating between 1 and 5!')
        return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})
