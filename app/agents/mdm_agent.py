from app.ai_agent import ask_llm

def run_mdm_agent(sample):
    prompt = f"""
    You are a data deduplication expert.
    Suggest conflict resolution strategy for:
    {sample}
    """

    return ask_llm(prompt)