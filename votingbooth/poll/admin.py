from django.contrib import admin
from poll import models

admin.site.register(models.Answer)
admin.site.register(models.GroupVotes)
admin.site.register(models.Poll)
admin.site.register(models.PollResult)
admin.site.register(models.Votes)
admin.site.register(models.UserVotes)
