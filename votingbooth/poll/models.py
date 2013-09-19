import datetime
import pytz

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.aggregates import Sum
from django.conf import settings


class Answer(models.Model):
    text = models.CharField(max_length=255)
    poll = models.ForeignKey('poll.Poll', blank=False, null=False)


class Poll(models.Model):
    question = models.CharField(max_length=255, blank=False)
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)

    def is_active(self):
        now = datetime.datetime.now(tz=pytz.UTC)
        return now > self.start and now < self.end


class PollResultManager(models.Manager):
    def update_for_vote(self, vote, increment=0):
        """
        Should only be called by a signal, because this blindly adds
        the number of votes to this pre-calc'd table

        :param vote:
        :param increment: How much the vote number has changed by (can be neg)
        """

        pr, _created = self.get_or_create(poll=vote.answer.poll, answer=vote.answer)
        pr.total_votes += increment

    def update_for_poll(self, poll):
        """
        Set the number of total votes for the poll.
        Longer calculation potentially
        :param poll:
        :return:
        """

        for answer in Answer.objects.filter(poll=poll):
            pr, _created = self.get_or_create(poll=answer.poll, answer=answer)
            pr.total_votes = Votes.objects.filter(answer=answer).aggregate(total=Sum('num')).values('total')


class PollResult(models.Model):
    poll = models.ForeignKey(Poll, blank=False, null=False)
    answer = models.ForeignKey(Answer, blank=False, null=False)
    total_votes = models.PositiveIntegerField(blank=False, default=0)

    class Meta:
        unique_together =(('poll', 'answer'))


class Votes(models.Model):
    num = models.PositiveIntegerField(blank=False, null=False)
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class UserVotes(models.Model):
    """Dynamically generate the 1 to 1 relation with users
    """

    user = models.OneToOneField(get_user_model())
    votes_per_poll = models.IntegerField(null=True, blank=True, default=None)

class GroupVotes(models.Model):
    group = models.OneToOneField('auth.Group')
    votes_per_poll = models.IntegerField(null=True, blank=True, default=None)

