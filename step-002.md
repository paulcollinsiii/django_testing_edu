Standard new project machinations
=================================

* mkdir project
* readme, requirements.txt, setup.py
* django-admin startproject project, which does create a few new
  directories for you with the same name. Enh.
* make a folder to hold all your tests
* change the settings to "The One True Way" style

One thing to be aware of is that django 1.5 layout expects "top level"
apps to be fully reusable, thus the names need to be unique in your
virtual env. If you need to namespace them slightly, put them in your
project directory. In this case that'd be 
votingbooth/votingbooth

Split up your requirements
==========================

This is very much an iterative process, you'll be writing tests and then
writing code, and then back to tests. Unit testing in particular is all
about small quick test, run it make sure it fails, then make it pass.
Take each action that you need and break them down.

Things that are missing: We don't know if the date time is timezone
aware! Since this is a brand spanking new django 1.5 project, let's just
assume we want it to be timezone aware (though real life, I'd probably
go back and ask on this)
We'll also have to add pytz to the requirements.txt


Poll Models
===========

Each poll has a question with a list of answers. Boom two models.
For those two models there's nothing interesting to unit test because
they're just tracking state.

Except for that date range requirement. That's an easy test that you
don't need to hit the DB for.


Poll model date range
---------------------
Since each model should know if it's active, we can just call this
`is_active()` on the model and let it figure out the date range bits.
Since the date range is in control of this, we need to have a setup that
will set some date ranges and then call `is_active()` on the Poll model and
check the result.
