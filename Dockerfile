# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable
ENV OPENAI_API_KEY #TODO Give your OpenAI API key here

# Set the command to run your Python file
CMD ["python", "execute_spider.py"]
