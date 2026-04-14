from app.utils import log

def sync_data(df):
    log("Syncing data")
    df['synced'] = True
    return df