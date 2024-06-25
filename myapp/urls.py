from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    # path(r'', views.about_view, name='about6'), # for lab6 evaluation
    path('about/', views.about_view, name='about'),  # myapp/about page for lab 5
    path('<int:book_id>/', views.detail_view, name='detail'),
    path('feedback', views.getFeedback, name='feedback1'),
]