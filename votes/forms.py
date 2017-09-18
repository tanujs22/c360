from django import forms
from django.forms import HiddenInput
from .models import Votes
class VoteForm(forms.Form):
	class Meta:
		model = Votes
		widgets = {'any_fields' : HiddenInput(),}