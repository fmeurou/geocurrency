FROM nginx:latest
EXPOSE 80
VOLUME /var/www /var/log
COPY nginx.conf /etc/nginx/nginx.conf
ENTRYPOINT ["/usr/sbin/nginx"]