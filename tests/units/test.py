from typing import Tuple
import pytest
import requests
import urllib.error

from ip2w import get_ipinfo, Weather

ACCESS_TOKEN_VALID = ''
ACCESS_TOKEN_INVALID = '1234567890abc'
APPID_VALID = ''
APPID_INVALID = '1234567890abc'


@pytest.mark.parametrize('ip', ['1.1.1.1'])
def test_get_ipinfo_valid(ip):
    info_ip = get_ipinfo(ACCESS_TOKEN_VALID, ip)
    assert info_ip['city'] == 'Haymarket'
    assert info_ip['country'] == 'AU'


@pytest.mark.parametrize('ip', ['1.1.1.1'])
def test_get_ipinfo_unauthorizade(ip):
    with pytest.raises(requests.exceptions.HTTPError) as e:
        get_ipinfo(ACCESS_TOKEN_INVALID, ip)
    assert e.value.response.status_code == 403


@pytest.mark.parametrize('ip', ['a1.1.1.1', '1231.143.1.12'])
def test_get_ipinfo_not_found(ip):
    with pytest.raises(requests.exceptions.HTTPError) as e:
        get_ipinfo(ACCESS_TOKEN_VALID, ip)
    assert e.value.response.status_code == 404


@pytest.mark.parametrize('ip', ['192.168.24.222', '192.168.12.224'])
def test_get_ipinfo_bad_request(ip):
    with pytest.raises(Exception) as e:
        get_ipinfo(ACCESS_TOKEN_VALID, ip)
    assert str(e.value) == f"Ipinfo service did not return information about {ip}"


@pytest.mark.parametrize('ipinfo', [{'city': 'Haymarket', 'country': 'AU'}])
def test_weather_valid(ipinfo):
    info_weather = Weather(APPID_VALID)
    response = info_weather.get_weather(ipinfo)
    assert isinstance(response, Tuple)
    assert isinstance(response[0], str) and response[0]
    assert isinstance(response[1], str) and response[1]


@pytest.mark.parametrize('ipinfo', [{'city': 'Haymarket', 'country': 'AU'}])
def test_weather_unauthorizade(ipinfo):
    info_weather = Weather(APPID_INVALID)
    with pytest.raises(urllib.error.HTTPError) as e:
        info_weather.get_weather(ipinfo, timeout=2)
    assert e.value.code == 401


@pytest.mark.parametrize('ipinfo', [{'city': 'Haymaasrket', 'country': 'AUas'},
                                    {'city': '', 'country': ''}])
def test_weather_not_found(ipinfo):
    info_weather = Weather(APPID_VALID)
    with pytest.raises(urllib.error.HTTPError) as e:
        info_weather.get_weather(ipinfo)
    assert e.value.code == 404

