# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request, 'index.html')


def contact(request):
	return render(request, 'contact.html')


def products(request):
	return render(request, 'products.html')


def product(request):
	return render(request, 'product.html')