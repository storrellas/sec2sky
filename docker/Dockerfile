FROM node:10.14.2-alpine
MAINTAINER Sergi Torrellas

# Add folder
RUN apk add --no-cache --update python3 bash mosquitto
ADD . /repo/

# Configure Node
#WORKDIR /repo/react-ui
#RUN npm install
#RUN npm run build

# Configure Django
WORKDIR /repo/
RUN pip3 install -r requirements.txt
RUN python3 manage.py makemigrations api
RUN python3 manage.py migrate
RUN python3 manage.py loaddata api user


# Create superuser (if necessary)
#RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" \
#           | python3 manage.py shell

EXPOSE 8000

# Run container
CMD mosquitto & python3 /repo/mqtt/sensor_sink.py & python3 /repo/manage.py runserver 0.0.0.0:$PORT
