from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings

from model_mommy import mommy


User = get_user_model()


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('index')

    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')


class ContactViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')

    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'contact.html')

    def test_invalid_form(self):
        data = {'name': '', 'email': '', 'message': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'name', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_valid_form(self):
        data = {'name': 'Test', 'email': 'test@test.com', 'message': 'Test Message'}
        response = self.client.post(self.url, data)
        self.assertTrue(response.context['success'])
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Contato Django E-commerce')


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('password123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'login.html')

    def test_invalid_form(self):
        data = {'username': self.user.username, 'password': 'password1234'}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        error_msg = 'Por favor, entre com um usuário  e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas.'
        self.assertFormError(response, 'form', None, error_msg)

    def test_valid_form(self):
        data = {'username': self.user.username, 'password': 'password123'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class LogoutViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('logout')

    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)


class RegisterViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'register.html')

    def test_invalid_form(self):
        data = {'username': 'username12three4', 'password1': 'password1two34', 'password2': 'password123four'}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFormError(response, 'form', 'password2', 'Os dois campos de senha não correspondem.')

    def test_valid_form(self):
        data = {'username': 'username12three4', 'password1': 'password1two34', 'password2': 'password1two34'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('index'))
        self.assertEquals(User.objects.count(), 1)
