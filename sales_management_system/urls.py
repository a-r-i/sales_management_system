from django.urls import path

from. import views

urlpatterns = [
    path('fruit-list', views.FruitListView.as_view(), name='fruit_list'),
    path('create-fruit', views.FruitCreateView.as_view(), name='create_fruit'),
    path('update-fruit/<int:pk>', views.FruitUpdateView.as_view(), name='update_fruit'),
]