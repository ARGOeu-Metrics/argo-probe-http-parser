import unittest
from unittest import mock

import requests.exceptions

from argo_probe_http_parser.parse import HttpParse


def mock_function(*args, **kwargs):
    pass


class MockResponse:
    def __init__(self, text):
        self.text = text


def mock_response_ok(*args, **kwargs):
    return MockResponse('OK')


def mock_response_warning(*args, **kwargs):
    return MockResponse('WARNING')


def mock_response_critical(*args, **kwargs):
    return MockResponse('CRITICAL')


def mock_response_mixed_warning(*args, **kwargs):
    return MockResponse('WARNING: item1,item2,item3\nOK:item4,item5')


def mock_response_mixed_critical(*args, **kwargs):
    return MockResponse('CRITICAL: item1,item2,item3\nOK:item4,item5')


def mock_response_mixed_warning_and_critical(*args, **kwargs):
    return MockResponse('WARNING: item1,item2\nCRITICAL:item3, item4\nOK:item5')


def mock_response_strange(*args, **kwargs):
    return MockResponse('Some strange text.')


class HttpParseTests(unittest.TestCase):
    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_ok(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_ok
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('OK - Everything is ok.')
        mock_sys.assert_called_with(0)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_ok_case_sensitive(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_ok
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='OK', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('OK - Everything is ok.')
        mock_sys.assert_called_with(0)


    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_ok_case_sensitive_not_found(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_ok
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN - Something unknown.')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_ok_with_ssl(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_ok
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php', ssl=True
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'https://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('OK - Everything is ok.')
        mock_sys.assert_called_with(0)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_warning(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('WARNING - Not everything is ok.')
        mock_sys.assert_called_with(1)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_warning_case_sensitive(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='WARNING', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('WARNING - Not everything is ok.')
        mock_sys.assert_called_with(1)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_warning_case_sensitive_not_found(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN - Something unknown.')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_critical(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('CRITICAL - Nothing is ok.')
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_critical_case_sensitive(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='CRITICAL',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('CRITICAL - Nothing is ok.')
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_critical_case_sensitive_not_found(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN - Something unknown.')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_critical(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_mixed_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('CRITICAL - Nothing is ok.')
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_critical_case_sensitive(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='CRITICAL',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('CRITICAL - Nothing is ok.')
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_critical_case_sensitive_not_found(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN - Something unknown.')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_critical_without_message(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='', timeout=20,
            case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with(
            'CRITICAL - CRITICAL: item1,item2,item3\nOK:item4,item5'
        )
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_critical_without_message_case_sensitive(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='CRITICAL',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='', timeout=20,
            case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with(
            'CRITICAL - CRITICAL: item1,item2,item3\nOK:item4,item5'
        )
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_critical_without_message_case_sensitive_not_found(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='', timeout=20,
            case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_mixed_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('WARNING - Not everything is ok.')
        mock_sys.assert_called_with(1)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_case_sensitive(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='WARNING', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('WARNING - Not everything is ok.')
        mock_sys.assert_called_with(1)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_case_sensitive_not_found(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN - Something unknown.')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_without_message(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='', timeout=20,
            case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with(
            'WARNING - WARNING: item1,item2,item3\nOK:item4,item5'
        )
        mock_sys.assert_called_with(1)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_without_message_case_sensitive(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='WARNING', crit_search='critical',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='', timeout=20,
            case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with(
            'WARNING - WARNING: item1,item2,item3\nOK:item4,item5'
        )
        mock_sys.assert_called_with(1)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_without_message_case_sensitive_not_found(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='', timeout=20,
            case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_and_crit(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_mixed_warning_and_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('CRITICAL - Nothing is ok.')
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_and_crit_case_sensitive(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning_and_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='WARNING', crit_search='CRITICAL',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('CRITICAL - Nothing is ok.')
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_and_crit_case_sensitive_not_found(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning_and_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN - Something unknown.')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_and_critical_without_message(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning_and_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='', timeout=20,
            case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with(
            'CRITICAL - WARNING: item1,item2\nCRITICAL:item3, item4\nOK:item5'
        )
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_and_critical_without_message_case_sensitive(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning_and_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='WARNING', crit_search='CRITICAL',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='', timeout=20,
            case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with(
            'CRITICAL - WARNING: item1,item2\nCRITICAL:item3, item4\nOK:item5'
        )
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_mixed_warning_and_critical_without_message_case_sensitive_nf(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_mixed_warning_and_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='', timeout=20,
            case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_unknown(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_strange
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN - Something unknown.')
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_with_connection_error(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = requests.exceptions.ConnectionError('Error')
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('CRITICAL - Error')
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_with_unknown_error(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = Exception('Unknown exception')
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', unknown_msg='Something unknown.',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN - Unknown exception')
        mock_sys.assert_called_with(3)


if __name__ == '__main__':
    unittest.main()
