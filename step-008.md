Data validation complete?
=========================

So we're passing our data validation tests, which is a good foundation
to start from, but we have a crap UI right now.

I'm not going to fix the layout of it, but let's get at least a few more
views in place that shove data around. Then we can write some more tests
for that.


Big Views Don't Cry
===================

(read the above to the tune of Big Girls Don't Cry)
Pages that are important, shouldn't suddenly die on us. The easiest
smoke test in the world is to use the django client and just load the
page. If it tosses an error, ruroh. We can get a bit fancier if we know
that regardless of how the template is structured, some piece of a model
has to be on that page. If you need to get fancier than that it's
probably worth writing a Selenium test for. In this case our earlier
stub views actually pass the tests!
I'm a bit surprised by this as well actually...


What about those requirements?
==============================

Like only showing the results of a poll after it's no longer valid? That
can be done with the test client as well. Just keep in mind that you'll
make your test code more fragile the more knowledge of the underlying
system you put in. Tests (ESPECIALLY unit tests) should continue working
even if you completely change the underlying implementation of the
function being tested. It's a nice ideal and it's worth taking the time
to shoot for as much as possible, but as you move up the stack in
testing the less possible that seems to become.

Things we haven't touched on:

* Poll results...
* Permissions

This set of tests deals with poll results and submitting votes, but
notice! The way I've written the tests assumes a formset is being used.
That's the price you pay for higher level tests. They have a bit more
knowledge of the underlying implmentation so when it changes you end up
having to update more of your tests. DISABLING YOUR TESTS IS NOT
UPDATING YOUR TESTS. No matter how tempting it might be to shut your
failing tests up that way =)


Tags to follow
==============

Tags 9 - end are fixing tests, then more tests, then fixing.
Further explination is mainly done through the code. If it's strange
looking please send me a PR!!
