#!/usr/bin/bash

source ./env/bin/activate
daphne -e ssl:443:privateKey=privkey.pem:certKey=fullchain.pem linkClick_engine.asgi:application -p 8081 -b 127.0.0.1
deactivate
