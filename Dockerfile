#Base image

FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 5000

# Write the command to run on container start
# CMD ["python", "app.py"]
CMD gunicorn -b 0.0.0.0:5000 app:app --timeout 600
