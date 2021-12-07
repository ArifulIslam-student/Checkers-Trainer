from django import forms
from .models import Userstable


class FormUserstable(forms.ModelForm):
    class Meta:
        model = Userstable
        fields = ["userid", "userpassword"]
