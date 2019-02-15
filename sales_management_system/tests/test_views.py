from django.contrib.auth.models import User
from django.test import TestCase


class TestLogin(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_get(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/login.html')

    def test_login(self):
        """
           ユーザ名・パスワードが正しい場合はログインしTopページへ飛ばすことを検証
        """
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


class TestTopView(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?redirect_to=/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/index.html')


class TestFruitListView(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/fruit-list/')
        self.assertRedirects(response, '/login/?redirect_to=/fruit-list/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/fruit-list/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/fruit_list.html')


class TestFruitCreateView(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/create-fruit/')
        self.assertRedirects(response, '/login/?redirect_to=/create-fruit/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/create-fruit/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/fruit_form.html')


class TestFruitUpdateView(TestCase):
    fixtures = ['test_views.json']

    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/update-fruit/1/')
        self.assertRedirects(response, '/login/?redirect_to=/update-fruit/1/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/update-fruit/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/fruit_form.html')


class TestFruitDeleteView(TestCase):
    fixtures = ['test_views.json']

    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/delete-fruit/1/')
        self.assertRedirects(response, '/login/?redirect_to=/delete-fruit/1/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/delete-fruit/1/')
        self.assertRedirects(response, '/fruit-list/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


class TestSaleManagementView(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/sale-management/')
        self.assertRedirects(response, '/login/?redirect_to=/sale-management/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/sale-management/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/sale_management.html')


class TestSaleFormView(TestCase):
    fixtures = ['test_views.json']

    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/sale-form/')
        self.assertRedirects(response, '/login/?redirect_to=/sale-form/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_create_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/sale-form/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/sale_form.html')

    def test_authenticated_update_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/sale-form/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/sale_form.html')


class TestSaleDeleteView(TestCase):
    fixtures = ['test_views.json']

    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/delete-sale/1/')
        self.assertRedirects(response, '/login/?redirect_to=/delete-sale/1/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/delete-sale/1/')
        self.assertRedirects(response, '/sale-management/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


class TestSaleStatisticsView(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/sale-statistics/')
        self.assertRedirects(response, '/login/?redirect_to=/sale-statistics/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/sale-statistics/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/sale_statistics.html')
