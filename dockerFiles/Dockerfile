# Workforcehub was written with Python 3.11
FROM python:3.11

# Create a working directory for the image to be built in.
# This is where `docker exec -it containerName bash` or `docker exec -it containerName /bin/sh` will land you.
WORKDIR /workforcehub

# Copy your code to the Docker working directory.
COPY . .

# Install the project dependencies.
RUN pip install -r requirements.txt
# COPY init.sql /docker-entrypoint-initdb.d/


# Set environmental variables: we will set database credentials and other sensitive information in the docker-compose file.
# - `PYTHONUNBUFFERED` to allow logs to be immediately visible (`docker logs container`).
# - `PYTHONDONTWRITEBYTECODE` to avoid generating `.pyc` files.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
# Both `ENV key=value` and `ENV key value` are valid for setting environment variables.

# Install Vim and upgrade pip as dependencies.
RUN pip install --upgrade pip
# RUN apt-get update && apt install -y postgresql-client  vim && pip install --upgrade pip

# We are using SQLite file database, so MySQL or PostgreSQL servers are not needed in the development environment.

# Expose port 8000 for the container to listen on so that the host machine can communicate properly.
# Note that `EXPOSE` does not actually make the ports accessible. Use -p `HOST_PORT:CONTAINER_PORT` with docker run
EXPOSE 8000

# Set the default command to run at container startup.
# CMD specifies the command to run when the container is started without any arguments.
# CMD ["python", "manage.py", "runserver"]

# ENTRYPOINT sets the primary command that is executed when the container starts.
# It is similar to CMD but does not allow the command to be overridden at runtime. is the default command to run at container startup but we will use docker-compose to override it.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
