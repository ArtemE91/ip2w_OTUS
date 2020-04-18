import pytest

from ip2w import application


class StartResponse:
    status = ''
    header = []

    def __call__(self, *args, **kwargs):
        self.status = args[0]
        self.header = args[1]


@pytest.mark.parametrize('environ', [{'PATH_INFO': '/ip2w/1.1.1.1'}, {'PATH_INFO': '/ip2w/2.2.2.2'}])
def test_application_valid(environ):
    start_response = StartResponse()
    body = application(environ, start_response)
    assert start_response.status == '200 OK'
    assert start_response.header[-1][-1] == str(len(body[0]))


@pytest.mark.parametrize('environ', [{'PATH_INFO': '1.1.1.1/test'}, {'PATH_INFO': '/ip2w/2.2.2.2/test'}])
def test_application_invalid(environ):
    start_response = StartResponse()
    body = application(environ, start_response)
    assert start_response.status != '200 OK'
    assert start_response.header[-1][-1] == str(len(body[0]))


@pytest.mark.parametrize('environ', [{'PATH_INFO': '/ip2w/1.1.1.1'}, {'PATH_INFO': '/ip2w/2.2.2.2'}])
def test_application_unauthorized(environ):
    start_response = StartResponse()
    body = application(environ, start_response)
    assert start_response.status == '401 Unauthorized' or '403 Forbidden'
    assert start_response.header[-1][-1] == str(len(body[0]))

