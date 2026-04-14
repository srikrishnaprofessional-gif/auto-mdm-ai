from app.ai_agent import ask_llm

def run_quality_agent(sample):
    prompt = f"""
    You are a data quality expert.
    Identify issues in:
    {sample}
    """

    return ask_llm(prompt)