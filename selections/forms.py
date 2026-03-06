from django import forms
from matches.models import Match


class PickMatchesForm(forms.Form):
    match_ids = forms.ModelMultipleChoiceField(
        queryset=Match.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Choose 2 matches",
    )

    def __init__(self, *args, **kwargs):
        available_matches = kwargs.pop("available_matches", Match.objects.none())
        super().__init__(*args, **kwargs)
        self.fields["match_ids"].queryset = available_matches

    def clean_match_ids(self):
        matches = self.cleaned_data["match_ids"]
        if len(matches) != 2:
            raise forms.ValidationError("You must choose exactly 2 matches.")
        return matches