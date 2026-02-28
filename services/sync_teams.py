from services.api_client import api_get
from competitions.models import Competition
from matches.models import Team

def sync_teams(competition: Competition, season_year: int):
    data = api_get("teams", {
        "league": competition.api_league_id,
        "season": season_year
    })

    created = 0
    updated = 0

    for t in data.get("response", []):
        team_data = t["team"]

        obj, created_flag = Team.objects.update_or_create(
            api_team_id=team_data["id"],
            defaults={
                "name": team_data["name"],
                "competition": competition
            }
        )

        if created_flag:
            created += 1
        else:
            updated += 1

    print(f"[OK] {competition.name} teams → created={created}, updated={updated}")