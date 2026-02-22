FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \
    apt-get update -y && \
    apt-get install -y libxcb1 libx11-6 libxext6 libxrender1 libgl1 && \
    apt-get install -y libglib2.0-0 && \
    rm -rf /root/.cache/pip

COPY Chatbot/ ./Chatbot/
COPY RAGAgent/ ./RAGAgent/
COPY navigation.py ./navigation.py
COPY config.toml /root/.streamlit/config.toml

EXPOSE 8501
CMD ["streamlit", "run", "navigation.py", "--server.port=8501", "--server.address=0.0.0.0"]