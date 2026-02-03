
from django.db import models
import uuid

from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.membre import Membre

class CommunauteMessage(models.Model):

    id = models.UUIDField(  primary_key=True,  default=uuid.uuid4,  editable=False  )
    communaute = models.ForeignKey(
        Communaute, 
        on_delete=models.CASCADE,
        related_name='messages',
        db_column='community_id'
    )
    user = models.ForeignKey(
        Membre,
        on_delete=models.SET_NULL,   # ou CASCADE selon ta logique
        null=True,
        blank=True,
        related_name='community_messages',
        db_column='user_id'
    )
    username = models.CharField( max_length=150,  editable=False )
    message = models.TextField()
    
    created_at = models.DateTimeField(  auto_now_add=True,db_index=True  )
    updated_at = models.DateTimeField( auto_now=True )

    class Meta:
        db_table = 'community_messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['communaute', 'created_at']),
        ]

    def __str__(self):
        return f"{self.username} in {self.communaute} – {self.created_at:%Y-%m-%d %H:%M}"

    def save(self, *args, **kwargs):
        if not self.username and self.user:
            self.username = self.user.username or self.user.get_full_name() or "Anonymous"
        super().save(*args, **kwargs)