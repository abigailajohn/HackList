# --- Build stage ---
    FROM python:3.12-slim AS builder

    WORKDIR /app
    
    # Install build dependencies
    RUN apt-get update && apt-get install -y --no-install-recommends gcc
    
    # Install Python dependencies
    COPY requirements.txt .
    RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt
    
    # Copy app code
    COPY . .
    
    # --- Final stage (distroless) ---
    FROM gcr.io/distroless/base-debian12
    
    WORKDIR /app
    
    # Copy Python and site-packages from builder
    COPY --from=builder /usr/local/bin/python3 /usr/local/bin/python3
    COPY --from=builder /usr/local/lib /usr/local/lib
    COPY --from=builder /install /usr/local
    
    # Copy app code
    COPY --from=builder /app /app
    
    # Expose Streamlit port
    EXPOSE 8501
    
    # Set environment variables for Streamlit
    ENV STREAMLIT_SERVER_PORT=8501 \
        STREAMLIT_SERVER_HEADLESS=true \
        STREAMLIT_SERVER_ENABLECORS=false
    
    # Entrypoint
    ENTRYPOINT ["/usr/local/bin/python3", "-m", "streamlit", "run", "app.py"]
