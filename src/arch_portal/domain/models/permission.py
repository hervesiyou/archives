import uuid

from django.db import models
from arch_portal.domain.enums import PermissionEnum


class Permission(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, serialize=False
    )
    nom = models.CharField(
        unique=True, choices=PermissionEnum.choices(), max_length=255
    )
    description = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "permissions"
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self):
        return f"{self.nom}"