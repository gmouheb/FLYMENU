from django.shortcuts import render
from .models import Category
from django.views.generic import ListView


# Create your views here.


class CategoryListView(ListView):
    model = Category
    template_name = 'Category/Category_list.html'
