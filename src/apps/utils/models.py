from django.db import models


class Preferences(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    prefs = models.JSONField(default=dict, blank=True)


