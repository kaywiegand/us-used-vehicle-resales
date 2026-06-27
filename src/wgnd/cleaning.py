def safe_drop(df, columns):
    return df.drop(columns=columns, errors='ignore')

def safe_reset(df):
    return df.drop_duplicates().reset_index(drop=True)