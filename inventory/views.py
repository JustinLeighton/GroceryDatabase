# inventory/models.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import modelformset_factory
from django.views.generic import ListView, CreateView, FormView, DetailView, UpdateView
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.db import transaction, IntegrityError
from django.urls import reverse
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import pandas as pd
import requests
from bs4 import BeautifulSoup

def home(request):
    return render(request, 'inventory/home.html')

def onhand(request):
    query_results = Scans.objects.raw("""
    select a.id, a.image, a.description, sum(ifnull(b.delta,0)) as OnHand
    from inventory_upcdetail a
    left join inventory_Scans b on a.id = b.UPC_id
    group by a.id, a.image, a.description
    having sum(ifnull(b.delta,0)) > 0
    order by sum(ifnull(b.delta, 0)) desc""")
    return render(request, 'inventory/onhand.html', {'title': 'OnHand', 'query_results': query_results})

def history(request):
    query_results = Scans.objects.raw("""
        select a.id
              ,a.date
              ,b.id as UPC
              ,b.description
              ,case when a.delta > 0  then 'In' else 'Out' end as delta
        from inventory_scans a
        join inventory_upcdetail b on a.UPC_id = b.id
        order by a.id desc
        limit 100""")
    return render(request, 'inventory/history.html', {'title': 'History', 'query_results': query_results})

def upc_editor(request, UPC=None):
    if UPC:
        instance = get_object_or_404(UpcDetail, id=UPC)
        image = f'/media/{UpcDetail.objects.values_list("image", flat=True).get(id=UPC)}'
    else:
        instance = UpcDetail()
        image = '/media/UPC/default.png'

    form = UpcEditor_Form(request.POST or None, request.FILES or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect('/inventory')

    context = {'form': form,
               'image': image,
               'header': 'Product Information Editor'}
    return render(request, 'inventory/form.html', context)

class RecipeListView(ListView):
    template_name = 'inventory/recipes.html'
    model = Recipes

class RecipeDetailView(DetailView):
    template_name = 'inventory/recipedetail.html'
    model = Recipes

class RecipeCreateView(CreateView):
    template_name = 'inventory/recipecreate.html'
    form_class = RecipeEditor_Form
    queryset = Recipes.objects.all()

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Recipe created.'
        )

        return super().form_valid(form)

def RecipeEditor(request, id=None):
    if id:
        instance = get_object_or_404(Recipes, id=id)
    else:
        instance = Recipes()

    form = RecipeEditor_Form(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect('/inventory/Recipe')

    return render(request, 'inventory/form.html', {'form': form, 'header': 'Product Information Editor'})

class RecipeUpdateView(UpdateView):
    template_name = 'inventory/recipecreate.html'
    form_class = RecipeEditor_Form
    queryset = Recipes.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class RecipeIngredientEditView(SingleObjectMixin, FormView):
    template_name = 'inventory/recipeingredientedit.html'
    model = Recipes

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipes.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipes.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return RecipeIngredientsFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('inventory-recipesdetail', kwargs={'pk': self.object.pk})

def bulkloader(request):
    form = BulkLoader_Form()
    if request.method == 'POST':
        form = BulkLoader_Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            input = cd.get('input')
            print(input)

    context = {'form': form,
               'header': 'Scan Bulk Loader'}
    return render(request, 'inventory/bulkloader.html', context)

def translator(request):
    form = TranslatorForm()
    result_set = pd.DataFrame()
    resultflag = False
    source = ''

    if request.method == 'POST':
        form = TranslatorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            input = cd.get('input')
            source = cd.get('Source')
            resultflag = True

            # Parse input text box
            input = input.replace('\r', '').replace(',', '\n').split('\n')

            # Clean inputs
            input_list = []
            for i in input:
                str(i).replace(' ', '')
                input_list.append(i)

            # Translator function by source
            if source == 'Target DPCI':
                result_set = TargetDPICtoUPC(input_list)

    context = {'form': form,
               'resultflag': resultflag,
               'results': result_set,
               'source': source,
               'header': 'UPC Translator'}

    return render(request, 'inventory/bulkloader.html', context)

def translator_processed(request):

    response_data = ''

    context = {'text': response_data,
               'header': 'UPC Translator'}

    return render(request, 'inventory/bulkloader.html', context)

### Functions

def TargetDPICtoUPC(input_list):
    # Start session
    s = requests.session()
    s.get('https://www.target.com')
    visitorid = s.cookies['visitorId']

    result_set = pd.DataFrame(columns=['DPCI', 'Name', 'UPC'])

    input_list = ['281050554', '063030004', '049040083', '037130749']

    for DPCI in input_list:

        print(DPCI)

        # Initialize output
        upc, Name = 'Unknown', 'Unknown'

        # Search Target using hidden API
        headers = {
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'Accept': 'application/json',
            'Referer': 'https://www.target.com/s?searchTerm=' + DPCI,
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = (
            ('key', 'ff457966e64d5e877fdbad070f276d18ecec4a01'),
            ('channel', 'WEB'),
            ('count', '24'),
            ('default_purchasability_filter', 'false'),
            ('include_sponsored', 'true'),
            ('keyword', DPCI),
            ('offset', '0'),
            ('page', '/s/' + DPCI),
            ('platform', 'desktop'),
            ('pricing_store_id', '659'),
            ('useragent',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'),
            ('visitor_id', visitorid),
        )

        response = requests.get('https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1', headers=headers,
                                params=params)

        # Parse search response
        if response.status_code == 200:

            jsonResponse = response.json()
            resultList = jsonResponse['data']['search']['products']

            tcin = resultList[0]['tcin']
            productUrl = resultList[0]['item']['enrichment']['buy_url']

            # Scrape product page
            response2 = requests.get(productUrl)

            # Parse response
            if response2.status_code == 200:
                soup = BeautifulSoup(response2.text, "html.parser")
                html = str(soup.encode('utf8'))
                index = html.find('primary_barcode')

                if index > 1:
                    html = html[index + 18:]
                    index = html.find('"')
                    upc = html[:index]
                    index = html.find('"name":"')
                    html = html[index + 8:]
                    index = html.find('"}')
                    Name = html[:index]

        # Append to results
        result_set = result_set.append({'DPCI': DPCI, 'Name': Name, 'UPC': upc}, ignore_index=True)

    # Output
    return result_set