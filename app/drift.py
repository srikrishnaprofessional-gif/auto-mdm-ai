from app.utils import log

def detect_drift(df):
    log("Detecting drift")

    if df['email'].nunique() < len(df) * 0.6:
        return "High duplication drift"
    return "No drift"