from django import forms
from Movie_Recommender.models import Myrating,RATE_CHOICES

class RateForm(forms.ModelForm):
	rating = forms.ChoiceField(choices=RATE_CHOICES,widget=forms.Select(), required=True)

	class Meta:
		model = Myrating
		fields = ('rating',)