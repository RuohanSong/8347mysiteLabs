import random
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect

from myapp.models import *
from . import models
from .forms import FeedbackForm, SearchForm, OrderForm, ReviewForm


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    last_login = request.session.get('last_login')
    if last_login:
        message = f"Your last login was: {last_login}"
    else:
        message = "Your last login was more than one hour ago."
    return render(request, 'myapp/index.html', {'booklist': booklist, 'message': message})


def about_view(request):
    lucky_num = request.COOKIES.get('lucky_num')
    if lucky_num:
        mynum = int(lucky_num)
    else:
        mynum = random.randint(1, 100)

    response = render(request, 'myapp/about.html', {'mynum': mynum})
    expires = timezone.now() + timedelta(minutes=5)
    response.set_cookie('lucky_num', mynum, expires=expires)
    return response


# for lab6 evaluation:
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
            feedbacks = form.cleaned_data['feedback']
            return render(request, 'myapp/fb_results.html', {'feedbacks': feedbacks})
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
            min_price = form.cleaned_data['min_price']

            if category:
                booklist = Book.objects.filter(category=category, price__lte=max_price, price__gte=min_price)
            else:
                booklist = Book.objects.filter(price__lte=max_price, price__gte=min_price)

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
            order = form.save(commit=False)
            order.save()

            books = form.cleaned_data['books']
            order.books.set(books)
            member = order.member
            type = order.order_type
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save(commit=False)
                review.save()

                book = form.cleaned_data['book']
                book.num_reviews += 1
                book.save()
                return redirect('myapp:index')
            else:
                return render(request, 'myapp/review.html',
                              {'form': form, 'error_message': 'You must enter a rating between 1 and 5!'})
        else:
            return render(request, 'myapp/review.html',
                          {'form': form, 'error_message': 'The information you provided is invalid!'})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"{username} logging in with password {password}")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(timezone.now())
                request.session.set_expiry(3600)    # 1 hour
                return redirect('myapp:index')
            else:
                return HttpResponse('Your account is disabled.')
        else:
            message = "Invalid username or password"
            return render(request, 'myapp/login.html', {'message': message})
    else:
        return render(request, 'myapp/login.html')


@login_required(login_url='/myapp/login')
def user_logout(request):
    logout(request)
    return redirect('myapp:index')


# @login_required(login_url='/myapp/login')
def chk_reviews(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    if isinstance(user, Member):
        reviews = Review.objects.filter(book=book)
        if reviews.exists():
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            message = f'The average rating for {book.title} is {avg_rating:.2f}.'
        else:
            message = 'No reviews yet'
    else:
        # message = 'You are not a registered member.'
        # messages.warning(request, message)
        # return redirect('myapp:user-login')
        return HttpResponse('You are not a registered member.')

    context = {
        'book': book,
        'message': message
    }
    return render(request, 'myapp/chk_reviews.html', context)
