# Start with a Python OS
FROM python:3.9-slim

# Set the working folder inside the container
WORKDIR /code

# Copy the shopping list first (Caching trick!)
COPY ./requirements.txt /code/requirements.txt

# Install the tools
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the code
COPY ./app /code/app

# The Command to run when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]