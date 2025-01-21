# Creating a view
from django.shortcuts import render, redirect
from .forms import AddToInventoryForm

def add_to_inventory(request):
    if request.method == "POST":
        form = AddToInventoryForm(request.POST)
        if form.is_valid():
            item_type = form.cleaned_data['item_type']
            date_added = form.cleaned_data['date_added']
            return redirect('inventory_success')
    else:
        form = AddToInventoryForm()
    
    return render(request, 'add_to_inventory.html', {'form': form})

