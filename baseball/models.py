import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseballStats(models.Model):
    class Bats(models.TextChoices):
        LEFT = "L", _("Left")
        RIGHT = "R", _("Right")
        BOTH = "B", _("Both")

    player = models.CharField(max_length=255)
    rank = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=datetime.datetime.now().year)
    bats = models.CharField(max_length=1, choices=Bats, default=Bats.LEFT)
    age = models.PositiveIntegerField(verbose_name="Age That Year", default=0)
    hits = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("rank", )
        verbose_name_plural = "Baseball Stats"

    def __str__(self):
        return self.player
