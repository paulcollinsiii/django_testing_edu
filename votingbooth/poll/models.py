import datetime
import pytz

from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=255, blank=False)
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)

    def is_active(self):
        pass
