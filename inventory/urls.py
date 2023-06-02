# inventory/urls.py

from django.urls import path
from . import views
from index import views as ixviews
from django.conf.urls import url
from .api import *
from .views import *

urlpatterns = [
    path('../', ixviews.home, name='index'),
    path('', views.onhand, name='inventory-onhand'),

    path('Home/', views.home, name='inventory-home'),

    path('History/', views.history, name='inventory-history'),
    path('History/BulkLoader/', views.bulkloader, name='inventory-history-bulkloader'),
    path('History/UPCTranslator', views.translator, name='inventory-history-translator'),
    path('History/UPCTranslator/Processed', views.translator_processed, name='inventory-history-translator-processed'),

    path('UPC_Editor/', views.upc_editor, name='inventory-upceditor'),
    path('UPC_Editor/new/', views.upc_editor, name='inventory-upceditor-new'),
    path('UPC_Editor/edit/<UPC>', views.upc_editor, name='inventory-upceditor-edit'),

    path('Recipe/', views.RecipeListView.as_view(), name='inventory-recipes'),
    path('Recipe/new/', views.RecipeEditor, name='inventory-recipesnew'),
    path('Recipe/<int:pk>', views.RecipeDetailView.as_view(), name='inventory-recipesdetail'),
    path('Recipe/<id>/edit', views.RecipeEditor, name='inventory-recipeseditor'),
    path('Recipe/<int:pk>/ingredients/edit', views.RecipeIngredientEditView.as_view(), name='inventory-recipeingredienteditor'),

    url(r'^api/scans/$', Scans_Response.as_view(), name='scans-api'),
    url(r'^api/upcdetailpost/$', UpcDetail_Old_Response.as_view(), name='upcdetail-api'),
    url(r'^api/upcdetail/$', UpcDetail_Response.as_view(), name='upcdetailpost-api'),
    url(r'^api/onhand/$', OnHand_Response.as_view(), name='onhand-api'),
]