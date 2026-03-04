from django import forms

class JoinLeagueForm(forms.Form):
    join_code = forms.CharField(max_length=12)