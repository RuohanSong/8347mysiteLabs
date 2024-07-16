from django.contrib import admin
from django.contrib.auth.models import User

from .models import *

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Order)
admin.site.register(Review)