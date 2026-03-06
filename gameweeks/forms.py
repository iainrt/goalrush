from django import forms
from .models import Gameweek
from competitions.models import Competition


class GameweekCreateForm(forms.ModelForm):
    class Meta:
        model = Gameweek
        fields = [
            "name",
            "number",
            "season",
            "competitions",
            "start_date",
            "end_date",
            "lock_time",
            "published",
            "locked",
        ]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "lock_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "competitions": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        league = kwargs.pop("league", None)
        super().__init__(*args, **kwargs)

        self.fields["competitions"].queryset = Competition.objects.order_by("country", "name")

        if league:
            self.fields["season"].initial = league.season