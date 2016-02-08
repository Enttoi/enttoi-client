# Enttoi Raspberry Pi client

This is a client application that runs on RPi and streams sensors data to [gateway](https://github.com/Enttoi/enttoi-gateway).

## Dependencies

1. [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) 
2. [Requests](http://www.python-requests.org/en/latest/). 

## Deploy 

Setup environment variables:
```bash
export ENTTOI_ENDPOINT=[gateway endpoint URI]
export ENTTOI_CLIENT_TOKEN=[client's token]
```

Persist them, by adding those lines into
```bash
vi ~/.bash_profile
```

Since GPIO requires elevations, environment variables needs to be added for sudo 
```bash
sudo visudo
```
then add:
```bash
Defaults	env_keep +="ENTTOI_ENDPOINT"
Defaults	env_keep +="ENTTOI_CLIENT_TOKEN"
```

Deploy the ```/src``` folder into Raspberry Pi. 

Start client:
```bash
sudo python clint.py
```

## Sensors configuration

The current setup is:
* One [LED](http://www.aliexpress.com/item//32377761083.html) connected to wPi=0 or BCM=17 pin. This LED turned on once the client launched and turned off when terminated
* 2 [reed switches](http://www.aliexpress.com/item//32424305003.html) connected to wPi=5,7 or BCM=4,24. 
