from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def kickoff_pretty(value):
    if not value:
        return ""
    return value.strftime("%a %d %b %Y, %H:%M")


@register.filter
def match_result_badge(match):
    if match.home_goals is None or match.away_goals is None:
        return ""

    if match.both_scored:
        return "BTTS Yes"
    return "BTTS No"


@register.filter
def pick_status_label(status):
    if status == "btts_success":
        return "Success"
    if status == "btts_fail":
        return "Fail"
    return "Pending"


@register.filter
def pick_status_style(status):
    if status == "btts_success":
        return "background:#e8f7ed;border:1px solid #b7e4c7;color:#1b5e20;"
    if status == "btts_fail":
        return "background:#fdecec;border:1px solid #f5c2c7;color:#842029;"
    return "background:#f5f5f5;border:1px solid #ddd;color:#333;"