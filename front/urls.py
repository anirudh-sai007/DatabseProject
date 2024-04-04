from django.urls import path

from front import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='seller'),
    path('', views.index, name='customer'),
]