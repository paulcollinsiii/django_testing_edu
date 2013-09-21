from .base import *

INSTALLED_APPS.append('django_nose')
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

LOGGING['loggers']['factory'] = {
    'handlers': ['null',],
    'level': 'DEBUG',
    'propagate': False
}
