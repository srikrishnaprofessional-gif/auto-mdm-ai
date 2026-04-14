from app.agents.context import AgentContext
from app.agents.schema_agent import run_schema_agent
from app.agents.mdm_agent import run_mdm_agent
from app.agents.quality_agent import run_quality_agent
from app.agents.sync_agent import run_sync_agent

from app.vector_memory import store_memory

def orchestrate(df):
    context = AgentContext()

    # -------------------------
    # SCHEMA AGENT
    # -------------------------
    schema = run_schema_agent(list(df.columns))
    context.update("schema", schema)
    context.send("SchemaAgent", schema)

    # -------------------------
    # MDM AGENT
    # -------------------------
    mdm = run_mdm_agent(df.head(5).to_dict())
    context.update("mdm", mdm)
    context.send("MDMAgent", mdm)

    # -------------------------
    # QUALITY AGENT
    # -------------------------
    quality = run_quality_agent(df.head(5).to_dict())
    context.update("quality", quality)
    context.send("QualityAgent", quality)

    # -------------------------
    # SYNC
    # -------------------------
    df = run_sync_agent(df)

    # -------------------------
    # STORE MEMORY (IMPORTANT 🔥)
    # -------------------------
    decision_text = f"""
    Schema Decision: {schema}
    MDM Decision: {mdm}
    Quality Insight: {quality}
    """

    store_memory(decision_text)

    return df, context.memory, context.get_messages()