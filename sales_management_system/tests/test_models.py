from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Fruit


class TestFruit(TestCase):
    fixtures = ['test_models.json']

    # 削除リンクを押すと、対象の果物は削除される
    def test_delete_fruit_get(self):
        self.client.force_login(User.objects.create_user('testuser'))

        fruit_count = Fruit.objects.all().count()
        self.assertEqual(fruit_count, 1)

        response = self.client.get('/delete-fruit/1/')
        self.assertRedirects(response, '/fruit-list/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

        fruit_count = Fruit.objects.all().count()
        self.assertEqual(fruit_count, 0)
