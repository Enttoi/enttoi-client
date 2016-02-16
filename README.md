# Enttoi Raspberry Pi client

This is a client application that runs on RPi and streams sensors data to [gateway](https://github.com/Enttoi/enttoi-gateway).

The client will read each sensor's state every `X` ms. After reading, it will report on each change of state immediately or at least once every `Y` seconds (even if the state wasn't changed) to the gateway. This will provide an efficient way of getting real-time state of sensors and track of online/offline clients (due to network or other issues). 

For each sensor a separated thread is spinned, so the IO operations won't block reporting of different sensors.

## Configurations

The only prerequisite is to have environment variables which defines the endpoint of API and a security token. 

Those can be defined either simply in `/etc/environment`:
```bash
ENTTOI_ENDPOINT="[gateway endpoint URI]"
ENTTOI_CLIENT_TOKEN="[client's token]"
```

## Running as shell application

Since GPIO requires elevations, environment variables needs to be added for sudo 
```bash
sudo visudo
```
then add:
```bash
Defaults	env_keep +="ENTTOI_ENDPOINT"
Defaults	env_keep +="ENTTOI_CLIENT_TOKEN"
```

Deploy the `/` folder into Raspberry Pi and start client from terminal:
```bash
sudo python app.py
```

## Running as daemon service

>The client daemonized using [Stephen's](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/) fairly painless trick. 

Assuming that the project cloned into `/home/pi/enttoi-client` (this can me changed in `enttoi.sh`), copy init script to `/etc/init.d`:

```bash
sudo cp enttoi.sh /etc/init.d
```

Make sure that both `enttoi.sh` and `service.py` are executable:

```bash
sudo chmod 755 /etc/init.d/enttoi.sh
chmod 755 service.py
```

At this stage you can start and stop service:
```bash
sudo /etc/init.d/enttoi.sh start
sudo /etc/init.d/enttoi.sh status
sudo /etc/init.d/enttoi.sh stop
```

See log file at `/tmp/entoi-client.log` for info or errors.

Now, add it to boot sequence:
```bash
sudo update-rc.d enttoi.sh defaults
```

## Sensors setup

The current setup is:
* One [LED](http://www.aliexpress.com/item//32377761083.html) connected to wPi=0 or BCM=17 pin. The LED has 4 states:
  * On - client launched, but no request is sent to gateway
  * Slow blinking - latest request were successfull
  * Fast blinking - latest request wasn't sent due error (timeout, network errors, etc)
  * Off - client terminated
* 2 [reed switches](http://www.aliexpress.com/item//32424305003.html) connected to wPi=5,7 or BCM=4,24. 
