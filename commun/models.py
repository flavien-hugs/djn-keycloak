import uuid

from django.db import models
from django.contrib import admin
from django.utils.timezone import now


class BaseTimeStampModel(models.Model):

    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4().hex,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name="date de création",
        db_index=True, default=now
    )
    updated_at = models.DateTimeField(
        verbose_name="date de mise à jour",
        auto_now=True
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    @admin.display(description="date")
    def date(self):
        return self.created_at.date()
