
![architecture](https://github.com/saqib4975/AIQ_data/assets/146154778/c9498847-ef8b-49f8-95e8-8dfb3228eff7)


# Frist Step
first let set up the docker file where all our depencies for code we will use Pyhton 3.9 

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

# Run the following command to build the image 
docker build -t AIQ
# Run Docker compose yaml file and run in the bcakground 
Docker compoes up -d 

####################################################################################






