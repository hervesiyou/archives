import uuid
from django.db import models
from arch_portal.domain.enums import RoleEnum


class Role(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, serialize=False
    )
    nom = models.CharField(unique=True, choices=RoleEnum.choices(), max_length=50)
    description = models.CharField(max_length=255, null=True)
    permissions = models.ManyToManyField("Permission")

    class Meta:
        db_table = "roles"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return f"{self.nom} , {len(self.permissions.all())}"
