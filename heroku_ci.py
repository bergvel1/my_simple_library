"""
Test settings for deployment on Heroku CI
"""
# Inherit from your regular test settings, here the settings files are arranged like those generated from the
# django-cookiecutter package
from library_app.settings import *
import environ

env = environ.Env()

# Get the CI environment variable and die if it isn't set; we don't want to risk running this on a production machine as
# all tables will get dropped
CI = env.bool('CI', default=False)  # note this uses django-environ
if not CI:
    raise ValueError('CI environment variable not set to true - avoiding start with this test configuration as a '
                     'safety precaution')

# Register the heroku CI runner, which wipes tables instead of dropping the whole database
# (Heroku users don't have database drop permission)
TEST_RUNNER = 'test_suite_runner.HerokuDiscoverRunner'

# Register the test database as being the same as the default (already set in the settings we inherited from). We've
# used use a heroku addon to provision a new, clean, database into the CI environment, so this should be OK here but
# DEFINITELY SHOULD NOT BE USED IN PRODUCTION
DATABASES['default']['TEST'] = env.db('DATABASE_URL')  # note this uses django-environ
