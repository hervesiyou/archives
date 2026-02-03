
from django.db import  models
from arch_portal.domain.models.librairie import Librairie
from arch_portal.domain.models.membre import Membre

import uuid


class LibrairieMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,  editable=False  )
    librairie = models.ForeignKey(
        Librairie,  # ← remplace par le vrai nom de ton modèle si différent
        on_delete=models.CASCADE,
        related_name='messages',
        db_column='library_id'
    )
    user = models.ForeignKey(
        Membre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='library_messages',
        db_column='user_id'
    )
    username = models.CharField(  max_length=150,  editable=False  )
    message = models.TextField()
    
    created_at = models.DateTimeField(  auto_now_add=True,  db_index=True  )
    updated_at = models.DateTimeField(  auto_now=True  )

    class Meta:
        db_table = 'library_messages'
        ordering = ['-created_at']
        indexes = [ models.Index(fields=['librairie', 'created_at']),  ]

    def __str__(self):
        return f"{self.username} in librairie {self.librairie} – {self.created_at:%Y-%m-%d %H:%M}"

    def save(self, *args, **kwargs):
        if not self.username and self.user:
            self.username = self.user.username or self.user.get_full_name() or "Anonymous"
        super().save(*args, **kwargs)