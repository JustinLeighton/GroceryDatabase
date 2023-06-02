# finance/urls.py

from django.urls import path
from . import views
from index import views as ixviews
from django.conf.urls import url
from .views import *


urlpatterns = [
    path('../', ixviews.home, name='index'),
    path('', views.home, name='finance-home'),

    path('transactions/add/', views.transaction_create_view, name='finance-transaction-add'),
    path('transactions/<int:pk>/', views.transaction_update_view, name='finance-transaction-update'),
    path('transactions/ajax/load-categories', views.load_categories_ajax, name='finance-ajax-load-categories')

]