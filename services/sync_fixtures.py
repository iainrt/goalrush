from services.api_client import api_get
from competitions.models import Competition, Season
from matches.models import Match, Team
from django.utils.dateparse import parse_datetime
from django.db import transaction

def sync_fixtures(competition: Competition, season: Season, season_year: int):
    data = api_get("fixtures", {
        "league": competition.api_league_id,
        "season": season_year
    })

    created = 0
    updated = 0
    skipped = 0

    for f in data.get("response", []):
        try:
            fixture = f["fixture"]
            teams = f["teams"]
            goals = f["goals"]

            home_api_id = teams["home"]["id"]
            away_api_id = teams["away"]["id"]

            home = Team.objects.filter(api_team_id=home_api_id).first()
            away = Team.objects.filter(api_team_id=away_api_id).first()

            # Auto-create teams if missing (self-healing)
            if not home:
                home = Team.objects.create(
                    api_team_id=home_api_id,
                    name=teams["home"]["name"],
                    competition=competition
                )

            if not away:
                away = Team.objects.create(
                    api_team_id=away_api_id,
                    name=teams["away"]["name"],
                    competition=competition
                )

            obj, created_flag = Match.objects.update_or_create(
                api_fixture_id=fixture["id"],
                defaults={
                    "home_team": home,
                    "away_team": away,
                    "competition": competition,
                    "season": season,
                    "kickoff_time": parse_datetime(fixture["date"]),
                    "status": fixture["status"]["short"],
                    "home_goals": goals["home"],
                    "away_goals": goals["away"],
                    "both_scored": bool(goals["home"] and goals["away"]),
                }
            )

            if created_flag:
                created += 1
            else:
                updated += 1

        except Exception as e:
            skipped += 1
            print(f"[SKIP] Fixture error: {e}")

    print(f"[OK] {competition.name} → created={created}, updated={updated}, skipped={skipped}")