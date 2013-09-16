Basic Requirements
==================

* Polls have multiple choices with a number of votes per answer
* Polls have a date range they are active in, after which they just show
  the results
* Users have some number of votes they can distribute on each poll
* The number of votes a user has is configurable per-user, group and
  global. The more specific overriding the less specific (e.g. user
  settings says 100 votes, group settings say 25 then user setting wins)
* Anon users can see poll results but cannot vote
* Only users with permission can create polls


Some (slightly contrived) design
================================

* Pre calculated table for poll results updated via signal
* Use custom user models rather than get_profile()
* django doesn't have custom group models, so we'll have to track that
  on our own with inheritance.
* HTML is going to be kinda crappy looking
* We don't need any ReST bits... yet.
* Two apps, userprofile and polls.
