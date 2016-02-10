# Enttoi Raspberry Pi client

This is a client application that runs on RPi and streams sensors data to [gateway](https://github.com/Enttoi/enttoi-gateway).

The client will read each sensor's state every `X` ms. After reading, it will report on each change of state immediately or at least once every `Y` seconds (even if the state wasn't changed) to the gateway. This will provide an efficient way of getting real-time state of sensors and track of online/offline clients (due to network or other issues). 

For each sensor a separated thread is spinned, so the IO operations won't block reporting of different sensors.

## Dependencies

1. [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) 
2. [Requests](http://www.python-requests.org/en/latest/). 

## Deploy lower env

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
Defaults	env_keep +="ENTTOI_ENDPOINT ENTTOI_CLIENT_TOKEN"
```

Deploy the ```/src``` folder into Raspberry Pi. 

Start client:
```bash
sudo python client.py
```

## Sensors configuration

The current setup is:
* One [LED](http://www.aliexpress.com/item//32377761083.html) connected to wPi=0 or BCM=17 pin. This LED turned on once the client launched and turned off when terminated
* 2 [reed switches](http://www.aliexpress.com/item//32424305003.html) connected to wPi=5,7 or BCM=4,24. 
