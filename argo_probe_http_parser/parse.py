import sys

import requests

from argo_probe_http_parser.nagios import NagiosResponse


class HttpParse:
    def __init__(self, hostname, port, uri, ssl=False):
        self.hostname = hostname
        self.port = port
        self.uri = uri
        self.ssl = ssl

        self.nagios = NagiosResponse()

    def _build_url(self):
        hostname = self.hostname
        if hostname.startswith('https://'):
            hostname = hostname[8:]

        if hostname.startswith('http://'):
            hostname = hostname[7:]

        if hostname.endswith('/'):
            hostname = hostname[0:-1]

        uri = self.uri
        if not uri.startswith('/'):
            uri = '/{}'.format(uri)

        if self.ssl:
            return 'https://{}:{}{}'.format(hostname, self.port, uri)

        else:
            return 'http://{}:{}{}'.format(hostname, self.port, uri)

    def parse(
            self, ok_search, warn_search, crit_search, ok_msg, warn_msg,
            crit_msg, unknown_msg, timeout, case_sensitive
    ):
        url = self._build_url()

        try:
            response = requests.get(url, timeout=timeout)
            response_text = response.text

            if not case_sensitive:
                crit_search = crit_search.lower()
                warn_search = warn_search.lower()
                ok_search = ok_search.lower()
                response_text = response_text.lower()

            if crit_search in response_text:
                if crit_msg:
                    msg = crit_msg
                else:
                    msg = "\n".join([
                        c for c in response.text.split("\n") if
                        crit_search.lower() in c.lower()
                    ])

                msg = f"{msg}\nFor more info check URL: {url}"
                self.nagios.set_critical(msg)

            elif warn_search in response_text:
                if warn_msg:
                    msg = warn_msg

                else:
                    msg = "\n".join([
                        w for w in response.text.split("\n") if
                        warn_search.lower() in w.lower()
                    ])

                msg = f"{msg}\nFor more info check URL: {url}"
                self.nagios.set_warning(msg)

            elif ok_search in response_text:
                self.nagios.set_ok(ok_msg)

            else:
                if unknown_msg:
                    msg = f"{unknown_msg}\nFor more info check URL: {url}"

                else:
                    msg = f"For more info check URL: {url}"

                self.nagios.set_unknown(msg)

        except (
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.RequestException
        ) as e:
            self.nagios.set_critical(str(e))

        except Exception as e:
            self.nagios.set_unknown(str(e))

        print(self.nagios.get_message())
        sys.exit(self.nagios.get_code())
