from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from myapp.models import Book, Publisher, Member, Order
from .forms import FeedbackForm


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
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else:
                choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice': choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})
