from django import forms
from .models import *

class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)

class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label='Your Name'
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label='Select a category'
    )
    max_price = forms.IntegerField(
        min_value=0,
        required=True,
        label='Maximum Price',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    min_price = forms.IntegerField(
        required=True,
        label='Minimum Price',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type':forms.RadioSelect}
        labels = {'member': u'Member name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {'book': forms.RadioSelect}
        labels = {'reviewer': u'Please enter a valid email', 'rating': 'Rating: An integer between 1 (worst) and 5 (best)'}

