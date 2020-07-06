from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings

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



class CheckoutViewTestCase(TestCase):

    def setUp(self):
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('password123')
        self.user.save()
        self.cartitem = mommy.make(CartItem)
        self.client = Client()
        self.checkout_url = reverse('checkout:checkout')

    def test_view(self):
        response = self.client.get(self.checkout_url)
        redirect_url = '{}?next={}'.format(reverse(settings.LOGIN_URL), self.checkout_url)
        self.assertRedirects(response, redirect_url)
        self.client.login(username=self.user.username, password='password123')
        self.cartitem.cart_key = self.client.session.session_key
        self.cartitem.save()
        response = self.client.get(self.checkout_url)
        self.assertTemplateUsed(response, 'checkout.html')

