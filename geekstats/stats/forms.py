from django import forms
from django.contrib.auth.forms import UserCreationForm
from .geekmodels import Geek


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


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",) 
