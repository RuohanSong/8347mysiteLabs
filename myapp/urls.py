from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    # path(r'', views.about_view, name='about6'), # for lab6 evaluation
    path('about/', views.about_view, name='about'),  # myapp/about page for lab 5
    path('<int:book_id>/', views.detail_view, name='detail'),
    path('feedback', views.getFeedback, name='feedback1'),
    path('findbooks', views.findbooks, name='findbooks'),
    path('place_order', views.place_order, name='placeorder'),
    path('review', views.review, name='review'),
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('chk_reviews/<int:book_id>/', views.chk_reviews, name='chk-reviews')
]
