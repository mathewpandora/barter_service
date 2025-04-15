from django.contrib.auth.models import User
from django.db import models

class Ad(models.Model):

    ELECTRONICS = 'electronics'
    CLOTHING = 'clothing'
    TECH = 'tech'
    FURNITURE = 'furniture'
    REAL_ESTATE = 'real_estate'
    AUTO = 'auto'
    CONSTRUCTION = 'construction'
    OTHER = 'other'

    CATEGORY_CHOICES = [
        (ELECTRONICS, 'Электроника'),
        (CLOTHING, 'Одежда и обувь'),
        (TECH, 'Техника'),
        (FURNITURE, 'Мебель'),
        (REAL_ESTATE, 'Недвижимость'),
        (AUTO, 'Авто'),
        (CONSTRUCTION, 'Строительство'),
        (OTHER, 'Прочее'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ads'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=OTHER
    )
    condition = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DECLINED = 'declined'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидает'),
        (STATUS_ACCEPTED, 'Принята'),
        (STATUS_DECLINED, 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='sent_proposals'
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='received_proposals'
    )
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal from {self.ad_sender.title} to {self.ad_receiver.title}"


