from django.urls import path

from. import views

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('fruit-list', views.FruitListView.as_view(), name='fruit_list'),
    path('create-fruit', views.FruitCreateView.as_view(), name='create_fruit'),
    path('update-fruit/<int:pk>', views.FruitUpdateView.as_view(), name='update_fruit'),
    path('delete-fruit/<int:pk>', views.FruitDeleteView.as_view(), name='delete_fruit'),
    path('sale-list', views.SaleListView.as_view(), name='sale_list'),
    path('sale-form', views.SaleFormView.as_view(), name='sale_form'),
    path('sale-form/<int:pk>', views.SaleFormView.as_view(), name='sale_form_pk'),
    path('delete-sale/<int:pk>', views.SaleDeleteView.as_view(), name='delete_sale'),
    path('sale-statistics', views.SaleStatisticsView.as_view(), name='sale_statistics'),
]