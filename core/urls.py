
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexHome.as_view(), name='home'),
    path('test', views.Test.as_view(), name='test')
]
