from django.db import models
from User.models import User
from StudentApp.models import Orders


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='chat_messages', null=True)
    message = models.TextField(default="", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_send = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} to {self.receiver}'
    




    # sendername = models.TextField(max_length=100, null=True, blank=True)