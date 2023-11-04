# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container and install the required dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Flask application code into the container
COPY . .

# add environment variables
ENV MYSQL_HOST=10.1.1.13
ENV MYSQL_USER=root
ENV MYSQL_PORT=3306
ENV MYSQL_PASSWORD=abogoboga
ENV MYSQL_DB=ecoguardian_db
# Expose the port your Flask app will run on
EXPOSE 5000

# Define the command to run your Flask application
# CMD ["python", "run.py"]
#use gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app"]