from django.db import transaction

@transaction.atomic
def delete_passage(request, passage_id):
    pass     