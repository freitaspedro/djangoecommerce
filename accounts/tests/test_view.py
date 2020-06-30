from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()



class RegisterViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:register')

    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'register.html')

    def test_invalid_form_required_field(self):
        data = {'username': 'username12three4', 'password1': 'password1two34', 'password2': 'password123four'}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')

    def test_invalid_form(self):
        data = {'username': 'username12three4', 'email': 'email123@email.com', 'password1': 'password1two34', 'password2': 'password123four'}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFormError(response, 'form', 'password2', 'Os dois campos de senha não correspondem.')

    def test_valid_form(self):
        data = {'username': 'username12three4', 'email': 'email123@email.com', 'password1': 'password1two34', 'password2': 'password1two34'}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertEquals(User.objects.count(), 1)
