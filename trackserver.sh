#!/usr/bin/bash

source ./env/bin/activate
daphne linkClick_engine.asgi:application  -p 443 -b 127.0.0.1
deactivate