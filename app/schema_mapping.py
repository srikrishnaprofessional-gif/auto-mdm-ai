import pandas as pd

def map_schema(stripe, hubspot, quickbooks):

    # -------------------------
    # STANDARDIZE COLUMN NAMES
    # -------------------------
    hubspot = hubspot.rename(columns={
        "full_name": "name",
        "contact_email": "email"
    })

    # Prefix columns to avoid clashes
    stripe = stripe.rename(columns={
        "amount": "stripe_amount",
        "payment_status": "stripe_status"
    })

    quickbooks = quickbooks.rename(columns={
        "invoice_amount": "qb_amount",
        "status": "qb_status"
    })

    # -------------------------
    # MERGE ALL DATA
    # -------------------------
    df = pd.concat([stripe, hubspot, quickbooks], ignore_index=True)

    # -------------------------
    # GOLDEN RECORD LOGIC 🔥
    # -------------------------
    def aggregate_group(group):
        return pd.Series({
            "name": group["name"].dropna().iloc[0] if "name" in group else None,
            "email": group["email"].dropna().iloc[0],

            "stripe_amount": group.get("stripe_amount", pd.Series()).max(),
            "stripe_status": group.get("stripe_status", pd.Series()).dropna().iloc[0] if "stripe_status" in group else None,

            "company": group.get("company", pd.Series()).dropna().iloc[0] if "company" in group else None,
            "lifecycle_stage": group.get("lifecycle_stage", pd.Series()).dropna().iloc[0] if "lifecycle_stage" in group else None,

            "qb_amount": group.get("qb_amount", pd.Series()).max(),
            "qb_status": group.get("qb_status", pd.Series()).dropna().iloc[0] if "qb_status" in group else None
        })

    # Group by EMAIL → single customer
    unified_df = df.groupby("email", as_index=False).apply(aggregate_group)

    # Reset index cleanly
    unified_df = unified_df.reset_index(drop=True)

    # Fill missing values
    unified_df = unified_df.fillna({
        "stripe_amount": 0,
        "qb_amount": 0,
        "company": "Unknown"
    })

    return unified_df