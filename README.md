# Challange_DE
first let set up the docker file where all our depencies will code we will use Pyhton 3.9 

# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run python script when the container launches
CMD ["python", "./main.py"]

after that we'll right a docker-compose.ymal file which will setup our postgre enviroment to store data from API 
All credentials are provided here which we will use to manage our database  


version: "3.8"

services:
  postgres:
    image: postgres:latest
    container_name: my_postgres_db
    environment:
      POSTGRES_DB: sales_db
      POSTGRES_USER: postgres_user
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
