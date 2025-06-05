FROM ollama/ollama:latest

WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip make

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN ollama pull mistral
RUN ollama pull llama3.2
RUN ollama pull nomic

EXPOSE 11434 8501

CMD ["./start.sh"]
