from django import forms

from poll import models


class PollForm(forms.Form):
    question = forms.CharField(max_length=255, required=False)
    start_date = forms.DateTimeField(required=True)
    end_date = forms.DateTimeField(required=True)
    max_num_reponses = forms.IntegerField(required=True,
        help_text='The poll will automatically close after the number of '
                  'Users have voted on this poll (0 means no max)',
        initial=0)

class AnswerForm(forms.Form):
    num_votes = forms.IntegerField(required=False, min_value=0)
    #: What answer does this number of votes tie to
    answer_id = forms.CharField(required=True, widget=forms.HiddenInput)

    def save(self, user):
        """
        ModelForm style without all the pain of a model form
        """

        vote, created = models.Votes.objects.get_or_create(answer=models.Answer.objects.get(pk=self.cleaned_data['answer_id']),
                                                           user=user,
                                                           defaults={'num': self.cleaned_data['num_votes']})

        if not created:
            vote.num = self.cleaned_data['num_votes']
            vote.save()
        return vote
