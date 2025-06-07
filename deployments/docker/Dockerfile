FROM ghcr.io/astral-sh/uv:python3.8-bookworm-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY ./app /app
COPY ./requirements.txt /app
COPY ./models /app/models

# Set MODEL_DIR env variable
ENV MODEL_PATH /app/models/model.pkl

# Expose port for documentation
EXPOSE 30000

# Install dependencies using uv (this uses the system Python environment)
RUN uv pip install --system -r requirements.txt

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
