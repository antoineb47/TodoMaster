# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Create directory for static files
RUN mkdir -p /code/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Create and set permissions for entrypoint script
RUN echo '#!/bin/bash\npython manage.py migrate\npython manage.py collectstatic --noinput\npython manage.py runserver 0.0.0.0:8000' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["/entrypoint.sh"]
