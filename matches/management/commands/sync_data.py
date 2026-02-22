from django.core.management.base import BaseCommand
from competitions.models import Competition, Season
from services.sync_teams import sync_teams
from services.sync_fixtures import sync_fixtures
from services.sync_results import sync_results

class Command(BaseCommand):
    help = "Sync teams, fixtures and results"

    def handle(self, *args, **kwargs):
        season = Season.objects.filter(active=True).first()
        if not season:
            self.stdout.write(self.style.ERROR("No active season found"))
            return

        competitions = Competition.objects.all()

        for comp in competitions:
            self.stdout.write(f"Syncing {comp.name}...")
            sync_teams(comp, season_year=2025)
            sync_fixtures(comp, season, season_year=2025)

        sync_results()

        self.stdout.write(self.style.SUCCESS("Full sync complete"))