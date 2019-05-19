"""
To use this, run:
heroku addons:add heroku-postgresql:dev
heroku config:set TEST_DATABASE_URL="postgres://..." # replace with the new HEROKU_POSTGRESQL_<COLOR>_URL
Then, make TEST_RUNNER setting a Python path to the HerokuTestSuiteRunner class.
"""
import os

import django
from django.test.runner import DiscoverRunner
from django.conf import settings
from django.core.management import call_command
from django.db.utils import ConnectionHandler


class HerokuDiscoverRunner(DiscoverRunner):
    """

    WARNING:  WHEN USED INCORRECTLY THIS TEST RUNNER WILL DROP ALL TABLES IN YOUR PRODUCTION DATABASE

    Heroku does not give users createdb/dropdb permissions, therefore Heroku CI cannot run tests for django.
    In order to fix this, use this test runner instead, which attempts to minimally override the
    default test runner by a) forcing keepdb=True to stop database create/drop, and b) by dropping all
    tables after a test run and resetting the database to its initial blank state.

    """
    def setup_databases(self, **kwargs):
        if not os.environ.get('CI'):
            raise ValueError(
                "The CI env variable must be set to enable this.  WARNING:  "
                "This test runner will wipe all tables in the database it targets!")
        self.keepdb = True
        return super(HerokuDiscoverRunner, self).setup_databases(**kwargs)

    def _wipe_tables(self, connection):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    DROP SCHEMA public CASCADE;
                    CREATE SCHEMA public;
                    GRANT ALL ON SCHEMA public TO postgres;
                    GRANT ALL ON SCHEMA public TO public;
                    COMMENT ON SCHEMA public IS 'standard public schema';
                """
            )

    def teardown_databases(self, old_config, **kwargs):
        self.keepdb = True
        for connection, old_name, destroy in old_config:
            if destroy:
                self._wipe_tables(connection)
        super(HerokuDiscoverRunner, self).teardown_databases(old_config, **kwargs)
