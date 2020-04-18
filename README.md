## GitHub-ArtemE91 ip2w_OTUS

Traing uwsgi daemon project.
Upon request, IPv4 returns the current weather in the city to which ip belongs.
The following parameters must be added to the config. 
After unpacking the rpm package, the config is located in /usr/local/etc/ip2w.yml.
```
ipinfo:
  access_token: 1234567890abc

openweathermap:
  appid: 1234567890abc
```
 
 ## Requires
 
 * CentOS 7,8
 * Python3+
 * python-requests library
 * systemd
 * nginx
 * uwsgi
 
 ## How to Run

 ```ini
 # install rpm package
 rpm -i ip2w-0.0.1-1.noarch.rpm
 
 # Run services
 systemctl start ip2w
 systemctl start nginx
 ```
 
 ## Example
 
 ```ini
 # Request
 curl http://127.0.0.1/ip2w/1.1.1.1
 
 # Response
{'city': 'Haymarket', 'temp': '+17', 'conditions': 'ясно'}
 ```
 
 ## How to stop
 
 ```ini
 systemctl stop ip2w
 ```
 
 ## Location settings file
 
 * __config nginx:__ `/etc/nginx/conf.d/ip2w.nginx.conf`
 * __config uwsgi:__ `/usr/local/ip2w/ip2w.uwsgi.ini`
 * __config app:__ `/usr/local/etc/ip2w.yml`
 * __systemd unit file:__ `/usr/systemd/system/ip2w.service`
 * __app:__ `/usr/local/ip2w/ip2w.py`
 * __log:__ `/var/log/ip2w/ip2w.log`
 
 
 ## How to run tests
 
 * __units:__ `(venv) python -m pytest tests/units/test.py `
 * __integration:__ `(venv) python -m pytest tests/integrations/application_test.py`
 
 ### Example
 ```
 # integration - python -m pytest tests/integrations/application_test.py 
 (venv) mbp-user:ip2w_OTUS user$ python -m pytest tests/units/test.py 
============================================================================== test session starts ==============================================================================
platform darwin -- Python 3.7.3, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /Users/user/PycharmProjects/ip2w_OTUS
collected 10 items                                                                                                                                                              

tests/units/test.py ..........                                                                                                                                            [100%]

============================================================================== 10 passed in 36.98s ==============================================================================
```
