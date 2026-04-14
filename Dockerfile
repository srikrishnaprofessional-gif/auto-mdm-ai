FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pandas streamlit groq chromadb kafka-python python-dotenv

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/dashboard.py"]