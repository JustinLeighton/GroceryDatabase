from django import forms
from .models import *



class TransactionEditor_Form(forms.ModelForm):

    class Meta:
        model = Transactions
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.none()

        if 'source' in self.data:
            try:
                source_id = int(self.data.get('source'))
                self.fields['category'].queryset = Category.objects.filter(source_id=source_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Category queryset
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.source.category_set.order_by('name')