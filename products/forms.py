# forms.py
from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 0:  # the widget's min=0 is only enforced by the browser
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

    class Meta:
        model = Product
        fields = [
            "p_sku",
            "description",
            "quantity",
            "action",
            "location",
        ]
        widgets = {
            "p_sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "Product SKU"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Product description",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "placeholder": "0"}
            ),
            "action": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Restock, audit, dispatch",
                }
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Aisle, shelf, or zone"}
            ),
        }
