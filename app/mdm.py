def resolve_conflicts(df):
    return df.drop_duplicates(subset=["email"])