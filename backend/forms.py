from django import forms
from .models import ItemType 

class AddToInventoryForm(forms.Form):
    item_type = forms.ModelChoiceField(queryset=ItemType.objects.all(),
                                        empty_label="Select Item Type",
                                        to_field_name="barcode")
    date_added = forms.DateField(widget=forms.SelectDateWidget)

