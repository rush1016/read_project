from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from materials.models import Passage

@login_required
@transaction.atomic
def delete_passage(request, passage_id):
    passage_instance = get_object_or_404(Passage, pk=passage_id)

    if passage_instance:
        passage_instance.delete()

    messages.success(request, 'Successfully deleted reading material.')
    return redirect('reading_material')