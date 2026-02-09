from django import forms
from budgets.models import Budget
from decimal import Decimal


class BudgetForm(forms.ModelForm):
    """Form for creating and editing budgets."""
    class Meta:
        model = Budget
        fields = ['category', 'monthly_limit', 'currency']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'monthly_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3', 'placeholder': 'INR'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            from transactions.models import Category
            # Filter categories to only show user's expense categories
            self.fields['category'].queryset = Category.objects.filter(
                user=user,
                type='expense'
            )

    def clean(self):
        cleaned_data = super().clean()
        monthly_limit = cleaned_data.get('monthly_limit')

        if monthly_limit is not None and monthly_limit <= Decimal('0.00'):
            raise forms.ValidationError("Monthly limit must be greater than zero.")

        return cleaned_data
