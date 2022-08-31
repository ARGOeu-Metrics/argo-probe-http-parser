class NagiosResponse:
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self):
        self._code = self.OK
        self._status = 'OK'
        self._msg = ''

    def _create_msg(self, msg):
        if msg:
            return '{} - {}'.format(self._status, msg)

        else:
            return self._status

    def set_ok(self, msg=''):
        self._code = self.OK
        self._status = 'OK'
        self._msg = self._create_msg(msg)

    def set_warning(self, msg=''):
        self._code = self.WARNING
        self._status = 'WARNING'
        self._msg = self._create_msg(msg)

    def set_critical(self, msg=''):
        self._code = self.CRITICAL
        self._status = 'CRITICAL'
        self._msg = self._create_msg(msg)

    def set_unknown(self, msg=''):
        self._code = self.UNKNOWN
        self._status = 'UNKNOWN'
        self._msg = self._create_msg(msg)

    def get_code(self):
        return self._code

    def get_message(self):
        return self._msg
