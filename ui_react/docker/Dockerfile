#Grab the latest alpine image
FROM nginx
COPY ./public/ /usr/share/nginx/html
COPY ./dist /usr/share/nginx/html/dist
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
