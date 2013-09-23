import datetime
from django.core.exceptions import ValidationError
import pytz

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.aggregates import Sum, Count, Min

DEFAULT_GLOBAL_VOTES = 15

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

    def clean(self):
        allowed_votes = UserVotes.objects.get_allowed_votes(self.user)
        if self.num > allowed_votes:
            raise ValidationError('Attempted to vote more than allowed')
        total_votes_used = (Votes.objects
            .filter(answer__poll=self.answer.poll)
            .exclude(pk=self.pk)
            .aggregate(s=Sum('num')))['s'] or 0  # In case it's None
        if (total_votes_used + self.num) > allowed_votes:
            raise ValidationError('Attempted to vote more than allowed')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super(Votes, self).save(force_insert, force_update, using, update_fields)


class UserVotesManager(models.Manager):
    def get_allowed_votes(self, user):
        """Return the max number of votes a user can put on a poll

        Takes into account User --> Groups --> Global overrides
        """

        try:
            uv = UserVotes.objects.get(user=user)
            return uv.votes_per_poll
        except UserVotes.DoesNotExist:
            pass

        gv = (GroupVotes.objects.filter(group__in=user.groups.all())
              .aggregate(votes_allowed=Min('votes_per_poll')))
        if gv['votes_allowed'] is not None:
            return gv['votes_allowed']
        if hasattr(settings, 'POLL_SETTINGS') and 'GLOBAL_VOTES' in settings.POLL_SETTINGS:
            return settings.POLL_SETTINGS['GLOBAL_VOTES']
        return DEFAULT_GLOBAL_VOTES


class UserVotes(models.Model):
    objects = UserVotesManager()

    user = models.OneToOneField(get_user_model())
    votes_per_poll = models.IntegerField(null=True, blank=True, default=None)



class GroupVotes(models.Model):
    group = models.OneToOneField('auth.Group')
    votes_per_poll = models.IntegerField(null=True, blank=True, default=None)


models.signals.pre_save.connect(PollResult.handle_vote_signal, sender=Votes)
