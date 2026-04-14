from app.ai_agent import ask_llm

def run_schema_agent(columns):
    prompt = f"""
    You are a schema expert.
    Standardize these fields: {columns}
    Output clean schema.
    """

    return ask_llm(prompt)