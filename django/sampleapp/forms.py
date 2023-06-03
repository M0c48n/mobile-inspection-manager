from django import forms

class ImeiForm(forms.Form):
    imei = forms.CharField(label='IMEI', max_length=15)  # IMEIは通常15桁の数字
