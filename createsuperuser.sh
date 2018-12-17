#!/bin/bash

COMMAND="from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
echo $COMMAND | python manage.py shell
