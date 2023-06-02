# finance/views.py

# from django.http import JsonResponse
# from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TransactionEditor_Form
from .models import *

def home(request):
    return render(request, 'finance/home.html')

def transaction_create_view(request):
    form = TransactionEditor_Form()
    if request.method == 'POST':
        form = TransactionEditor_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finance-transaction-add')
    return render(request, 'finance/home.html', {'form': form})

def transaction_update_view(request, pk):
    transaction = get_object_or_404(Transactions, pk=pk)
    form = TransactionEditor_Form(instance=transaction)
    if request.method == 'POST':
        form = TransactionEditor_Form(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('finance-transaction-update', pk=pk)
    return render(request, 'finance/home.html', {'form': form})

# AJAX
def load_categories_ajax(request):
    source_id = request.GET.get('source_id')
    categories = Category.objects.filter(source_id=source_id).all()
    return render(request, 'finance/category_dropdown_list_options.html', {'categories': categories})
    #return JsonResponse(list(categories.values('id', 'name')), safe=False)

# JQuery for dependent dropdown
# https://www.youtube.com/watch?v=LmYDXgYK1so

# React for dynamic page
# https://www.youtube.com/channel/UCod4y5gvVv9LuMKGjXUz3MQ/videos