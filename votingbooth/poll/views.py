from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, DetailView

from poll import models
from poll import forms


class NewPollView(FormView):
    form_class = forms.PollForm
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


class VotePollForm(FormView):
    template_name = 'poll/vote.html'
    form_class = formset_factory(forms.AnswerForm, extra=0)

    def get_initial(self):
        return [{'answer_id': a.id,
                 'answer': a} for a in models.Poll.objects.get(pk=self.kwargs['pk']).answer_set.all()]

    def get_context_data(self, **kwargs):
        context = super(VotePollForm, self).get_context_data(**kwargs)
        context['poll'] = models.Poll.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        for subform in form:
            subform.save(self.request.user)
        return super(VotePollForm, self).form_valid(form)


vote_poll = VotePollForm.as_view()


class PollResultView(ListView):
    model = models.PollResult
    context_object_name = "results"

    def get_queryset(self):
       return self.model.objects.filter(poll__pk=self.kwargs['pk']).order_by('-total_votes')


results_poll = PollResultView.as_view()


