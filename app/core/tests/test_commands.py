'''test custom django management commands'''

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

#check method is provided by the command class in the core/management/wait_for_db
@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """test commands"""
    
    #patched_check will be provided by the patch above
    def test_wait_for_db_ready(self, patched_check):
        """test waiting for db if db is ready"""
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases = ["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """test waiting for db when getting operational error"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])

