import datetime
import pytz

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.aggregates import Sum, Count

from poll import signal


class Answer(models.Model):
    text = models.CharField(max_length=255)
    poll = models.ForeignKey('poll.Poll', blank=False, null=False)

    def __unicode__(self):
        return self.text


class Poll(models.Model):
    question = models.CharField(max_length=255, blank=False)
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)
    max_num_responses = models.IntegerField(blank=True, default=0, null=False,
    help_text='The poll will automatically close after the number of Users have voted '
    'on this poll')

    def __unicode__(self):
        return self.question

    def is_active(self):
        now = datetime.datetime.now(tz=pytz.UTC)
        valid_date = now > self.start and now < self.end if self.start and self.end else True
        valid_repsonses = self.num_responses() < self.max_num_responses if self.max_num_responses != 0 else True
        return valid_date and valid_repsonses

    def num_responses(self):
        return (Votes.objects
                .filter(answer__poll=self)
                .values('user')
                .aggregate(count=Count('user')))


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
        pr.save()

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
    objects = PollResultManager()

    poll = models.ForeignKey(Poll, blank=False, null=False)
    answer = models.ForeignKey(Answer, blank=False, null=False)
    total_votes = models.PositiveIntegerField(blank=False, default=0)

    class Meta:
        unique_together =(('poll', 'answer'))

    @staticmethod
    def handle_vote_signal(sender, instance, **kwargs):
        if instance.pk:
            original = Votes.objects.get(pk=instance.pk)
            increment = instance.num - original.num
        else:
            increment = instance.num
        PollResult.objects.update_for_vote(vote=instance, increment=increment)


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


models.signals.pre_save.connect(PollResult.handle_vote_signal, sender=Votes)
