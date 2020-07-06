from django.test import Client, TestCase
from django.urls import reverse

from model_mommy import mommy

from checkout.models import CartItem
from catalog.models import Product


class AddCartItemTestCase(TestCase):

    def setUp(self):
        self.product = mommy.make(Product)
        self.client = Client()
        self.url = reverse('checkout:add_cartitem', kwargs={'slug': self.product.slug})

    def tearDown(self):
        self.product.delete()
        CartItem.objects.all().delete()

    def test_add(self):
    	response = self.client.get(self.url)
    	self.assertRedirects(response, reverse('checkout:cartitem'))
    	self.assertEquals(CartItem.objects.count(), 1)

    def test_double_add(self):
	    response = self.client.get(self.url)
	    response = self.client.get(self.url)
	    self.assertRedirects(response, reverse('checkout:cartitem'))
	    self.assertEquals(CartItem.objects.get().quantity, 2)
	    