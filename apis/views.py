from django.views.generic import TemplateView
from .models import ItemType, IndividualItem

class ListView(TemplateView):
    template_name = 'list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all ItemTypes and their related IndividualItems
        # context['item_types'] = IndividualItem.objects.all()
        context['individual_items'] = IndividualItem.objects.select_related('itemType').all()
        print(context)
        return context