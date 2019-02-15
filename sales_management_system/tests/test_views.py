from django.contrib.auth.models import User
from django.test import TestCase


class TestLogin(TestCase):
    def test_get(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/login.html')


class TestTopView(TestCase):
    def setUp(cls):
        User.objects.create_user(username='testuser',
                                 email='test@test.com',
                                 password='password',
                                 last_name='test',
                                 first_name='user')

    # ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクト
    def test_not_authenticated_get(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?redirect_to=/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/index.html')


class TestFruitListView(TestCase):
    def setUp(cls):
        User.objects.create_user(username='testuser',
                                 email='test@test.com',
                                 password='password',
                                 last_name='test',
                                 first_name='user')

    # ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクト
    def test_not_authenticated_get(self):
        response = self.client.get('/fruit-list/')
        self.assertRedirects(response, '/login/?redirect_to=/fruit-list/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/fruit-list/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/fruit_list.html')


class TestFruitCreateView(TestCase):
    def setUp(cls):
        User.objects.create_user(username='testuser',
                                 email='test@test.com',
                                 password='password',
                                 last_name='test',
                                 first_name='user')

    # ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクト
    def test_not_authenticated_get(self):
        response = self.client.get('/create-fruit/')
        self.assertRedirects(response, '/login/?redirect_to=/create-fruit/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/create-fruit/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/fruit_form.html')


class TestSaleManagementView(TestCase):
    def setUp(cls):
        User.objects.create_user(username='testuser',
                                 email='test@test.com',
                                 password='password',
                                 last_name='test',
                                 first_name='user')

    # ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクト
    def test_not_authenticated_get(self):
        response = self.client.get('/sale-management/')
        self.assertRedirects(response, '/login/?redirect_to=/sale-management/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/sale-management/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/sale_management.html')


class TestSaleFormView(TestCase):
    def setUp(cls):
        User.objects.create_user(username='testuser',
                                 email='test@test.com',
                                 password='password',
                                 last_name='test',
                                 first_name='user')

    # ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクト
    def test_not_authenticated_get(self):
        response = self.client.get('/sale-form/')
        self.assertRedirects(response, '/login/?redirect_to=/sale-form/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/sale-form/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/sale_form.html')


class TestSaleStatisticsView(TestCase):
    def setUp(cls):
        User.objects.create_user(username='testuser',
                                 email='test@test.com',
                                 password='password',
                                 last_name='test',
                                 first_name='user')

    # ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクト
    def test_not_authenticated_get(self):
        response = self.client.get('/sale-statistics/')
        self.assertRedirects(response, '/login/?redirect_to=/sale-statistics/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/sale-statistics/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/sale_statistics.html')
