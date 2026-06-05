from django.db.models.signals import post_delete
from django.dispatch import receiver
from web.models import WebUser, Match, Country, LocalRanking
from web.services.rankings import update_global_ranking, update_local_ranking

@receiver(post_delete, sender=WebUser)
def handle_user_deletion(sender, instance, **_kwargs):
    update_global_ranking()
    update_local_ranking(instance.user_country)
    Match.objects.filter(winner__isnull=True, loser__isnull=True).delete()

@receiver(post_delete, sender=Country)
def reassign_deleted_country_users(sender, instance, **_kwargs):
    default_country = Country.get_default_country()
    LocalRanking.objects.filter(country__isnull=True).update(local_position=None, country=default_country)
    update_local_ranking(default_country)
