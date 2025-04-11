from django.db import models
from django.contrib.auth.models import User
from ads.models import ExchangeProposal

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    proposal = models.OneToOneField(ExchangeProposal, on_delete=models.CASCADE)  # Связь с предложением
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чат для предложения {self.proposal.id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.sender.username} в чате {self.chat.id}"
