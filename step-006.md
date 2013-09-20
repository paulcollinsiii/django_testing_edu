On to functional testing
========================

At this point there's not a whole lot of business logic left that can
be unit tested easily. The rest is making sure that when things happen
in the DB other parts are acting in concert. For example, while we
have a form right now, it doesn't save anything into the database.
That's a "bug"
Then there's the signaling for Votes to PollResult and making sure the
correct permissions are in there etc.

And user profile. That's completely random since we're not storing
anything beyond what would normally be in the django user.


Signaling between models should work
====================================

I tend to start at the lowest levels and work my way up the chain.
Going top down is also completely valid, but I tend to think DB -->
Python --> HTML(-ish). With that, MORE FAILING TESTS!!!

A note on structure: I'm putting these functional tests not with the
app, but outside of it in the tests folder.

When we create the `TestPollToResultsSignaling` test class, we're
going to need some stub data to shove in the database. Creating a
couple dozen polls and answers is tedious especially since they'll all
follow the same pattern. Thankfully we have tools for this!



Factory Boy, because fixtures kill kittens
==========================================

We'll go through the code for this, but factory boy lets you generate a
lot of test data quickly and easily. Relations between models,
scriptable. Horrible crazy things with signals? Bit more testable now
and just as importantly those tests are maintainable like "real" code.

Django has support for fixtures. They're a trap. No seriously, it's a
flat json file with no returns or pretty printing. You add a new field
to the DB? Suffer. Because that's what fixtures excel at causing.
