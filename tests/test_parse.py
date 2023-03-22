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


html_response = """
<html>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>APEL Publication Summary : SITE </title>
                        <link href="../core/stylesheet.css" rel="stylesheet" type="text/css" />
                        <link href="../core/style.css" rel="stylesheet" type="text/css" />
                </head>
<body>
<h3>APEL Publication Test</h3>
<ul>
 <li> Displays the last time the site published accounting data to the GOC.
 <li> A warning / error is raised if the site has not published accounting data for 7 / 31 days, if a site has not published data for 31 days, which usually signifies a problem with APEL or RGMA services.
 <li> Information about APEL <a href='https://wiki.egi.eu/wiki/APEL'>APEL Wiki</a>
 <li> Contact: apel-admins [at] example.com
<li>lastBuild : 2023-03-21 16:14:50.32</ul><hr><table>
<tr><th colspan='5' class='tableheader'>GSI-LCG2</td></tr>
<tr><th class='tableheader'>ExecutingSite</th><th class='tableheader'>MeasurementDate</th><th class='tableheader'>MeasurementTime</th><th class='tableheader'>Publication <br> Status</th></tr><tr><td align='middle' class='tabletext'>GSI-LCG2</td><td align='middle' class='tabletext'>2023-03-21</td><td align='middle' class='tabletext'>16:13:45</td><td align='middle' class='tabletext'><font color='red'>ERROR [ last published 4726 days ago: 2010-04-12 ]</font></td></tr></table></html>
"""


def mock_response_html(*args, **kwargs):
    return MockResponse(html_response)


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
        mock_print.assert_called_with(
            "UNKNOWN - Something unknown.\n"
            "For more info check URL: http://hostname.com:80/api/test.php"
        )
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
        mock_print.assert_called_with(
            "WARNING - Not everything is ok.\n"
            "For more info check URL: http://hostname.com:80/api/test.php"
        )
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
        mock_print.assert_called_with(
            "WARNING - Not everything is ok.\n"
            "For more info check URL: http://hostname.com:80/api/test.php"
        )
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
        mock_print.assert_called_with(
            "UNKNOWN - Something unknown.\n"
            "For more info check URL: http://hostname.com:80/api/test.php"
        )
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
        mock_print.assert_called_with(
            'CRITICAL - Nothing is ok.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'CRITICAL - Nothing is ok.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'UNKNOWN - Something unknown.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
        mock_sys.assert_called_with(3)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_critical_without_msg_when_response_html(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_html
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname="hostname.com", port=80, uri="/api/test.php"
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='error',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='',
            timeout=20, case_sensitive=False
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with(
            'CRITICAL - A warning / error is raised if the site has not '
            'published accounting data for 7 / 31 days, if a site has not '
            'published data for 31 days, which usually signifies a problem '
            'with APEL or RGMA services.\n'
            'ERROR [ last published 4726 days ago: 2010-04-12 ]\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
        mock_sys.assert_called_with(2)

    @mock.patch('argo_probe_http_parser.parse.sys.exit')
    @mock.patch('argo_probe_http_parser.parse.print')
    @mock.patch('argo_probe_http_parser.parse.requests.get')
    def test_parse_critical_without_msg_when_response_html_case_sensitive(
            self, mock_get, mock_print, mock_sys
    ):
        mock_get.side_effect = mock_response_html
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname="hostname.com", port=80, uri="/api/test.php"
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='ERROR',
            ok_msg='', warn_msg='', crit_msg='', unknown_msg='',
            timeout=20, case_sensitive=True
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with(
            'CRITICAL - ERROR [ last published 4726 days ago: 2010-04-12 ]\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
        mock_sys.assert_called_with(2)

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
        mock_print.assert_called_with(
            'CRITICAL - Nothing is ok.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'CRITICAL - Nothing is ok.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'UNKNOWN - Something unknown.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
            'CRITICAL - CRITICAL: item1,item2,item3\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
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
            'CRITICAL - CRITICAL: item1,item2,item3\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
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
        mock_print.assert_called_with(
            'UNKNOWN - '
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'WARNING - Not everything is ok.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'WARNING - Not everything is ok.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'UNKNOWN - Something unknown.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
            'WARNING - WARNING: item1,item2,item3\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
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
            'WARNING - WARNING: item1,item2,item3\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
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
        mock_print.assert_called_with(
            'UNKNOWN - '
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'CRITICAL - Nothing is ok.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'CRITICAL - Nothing is ok.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'UNKNOWN - Something unknown.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
            'CRITICAL - CRITICAL:item3, item4\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
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
            'CRITICAL - CRITICAL:item3, item4\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
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
        mock_print.assert_called_with(
            'UNKNOWN - '
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
        mock_print.assert_called_with(
            'UNKNOWN - Something unknown.\n'
            'For more info check URL: http://hostname.com:80/api/test.php'
        )
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
