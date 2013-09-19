from django.views.generic import FormView, ListView, DetailView
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


class NewPollView(FormView):
    form_class = PollForm
    template_name = 'poll/new.html'

new_poll = NewPollView.as_view()

class ListPollView(ListView):
    model = models.Poll
    context_object_name = 'poll_list'

list_poll = ListPollView.as_view()

class DetailPollView(DetailView):
    model = models.Poll
    context_object_name = 'poll'

    def get_context_data(self, **kwargs):
        context = super(DetailPollView, self).get_context_data(**kwargs)
        context['answers'] = self.object.answer_set.all()
        return context


detail_poll = DetailPollView.as_view()
