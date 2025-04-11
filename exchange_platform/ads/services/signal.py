from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import ExchangeProposal, Ad

@receiver(post_save, sender=ExchangeProposal)
def archive_ad_on_accepted(sender, instance, created, **kwargs):

    if instance.status == ExchangeProposal.STATUS_ACCEPTED:

        ad_sender = instance.ad_sender
        ad_receiver = instance.ad_receiver

        # Архивируем оба объявления
        ad_sender.is_archived = True
        ad_sender.save()

        ad_receiver.is_archived = True
        ad_receiver.save()
