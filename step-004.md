The more things change
======================

Requirements never stay the same, so your unit tests should be able to
adapt to these. Just like your user facing code, unit tests should be
treated like "real" code as well.

Thresholds in this case are fairly straight forward to add to the model
and adapting our test for this isn't too bad.


Mocking
=======

Since we need a way for a poll to know how many users have voted on it,
that's a simple DB query. Initially you might think to just add that DB
query straight into the `is_active()` method for the Poll, but that
would make testing a bit harder! Your functional tests would still be
easy because you'll have the whole DB there, but unit testing just got
painful.

Another way to attack it is to push that DB query out to a method
and then just have that method "lie" in the context of a unit test.

