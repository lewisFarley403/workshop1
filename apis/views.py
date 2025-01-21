from rest_framework import viewsets
from .models import ItemType, IndividualItem
from .serializers import ItemTypeSerializer

from django.shortcuts import render

# Function-based view that renders an HTML page
from django.views.generic import TemplateView

# Class-based view that renders an HTML page
class ListView(TemplateView):
    template_name = 'list.html'
    model = IndividualItem
    context_object_name = 'item_types'  # The name of the context variable in the template
