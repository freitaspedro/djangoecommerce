# coding=utf-8

from django.shortcuts import render

from .models import Product, Category



def products(request):
	context = {
		'products': Product.objects.all()
	}
	return render(request, 'products.html', context)


def category(request, slug):
	category = Category.objects.get(slug=slug)
	context = {
		'curr_category': category,
		'products_by_category': Product.objects.filter(category=category),
	}
	return render(request, 'category.html', context)


def product(request, c_slug, p_slug):
	# category = Category.objects.get(slug=c_slug)
	product = Product.objects.get(slug=p_slug)
	context = {
		# 'curr_category': category,
		'product': product,
	}
	return render(request, 'product.html', context)
