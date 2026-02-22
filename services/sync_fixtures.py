from services.api_client import api_get
from competitions.models import Competition, Season
from matches.models import Match, Team
from django.utils.dateparse import parse_datetime

def sync_fixtures(competition: Competition, season: Season, season_year: int):
    data = api_get("fixtures", {
        "league": competition.api_league_id,
        "season": season_year
    })

    for f in data["response"]:
        fixture = f["fixture"]
        teams = f["teams"]
        goals = f["goals"]

        home = Team.objects.get(api_team_id=teams["home"]["id"])
        away = Team.objects.get(api_team_id=teams["away"]["id"])

        Match.objects.update_or_create(
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

    print(f"[OK] Fixtures synced for {competition.name}")