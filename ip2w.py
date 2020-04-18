import yaml
import ipinfo
import logging
import urllib.request
import requests.exceptions
from urllib.error import HTTPError
from urllib import parse
import json

CONFIG_PATH = '/usr/local/etc/ip2w.yml'


OK = 200
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403

err_message = {
    'appid': 'No set appid for OpenWeatherMap. Please set appid in config file!',
    'access_token': 'No set access_token for ipinfo. Please set access_token in config file!',
    BAD_REQUEST: 'Bad Request!',
    UNAUTHORIZED: 'Please check parameter appid in config file!',
    FORBIDDEN: 'Please check parameter access_token in config file!'
}

status_code = {
    OK: '200 OK',
    BAD_REQUEST: '400 Bad Request',
    UNAUTHORIZED: '401 Unauthorized',
    FORBIDDEN: '403 Forbidden'
}


def set_logging(logging_level=logging.INFO, filename='log.log'):
    logging.basicConfig(
        level=logging_level,
        filename=filename,
        format='%(asctime)s %(levelname)s '
               '{%(pathname)s:%(lineno)d}: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


def read_config():
    with open(CONFIG_PATH, 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    return config


def get_ipinfo(access_token, ip_address):
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip_address)
    info = details.all

    if not ("city" in info and "country" in info):
        raise Exception(f"Ipinfo service did not return information about {ip_address}")

    return info


def get_status_code(e):
    code = BAD_REQUEST
    status = status_code[BAD_REQUEST]
    if isinstance(e, HTTPError):
        if e.code == UNAUTHORIZED:
            code = e.code
            status = status_code[UNAUTHORIZED]
    if isinstance(e, requests.exceptions.HTTPError):
        if e.response.status_code == FORBIDDEN:
            code = e.response.status_code
            status = [FORBIDDEN]
    return code, status


class Weather:
    url = 'https://api.openweathermap.org/data/2.5/weather?'

    def __init__(self, appid):
        self.appid = appid

    def get_weather(self, ip_info, timeout=10):
        request = self.generate_request(ip_info)
        response = urllib.request.urlopen(request, timeout=timeout)
        response = json.loads(response.read().decode('utf-8'))

        temp = self.forming_temp(response['main']['temp'])
        conditions = response['weather'][0]['description']

        return temp, conditions

    def generate_request(self, ip_info):
        params = {
            'q': '{city},{country}'.format(
                city=ip_info['city'],
                country=ip_info['country']
            ),
            'units': 'metric',
            'lang': 'ru',
            'appid': self.appid
        }

        request = self.url + parse.urlencode(params)
        return request

    @staticmethod
    def forming_temp(temp: float) -> str:
        temp = str(round(temp))
        if not temp.startswith('-') or temp != '0':
            temp = '+' + temp
        return temp


def application(environ, start_response):
    config = read_config()
    set_logging(filename=config['ip2w']['log_path'])

    appid = config["openweathermap"]["appid"]
    if appid is None:
        logging.error(err_message['appid'])
        raise Exception(err_message['appid'])

    access_token = config["ipinfo"]["access_token"]
    if access_token is None:
        logging.error(err_message['access_token'])
        raise Exception(err_message['access_token'])

    try:
        ip_address = environ['PATH_INFO']
        ip_address = ip_address.split('/')[-1]
        status = '200 OK'

        ip_info = get_ipinfo(access_token, ip_address)
        weather = Weather(config["openweathermap"]["appid"])
        temp, conditions = weather.get_weather(ip_info, config['ip2w']['timeout'])
        body = {
            'city': ip_info['city'],
            'temp': temp,
            'conditions': conditions
        }
        body = str(body).encode('utf-8')
    except Exception as e:
        code, status = get_status_code(e)
        logging.error(err_message[code])
        body = f'{str(e)}! {err_message[code]}'.encode('utf-8')
        type_header = ("Content-Type", "text/html")
    else:
        status = status_code[OK]
        type_header = ("Content-Type", "application/json")
    finally:
        start_response(
            status, [type_header, ("Content-Length", f"{len(body)}")]
        )

        return [body]