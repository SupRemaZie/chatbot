.PHONY: build run clean


up:
	docker build -t ollama-mistral-python .
	docker run --rm -p 11434:11434 -p 8501:8501 ollama-mistral-python

clean:
	docker rmi ollama-mistral-python || true
