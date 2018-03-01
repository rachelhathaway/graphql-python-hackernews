from django.db import models


class Link(models.Model):
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
