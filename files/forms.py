from django import forms
from django.contrib.auth.models import User

class ShareFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(
            queryset=user.profile.friends.all(),
            label="Share with",
        )
    message = forms.CharField(widget=forms.Textarea, required=False, label="Message (optional)")