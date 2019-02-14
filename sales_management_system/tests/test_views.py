from django.contrib.auth.models import User
from django.test import TestCase


class TestLogin(TestCase):
    def test_get(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/login.html')


class TestIndexView(TestCase):
    def setUp(cls):
        User.objects.create_user(username='testuser',
                                 email='test@test.com',
                                 password='password',
                                 last_name='test',
                                 first_name='user')

    def test_not_authenticated_get(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?redirect_to=/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/index.html')
