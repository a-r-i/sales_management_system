from django.urls import path

from. import views

urlpatterns = [
    path('fruits-list', views.FruitListView.as_view()),
]