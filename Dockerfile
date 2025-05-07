FROM python:3.10

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

ENV API_KEY=your-api-key
ENV API_SECRET=your-secret-key
# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project
COPY . /app/

# Default run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
