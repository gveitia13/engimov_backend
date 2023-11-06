# Import from alpine which is a ligthway image ready for production
FROM alpine 

# Prepare the image for django deployment
RUN apk update && apk add --no-cache python3 git tzdata && ln -sf python3 /usr/bin/python && python3 -m ensurepip && pip3 install --no-cache --upgrade pip setuptools gunicorn 

# Set the /app/ as the working dir
WORKDIR /app/

# Set the entrypoint as 
ENTRYPOINT python3 $(which gunicorn) --access-logfile /var/log/app/logfile $(ls */wsgi.py | cut -d / -f 1).wsgi:application --bind :8000 --reload

# Create the folder for our logs
RUN mkdir -p /var/log/app/

# Clear our apk cache
RUN rm -rf /var/cache/apk/*

# Include your our custom made app, should include the entrypoint.sh file 
COPY ./ /app/ 

# Install our django project dependencies
RUN pip3 install --no-cache -r /app/requirements.txt

# Run the collect statics
RUN yes yes | python3 /app/manage.py collectstatic 

# Run the migrations (Your docker build command should use the --network in case the db is in a docker network)
RUN python3 /app/manage.py migrate

# Exposes port 8000, this is used in reverse proxies like traefik to detect container port
EXPOSE 8000 
