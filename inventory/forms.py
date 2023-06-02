from django import forms
from django.forms.models import inlineformset_factory
from .models import *

class UpcEditor_Form(forms.ModelForm):
    class Meta:
        model = UpcDetail
        fields = [
            'id',
            'description',
            'details',
            'category',
            'grams',
            'image'
        ]
        labels = {
            'id': 'UPC Code',
            'description': 'Product Name',
            'details': 'Product Description',
            'category': 'Ingredient Category',
            'grams': 'Grams',
            'Image': 'Image',
        }

class RecipeEditor_Form(forms.ModelForm):
    class Meta:
        model = Recipes
        fields = [
            'title',
            'servings',
            'preptimeminutes',
            'description',
        ]
        labels = {
            'title': 'Title',
            'servings': 'Servings',
            'preptimeminutes': 'Prep Time (Minutes)',
            'description': 'Description',
        }

class IngredientEditor_Form(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = [
            'id',
            'category',
            'grams',
        ]
        labels = {
            'id': 'BASID',
            'category': 'Category',
            'grams': 'Grams',
        }

RecipeIngredientsFormset = inlineformset_factory(Recipes, Ingredients, fields=('__all__'), extra=10)

class BulkLoader_Form(forms.Form):
    input = forms.CharField(widget=forms.Textarea, label="Input", required=True)

class TranslatorForm(forms.Form):
    input = forms.CharField(widget=forms.Textarea, label="Input", required=True)
    Source = forms.ChoiceField(choices=[(x, x) for x in ("Target DPCI", "Other")])
