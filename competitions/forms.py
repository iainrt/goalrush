from django import forms
from .models import League, Season


class JoinLeagueForm(forms.Form):
    join_code = forms.CharField(max_length=12)


class LeagueCreateForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ["name", "season", "is_public"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["season"].queryset = Season.objects.order_by("-active", "-id")