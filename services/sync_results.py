from services.api_client import api_get
from matches.models import Match

def sync_results():
    data = api_get("fixtures", {"live": "all"})

    for f in data["response"]:
        fixture = f["fixture"]
        goals = f["goals"]

        try:
            match = Match.objects.get(api_fixture_id=fixture["id"])
        except Match.DoesNotExist:
            continue

        match.home_goals = goals["home"]
        match.away_goals = goals["away"]
        match.status = fixture["status"]["short"]
        match.both_scored = bool(goals["home"] and goals["away"])
        match.save()

    print("[OK] Live results synced")