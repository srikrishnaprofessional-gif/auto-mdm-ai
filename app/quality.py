from app.utils import log

def data_quality(df):
    log("Checking data quality")

    issues = []

    if df['email'].isnull().sum() > 0:
        issues.append("Missing emails")

    if df.duplicated(subset=['email']).sum() > 0:
        issues.append("Duplicates found")

    score = max(0, 100 - len(issues)*20)
    return score, issues