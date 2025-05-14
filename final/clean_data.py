# 1. Load Libraries and Dataset
import pandas as pd
df = pd.read_csv("ShartankIndiaAllPitches.csv")
df.columns = df.columns.str.strip()

# 2. Add New Columns
investor_columns = ['Anupam', 'Ashneer', 'Namita', 'Aman', 'Peyush', 'Vineeta', 'Ghazal']
df["Investor Count"] = df[investor_columns].apply(lambda row: row.str.upper().eq("Y").sum(), axis=1)
df["Got Investment"] = df["Investor Count"] > 0
# Remove the percentage sign and convert to numeric
df['Equity'] = df['Equity'].replace('%', '', regex=True).astype(float) / 100


# 3. Tag Business Domains
def classify_domain(idea):
    idea = idea.lower()
    if any(word in idea for word in ["food", "cafe", "snack", "beverage"]):
        return "Food & Beverage"
    elif any(word in idea for word in ["fashion", "clothing", "wear", "apparel"]):
        return "Fashion & Apparel"
    elif any(word in idea for word in ["tech", "platform", "app", "software"]):
        return "Technology"
    elif any(word in idea for word in ["skin", "beauty", "cosmetic", "makeup"]):
        return "Beauty & Wellness"
    elif any(word in idea for word in ["health", "fit", "yoga", "therapy"]):
        return "Health & Fitness"
    elif any(word in idea for word in ["edu", "school", "learning", "student"]):
        return "Education"
    elif any(word in idea for word in ["pet", "dog", "animal"]):
        return "Pets"
    elif any(word in idea for word in ["eco", "sustain", "green", "recycle"]):
        return "Sustainability"
    else:
        return "Other"

df["Domain"] = df["Idea"].apply(classify_domain)

# 4. Save for Tableau
df.to_csv("Final_SharkTank_Cleaned.csv", index=False)
print(df.head())  # Check the first few rows of the final dataset

# 5. Analysis Summaries

# Total investments per investor
investor_summary = df[investor_columns].apply(lambda col: col.str.upper().eq("Y").sum()).sort_values(ascending=False)
print("\n🦈 Top Investors:\n", investor_summary)

# Total investment amount per domain
domain_investment = df.groupby("Domain")["Investment Amount (In Lakhs INR)"].sum().sort_values(ascending=False)
print("\n💰 Total Investment per Domain:\n", domain_investment)

# Average investment per domain
avg_domain_investment = df.groupby("Domain")["Investment Amount (In Lakhs INR)"].mean().sort_values(ascending=False)
print("\n📊 Avg Investment per Domain:\n", avg_domain_investment)

# Number of pitches per domain
pitch_count_per_domain = df["Domain"].value_counts()
print("\n📈 Pitch Count per Domain:\n", pitch_count_per_domain)

avg_equity_per_domain = df.groupby("Domain")["Equity"].mean().sort_values(ascending=False)
print("\n⚖️ Avg Equity per Domain:\n", avg_equity_per_domain)


# Investor interest by domain
domain_investor_interest = df.groupby("Domain")["Investor Count"].mean().sort_values(ascending=False)
print("\n🔥 Avg Investor Count per Domain:\n", domain_investor_interest)
