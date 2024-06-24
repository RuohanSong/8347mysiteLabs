from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path('about/', views.about_view, name='about'),  # myapp/about page for lab 5
]