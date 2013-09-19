def nosettings(**overrides):
    """Magic incantation to make django setting just ignore us and move along
    you HAVE to do this before importing anything from any django app

    Sadly this means the order of your imports matter
    """

    from django.conf import settings, global_settings
    if not settings.configured:
        settings.configure(default_settings=global_settings, **overrides)

