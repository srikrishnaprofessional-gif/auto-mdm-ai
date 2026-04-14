import pandas as pd
import random
from datetime import datetime, timedelta
import uuid

names = ["John Doe","Alice Smith","Bob Brown","Emma Watson","Liam Noah","Sophia Lee"]
domains = ["gmail.com","yahoo.com","outlook.com"]

def random_email(name):
    return name.replace(" ", "").lower() + str(random.randint(1,50)) + "@" + random.choice(domains)

def random_date():
    return datetime.now() - timedelta(days=random.randint(1,365))

def generate_data(n=50):
    base_users = []

    for i in range(n):
        name = random.choice(names)

        # 20% duplicates
        if i % 5 == 0:
            email = "duplicate@gmail.com"
        else:
            email = random_email(name)

        base_users.append({"name": name, "email": email})

    base_df = pd.DataFrame(base_users).drop_duplicates()

    # -------------------------
    # STRIPE
    # -------------------------
    stripe = base_df.copy()
    stripe["customer_id"] = ["cus_" + uuid.uuid4().hex[:6] for _ in range(len(stripe))]
    stripe["amount"] = [random.randint(10,500) for _ in range(len(stripe))]
    stripe["payment_status"] = [random.choice(["paid","pending","failed"]) for _ in range(len(stripe))]
    stripe["created_at"] = [random_date() for _ in range(len(stripe))]

    # -------------------------
    # HUBSPOT
    # -------------------------
    hubspot = base_df.copy()
    hubspot = hubspot.rename(columns={"name":"full_name","email":"contact_email"})
    hubspot["company"] = [random.choice(["Google","Amazon","Tesla"]) for _ in range(len(hubspot))]
    hubspot["lifecycle_stage"] = [random.choice(["lead","customer"]) for _ in range(len(hubspot))]

    # -------------------------
    # QUICKBOOKS
    # -------------------------
    quickbooks = base_df.copy()
    quickbooks["invoice_id"] = ["inv_" + uuid.uuid4().hex[:6] for _ in range(len(quickbooks))]
    quickbooks["invoice_amount"] = [random.randint(100,5000) for _ in range(len(quickbooks))]
    quickbooks["status"] = [random.choice(["paid","unpaid"]) for _ in range(len(quickbooks))]

    return stripe, hubspot, quickbooks