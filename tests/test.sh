#!/bin/bash

export PG_HOST=127.0.0.1
export PG_PORT=5432
export PG_USER=test
export PG_PASSWORD=test
export PG_DBNAME=postgres
export SECRET_KEY=django-insecure-t5_xdreud3mu%bq6+=en9g1upcyqgi)y_!+w(q(wp11$1rzr@c
python3 manage.py test $1