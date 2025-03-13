FROM python:3.12-slim

RUN pip install uv
WORKDIR /app
RUN python3 -m venv .venv
RUN . .venv/bin/activate
COPY pyproject.toml uv.lock requirements.txt src/ ./
RUN uv add -r requirements.txt
EXPOSE 8000
CMD ["bash"]
# CMD ["./.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]