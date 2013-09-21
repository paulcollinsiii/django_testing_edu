Failing fast
============

So now we've got some more failing tests. This is actually a good thing,
because it means we have more tests that we can make pass! Thus far we
haven't really needed to poke around with Users, but now we need to
start fulfilling the requirements for max votes per user/poll and also
the max votes per user-group / poll. Here we find another place where
the requirements are lacking. Is it
`GroupVotes(group__in=user.groups.all()).aggregate(v=Min('votes_per_poll'))`
or is it `Max()` instead?
For now let's go with min just to go with a least permissions style.
Changing it later isn't hard anways.


Next tag
========

We should have the signals setup between the models, validation
happening on the model, and some kind of method with tests to tell us
how many votes a person can actually have.
