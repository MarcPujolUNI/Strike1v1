from django.db import transaction

def rebuild_ranking(queryset, field):
    ranking = queryset.order_by("-counter_user__score")
    ranking.update(**{field: None})
    for position, register in enumerate(ranking, start=1):
        setattr(register, field, position)
    return ranking

@transaction.atomic
def apply_ranking(model_class, ranking, field):
    ranking = rebuild_ranking(ranking, field)
    model_class.objects.bulk_update(ranking, [field])

def update_local_ranking(country_id):
    from web.models import LocalRanking
    apply_ranking(LocalRanking, LocalRanking.objects.filter(country_id=country_id).select_related("counter_user"), 'local_position')

def update_global_ranking():
    from web.models import GlobalRanking
    apply_ranking(GlobalRanking, GlobalRanking.objects.select_related("counter_user"), 'global_position')