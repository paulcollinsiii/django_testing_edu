Wait some tests passed?
=======================

Yea, because None is false-y so that means our test isn't specific
enough. Fix that, make sure all of them fail. Instead of just a blind
assert, we should be specific in what we're asserting. Changing this
from:

    assert something

to:

    assert something is something

or depending on the function (if it's not returning a boolean):

    assert something == something

will give you a better test and point more clearly to a failure. The
goal is that a failing unit test should just about direct you to the
exact line that something is failing on.


<picard> Make it so </picard>
=============================

So we've got some failing unit tests.
Excellent.
<ganesha> Fix it </ganesha>


More tests
==========

A table for calculated poll stats. Okay so something is taking a signal
probably from a `post_save()` on. This would normally be split into
several more steps, but for the sake of moving along

* Some method needs to keep track of when new votes go in and update the
  PollResults pre-calculated table. This is a simple increment so it
  doesn't need a unit test per say, but it SHOULD have a functional test!
  We'll get back to this later
* There should be another method that does a recalculation that's
  canonical for that table to make sure they don't get out of sync

Other Changes
=============

Also fill in the model for Answers, but those are less interesting from
a unit test perspective at this point. Grab a super basic template and
some form stuff. Standard machinations for the polls app.
