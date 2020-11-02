from django import forms
from home.choices import *

class InfoForm(forms.Form):
   #sender = forms.CharField(max_length = 100, label = "Name")
   sender_address_1 = forms.CharField(help_text="Street Address, Etc.", max_length = 100, label = "Address")
   sender_address_2 = forms.CharField(help_text="Apartment, Suite, Unit, Etc. (Optional)", max_length = 100, label = "", required=False)
   sender_city = forms.CharField(max_length = 100, label = "City")
   sender_state = forms.CharField(max_length = 100, label = "State")
   sender_zip_code = forms.CharField(max_length = 100, label="Zip Code")
   sender_country = forms.ChoiceField(choices=ISO3166, label="Country")

   #recipient = forms.CharField(max_length=100, label="Name")
   recipient_address_1 = forms.CharField(help_text="Street Address, Etc.", max_length = 100, label = "Address")
   recipient_address_2 = forms.CharField(help_text="Apartment, Suite, Unit, Etc. (Optional)", max_length=100, label="", required=False)
   recipient_city = forms.CharField(max_length = 100, label = "City")
   recipient_state = forms.CharField(max_length = 100, label = "State")
   recipient_zip_code = forms.CharField(max_length = 100, label="Zip Code")
   recipient_country = forms.ChoiceField(choices=ISO3166, label="Country")
   recipient_resident = forms.BooleanField(label="Check if this is a residential address", required=False)
   height = forms.IntegerField(min_value=1)
   width = forms.IntegerField(min_value=1)
   length = forms.IntegerField(min_value=1)
   weight = forms.IntegerField(min_value=1)
   unit = forms.ChoiceField(choices=weightUnits)

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      #self.fields["sender_state"] = forms.ChoiceField(choices=get_countries(), label="Country")
      #self.fields["recipient_state"] = forms.ChoiceField(choices=ISO3166, label="Country")


#class ResultForm(forms.Form):


