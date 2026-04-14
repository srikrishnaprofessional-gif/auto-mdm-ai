import os
import time
from datetime import datetime

from app.ingestion import generate_data
from app.schema_mapping import map_schema
from app.mdm import resolve_conflicts
from app.ai_agent import ask_llm
from app.vector_memory import store_memory

def run_agent():
    logs = []
    progress = {}

    logs.append("🔄 Generating data...")
    stripe, hubspot, quickbooks = generate_data()

    # Schema
    progress["Schema Agent"] = 20
    logs.append("🧬 Schema Agent started")

    df = map_schema(stripe, hubspot, quickbooks)
    schema = ask_llm(f"Standardize schema: {list(df.columns)}")

    logs.append("🧬 Schema completed")

    # MDM
    progress["MDM Agent"] = 40
    logs.append("🔁 Resolving duplicates")

    df = resolve_conflicts(df)
    mdm = ask_llm(f"Resolve duplicates: {df.head().to_dict()}")

    logs.append("🔁 MDM completed")

    # Quality
    progress["Quality Agent"] = 60
    logs.append("🧹 Checking data quality")

    quality = ask_llm(f"Check data quality: {df.head().to_dict()}")

    logs.append("🧹 Quality completed")

    # Sync
    progress["Sync Agent"] = 80
    logs.append("🔄 Syncing data")
    time.sleep(0.3)

    # Memory
    progress["Memory Agent"] = 100
    logs.append("💾 Storing memory")

    # 🧠 EXECUTIVE DECISIONS
    decisions = {
        "Schema Agent": {
            "summary": "Standardized schema across systems",
            "detail": schema,
            "impact": "Ensures consistent joins and integration",
            "confidence": "High"
        },
        "MDM Agent": {
            "summary": "Resolved duplicate records",
            "detail": mdm,
            "impact": "Improves data accuracy",
            "confidence": "High"
        },
        "Quality Agent": {
            "summary": "Performed data quality checks",
            "detail": quality,
            "impact": "Identifies missing/inconsistent data",
            "confidence": "Medium"
        }
    }

    store_memory(str(decisions))

    os.makedirs("output", exist_ok=True)
    filename = f"output/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)

    return df, decisions, progress, logs