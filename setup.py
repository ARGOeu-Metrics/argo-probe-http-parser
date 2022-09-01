from distutils.core import setup


NAME = 'argo-probe-http-parser'


def get_ver():
    try:
        for line in open(NAME + '.spec'):
            if "Version:" in line:
                return line.split()[1]

    except IOError:
        raise SystemExit(1)


setup(
    name=NAME,
    version=get_ver(),
    author='SRCE',
    author_email='kzailac@srce.hr',
    description='ARGO probe that parses http response.',
    url='https://github.com/ARGOeu-Metrics/argo-probe-http-parser',
    packages=['argo_probe_http_parser'],
    data_files=[
        ('/usr/libexec/argo/probes/http_parser', ['plugins/check_http_parser'])
    ]
)
