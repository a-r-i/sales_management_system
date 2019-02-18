from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Fruit, Sale


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

    def test_create(self):
        """
            データをPOSTするとFruitテーブルのレコードが1件作成されるかを検証
        """
        self.client.login(**self.credentials)
        fruit_count = Fruit.objects.count()
        self.client.post("/create-fruit/", {'name': "リンゴ", 'price': 100})
        self.assertEqual(Fruit.objects.count(), fruit_count+1)


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

    def test_update(self):
        """
             データをPOSTするとレコードの内容が更新されるかを検証
        """
        self.client.login(**self.credentials)

        pk = 2

        fruit = Fruit.objects.create(id=pk, name='リンゴ', price=100)

        self.client.post('/update-fruit/%i/' % pk, {'name': 'ブルーベリー', 'price': 100})

        fruit.refresh_from_db()
        self.assertEqual(fruit.name, 'ブルーベリー')


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
    
    def test_delete(self):
        """
            削除リンクを押すと、対象の果物が削除されることを検証
        """
        self.client.login(**self.credentials)
        pk = 1
        fruit_count = Fruit.objects.filter(pk=pk).count()
        self.client.get('/delete-fruit/%i/' % pk)
        self.assertEqual(Fruit.objects.filter(pk=pk).count(), fruit_count-1)


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


class TestSaleCreateView(TestCase):
    fixtures = ['test_views.json']

    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/create-sale/')
        self.assertRedirects(response, '/login/?redirect_to=/create-sale/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/create-sale/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/sale_form.html')

    def test_create(self):
        """
            データをPOSTするとSaleテーブルのレコードが1件作成されるかを検証
        """
        self.client.login(**self.credentials)
        sale_count = Sale.objects.count()
        self.client.post("/create-sale/", {'fruit': 1, 'amount': 1, 'sold_at': '2018-12-10 09:18'})
        self.assertEqual(Sale.objects.count(), sale_count+1)


class TestSaleUpdateView(TestCase):
    fixtures = ['test_views.json']

    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_not_authenticated_get(self):
        """
            ログインせず、ログインページ以外のページにアクセスした場合、ログインページへリダイレクトすることを検証
        """
        response = self.client.get('/update-sale/1/')
        self.assertRedirects(response, '/login/?redirect_to=/update-sale/1/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_authenticated_get(self):
        self.client.login(**self.credentials)
        response = self.client.get('/update-sale/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'sales_management_system/sale_form.html')

    def test_update(self):
        """
             データをPOSTするとレコードの内容が更新されるかを検証
        """
        self.client.login(**self.credentials)

        pk = 3

        fruit = Fruit.objects.get(id=1)
        sale = Sale.objects.create(id=pk, fruit=fruit, amount=1, sold_at='2018-12-10 09:18:30.845202')

        self.client.post('/update-sale/%i/' % pk, {'fruit': 1, 'amount': 2, 'sold_at': '2018-12-10 09:18:30.845202'})

        sale.refresh_from_db()
        self.assertEqual(sale.amount, 2)


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

    def test_delete(self):
        """
            削除リンクを押すと、対象の販売情報が削除されることを検証
        """
        self.client.login(**self.credentials)
        pk = 1
        sale_count = Sale.objects.filter(pk=pk).count()
        self.client.get('/delete-fruit/%i/' % pk)
        self.assertEqual(Sale.objects.filter(pk=pk).count(), sale_count-1)


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
