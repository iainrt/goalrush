import uuid
from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from .models import League, LeagueMembership


class LeagueService:

    @staticmethod
    def _generate_code():
        return uuid.uuid4().hex[:10].upper()

    @staticmethod
    @transaction.atomic
    def regenerate_join_code(*, user, league_id):
        league = League.objects.select_for_update().get(id=league_id)

        LeagueService._require_admin(user=user, league=league)

        # generate unique code
        while True:
            code = LeagueService._generate_code()
            if not League.objects.filter(join_code=code).exists():
                break

        league.join_code = code
        league.save(update_fields=["join_code"])

        return code
    
    @staticmethod
    @transaction.atomic
    def join_league_by_join_code(*, user, join_code: str) -> League:
        join_code = (join_code or "").strip().upper()
        if not join_code:
            raise ValidationError("Join code is required.")

        league = (
            League.objects.select_for_update()
            .filter(join_code=join_code)
            .first()
        )
        if not league:
            raise ValidationError("Invalid join code.")

        if league.is_locked:
            raise ValidationError("This league is locked and cannot accept new members.")

        if LeagueMembership.objects.filter(user=user, league=league).exists():
            raise ValidationError("You are already a member of this league.")

        LeagueMembership.objects.create(
            user=user,
            league=league,
            role="member",
        )

        return league

    @staticmethod
    def _get_membership(*, user, league):
        membership = LeagueMembership.objects.filter(user=user, league=league).first()
        if not membership:
            raise PermissionDenied("You are not a member of this league.")
        return membership

    @staticmethod
    def _require_admin(*, user, league):
        membership = LeagueService._get_membership(user=user, league=league)
        if membership.role != "admin":
            raise PermissionDenied("Only league admins can do that.")
        return membership

    @staticmethod
    @transaction.atomic
    def lock_league(*, user, league_id: int) -> League:
        league = League.objects.select_for_update().get(id=league_id)
        LeagueService._require_admin(user=user, league=league)

        if league.is_locked:
            return league

        league.is_locked = True
        league.save(update_fields=["is_locked"])
        return league

    @staticmethod
    @transaction.atomic
    def unlock_league(*, user, league_id: int) -> League:
        league = League.objects.select_for_update().get(id=league_id)
        LeagueService._require_admin(user=user, league=league)

        if not league.is_locked:
            return league

        league.is_locked = False
        league.save(update_fields=["is_locked"])
        return league

    @staticmethod
    @transaction.atomic
    def remove_member(*, user, league_id: int, member_user_id: int) -> None:
        league = League.objects.select_for_update().get(id=league_id)
        LeagueService._require_admin(user=user, league=league)

        member = (
            LeagueMembership.objects
            .select_for_update()
            .filter(league=league, user_id=member_user_id)
            .first()
        )

        if not member:
            raise ValidationError("Member not found.")

        # Prevent removing the league creator
        if league.created_by_id == member.user_id:
            raise ValidationError("The league creator cannot be removed.")

        # Prevent removing the last admin
        if member.role == "admin":
            admin_count = LeagueMembership.objects.filter(league=league, role="admin").count()
            if admin_count <= 1:
                raise ValidationError("You cannot remove the last admin.")

        member.delete()