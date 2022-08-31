import unittest

from argo_probe_http_parser.nagios import NagiosResponse


class NagiosResponseTests(unittest.TestCase):
    def setUp(self):
        self.nagios = NagiosResponse()

    def test_ok_message(self):
        self.nagios.set_ok('Everything is ok.')
        self.assertEqual(self.nagios.get_code(), 0)
        self.assertEqual(self.nagios.get_message(), 'OK - Everything is ok.')

    def test_ok_without_message(self):
        self.nagios.set_ok()
        self.assertEqual(self.nagios.get_code(), 0)
        self.assertEqual(self.nagios.get_message(), 'OK')

    def test_warning_message(self):
        self.nagios.set_warning('Not everything is ok.')
        self.assertEqual(self.nagios.get_code(), 1)
        self.assertEqual(
            self.nagios.get_message(), 'WARNING - Not everything is ok.'
        )

    def test_warning_without_message(self):
        self.nagios.set_warning()
        self.assertEqual(self.nagios.get_code(), 1)
        self.assertEqual(self.nagios.get_message(), 'WARNING')

    def test_critical_message(self):
        self.nagios.set_critical('Everything is wrong.')
        self.assertEqual(self.nagios.get_code(), 2)
        self.assertEqual(
            self.nagios.get_message(), 'CRITICAL - Everything is wrong.'
        )

    def test_critical_without_message(self):
        self.nagios.set_critical()
        self.assertEqual(self.nagios.get_code(), 2)
        self.assertEqual(self.nagios.get_message(), 'CRITICAL')

    def test_unknown_message(self):
        self.nagios.set_unknown('Something is wrong.')
        self.assertEqual(self.nagios.get_code(), 3)
        self.assertEqual(
            self.nagios.get_message(), 'UNKNOWN - Something is wrong.'
        )

    def test_unknown_without_message(self):
        self.nagios.set_unknown()
        self.assertEqual(self.nagios.get_code(), 3)
        self.assertEqual(self.nagios.get_message(), 'UNKNOWN')
