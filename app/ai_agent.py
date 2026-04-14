from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # fast + powerful
        messages=[
            {"role": "system", "content": "You are an autonomous data engineering AI agent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def decide_schema_mapping(columns):
    prompt = f"""
    Given these columns: {columns}
    Suggest a unified schema.
    """
    return ask_llm(prompt)


def decide_conflict_strategy(sample_data):
    prompt = f"""
    Analyze this data: {sample_data}
    Decide conflict resolution strategy.
    """
    return ask_llm(prompt)


def analyze_data_quality(df_sample):
    prompt = f"""
    Analyze this dataset: {df_sample}
    Identify quality issues.
    """
    return ask_llm(prompt)