from services.api_client import api_get
from competitions.models import Competition
from matches.models import Team

def sync_teams(competition: Competition, season_year: int):
    data = api_get("teams", {
        "league": competition.api_league_id,
        "season": season_year
    })

    for t in data["response"]:
        team_data = t["team"]

        Team.objects.update_or_create(
            api_team_id=team_data["id"],
            defaults={
                "name": team_data["name"],
                "competition": competition
            }
        )

    print(f"[OK] Teams synced for {competition.name}")