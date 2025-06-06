FROM ghcr.io/astral-sh/uv:python3.8-bookworm

# Set working directory
WORKDIR /app

# Copy project files
COPY ./main.py .
COPY ./requirements.txt .
COPY ./models ./models

# Expose port for documentation
EXPOSE 30000

# Install dependencies using uv (this uses the system Python environment)
RUN uv pip install --system -r requirements.txt

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
