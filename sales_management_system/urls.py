from django.urls import path

from. import views

urlpatterns = [
    path('fruit-list', views.FruitListView.as_view()),
]