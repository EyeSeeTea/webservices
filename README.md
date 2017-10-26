## Reverse proxy

Redirect all requests to scipion-portal

Deploy:

```
$ heroku config:set DISABLE_COLLECTSTATIC=0
```

## Config

```
# webservices/settings.py
TARGET = "http://scipion.i2pc.es"
```
