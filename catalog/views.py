# coding=utf-8

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from watson import search as watson

from .models import Product, Category


class ProductsListView(ListView):

	template_name = 'products.html'
	context_object_name = 'products'
	paginate_by = 3

	def get_queryset(self):
		queryset = Product.objects.all()
		q = self.request.GET.get('q', '')
		if q:
			queryset = watson.filter(queryset, q)
		return queryset


products = ProductsListView.as_view()


class CategoryListView(ListView):

	template_name = 'category.html'
	context_object_name = 'products_by_category'
	paginate_by = 3

	def get_queryset(self):
		return Product.objects.filter(category__slug=self.kwargs['slug'])

	def context_data(self, **kwargs):
		context = super(CategoryListView, self).get_context_data(**kwargs)
		context['curr_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
		return context


category = CategoryListView.as_view()


def product(request, c_slug, p_slug):
	# category = Category.objects.get(slug=c_slug)
	product = Product.objects.get(slug=p_slug)
	context = {
		# 'curr_category': category,
		'product': product,
	}
	return render(request, 'product.html', context)
