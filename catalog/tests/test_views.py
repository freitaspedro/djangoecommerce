from django.test import TestCase, Client
from django.urls import reverse

from model_mommy import mommy

from catalog.models import Category, Product



class ProductsTestCase(TestCase):

	def setUp(self):
		self.products = mommy.make(Product, _quantity=10)
		self.url = reverse('products')
		self.client = Client()

	def tearDown(self):
		for product in self.products:
			product.delete()

	def test_status_code(self):
		response = self.client.get(self.url)
		self.assertEquals(response.status_code, 200)

	def test_template_used(self):
		response = self.client.get(self.url)
		self.assertTemplateUsed(response, 'products.html')

	def test_context(self):
		response = self.client.get(self.url)
		self.assertTrue('products' in response.context)
		self.assertEquals(response.context['products'].count(), 10)



class CategoryTestCase(TestCase):

	def setUp(self):
		self.category = mommy.make(Category)
		self.products = mommy.make(Product, category=self.category, _quantity=5)
		self.url = reverse('category', kwargs={'slug': self.category.slug})
		self.client = Client()

	def tearDown(self):
		for product in self.products:
			product.delete()
		self.category.delete()

	def test_status_code(self):
		response = self.client.get(self.url)
		self.assertEquals(response.status_code, 200)

	def test_template_used(self):
		response = self.client.get(self.url)
		self.assertTemplateUsed(response, 'category.html')

	def test_context(self):
		response = self.client.get(self.url)
		self.assertTrue('curr_category' in response.context)
		self.assertTrue('products_by_category' in response.context)
		self.assertEquals(response.context['products_by_category'].count(), 5)


class ProductTestCase(TestCase):

	def setUp(self):
		self.category = mommy.make(Category)
		self.product = mommy.make(Product, category=self.category)
		self.url = reverse('product', kwargs={'c_slug': self.category.slug, 'p_slug': self.product.slug})
		self.client = Client()

	def tearDown(self):
		self.product.delete()
		self.category.delete()

	def test_status_code(self):
		response = self.client.get(self.url)
		self.assertEquals(response.status_code, 200)

	def test_template_used(self):
		response = self.client.get(self.url)
		self.assertTemplateUsed(response, 'product.html')

	def test_context(self):
		response = self.client.get(self.url)
		self.assertTrue('product' in response.context)
		self.assertEquals(response.context['product'], self.product)
