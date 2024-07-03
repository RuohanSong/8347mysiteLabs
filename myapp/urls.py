from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    # path(r'', views.about_view, name='about6'), # for lab6 evaluation
    path('', views.index, name='index'),
    path('about/', views.about_view, name='about'),
    path('<int:book_id>/', views.detail_view, name='detail'),
    path('feedback/', views.getFeedback, name='feedback'),
    path('findbooks/', views.findbooks, name='findbooks'),
    path('place_order/', views.place_order, name='place_order'),
    path('review/', views.review, name='review'),
]