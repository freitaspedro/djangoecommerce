from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

from model_mommy import mommy


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


class UpdateUserViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:update_user')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('password123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_invalid_form(self):
        self.client.login(username=self.user.name, password='password123')

        data = {'name': '', 'email': ''}
        response = self.client.post(self.url, data, follow=True)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')


    def test_valid_form(self):
        self.client.login(username=self.user.name, password='password123')

        data = {'name': 'name123', 'email': 'email321@email.com'}
        response = self.client.post(self.url, data, follow=True)
        # self.assertRedirects(response, reverse('accounts:index'))

        self.user.refresh_from_db()
        # user = User.objects.get(id=self.user.id)
        self.assertEquals(self.user.name, 'name123')
        self.assertEquals(self.user.email, 'email123@email.com')


class  UpdatePasswordViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:update_password')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('password123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_invalid_form(self):
        self.client.login(username=self.user.name, password='password123')

        data = {'old_password': 'password123', 'new_password1': 'newpassword123', 'new_password2': 'password123'}
        response = self.client.post(self.url, data, follow=True)
        self.assertFormError(response, 'form', 'new_password2', '')

    def test_valid_form(self):
        self.client.login(username=self.user.name, password='password123')

        data = {'old_password': 'password123', 'new_password1': 'newpassword123', 'new_password2': 'newpassword123'}
        response = self.client.post(self.url, data, follow=True)
        # self.assertRedirects(response, reverse('accounts:index'))

        self.user.refresh_from_db()
        # user = User.objects.get(id=self.user.id)
        self.assertTrue(self.user.check_password('newpassword123'))