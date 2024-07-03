from django.contrib import admin
from .models import Publisher, Book, Member, Order

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('books',)

admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Order, OrderAdmin)
