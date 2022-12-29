from django import forms
from django.contrib.auth.forms import UserCreationForm
from .geekmodels import Geek, Maps


# class PlayersForm(forms.ModelForm):
#     class Meta:
#         model = Geek
#         help_texts = {
#             'text_addr': ('Your mobile number'),
#             }
#         widgets = {
#             'tag': forms.HiddenInput(),
# ##            'text_addr': forms.Select(choices=carrier_list),
#             'carrier': forms.Select(choices=carrier_list)
#             }
# ##        fields = ['__all__'] 
#         exclude = ['last_check']

# GEEKS = Geek.objects.values('geek_id','handle').filter(alltime_kdr__gte=0).order_by('alltime_kdr')
TeamGeeks = [['1', 'Doug'],['2', 'Edge']]

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",) 

class GeeksForm(forms.Form):
    TeamGeeks = list(Geek.objects.values_list('geek_id','handle').filter(alltime_kdr__gte=0).order_by('alltime_kdr'))
    geeks_field = forms.MultipleChoiceField(choices = TeamGeeks)
	
