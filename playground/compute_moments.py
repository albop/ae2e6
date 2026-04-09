import dbnomics
from statsmodels.tsa.filters.hp_filter import hpfilter

# quartertly data from OECD

# country = "FRA"
country = "USA"

ids = [
    f"OECD/QNA/{country}.P5.LNBQRSA.Q", # investment
    f"OECD/QNA/{country}.B1_GS1.LNBQRSA.Q", # GDP
    f"OECD/QNA/{country}.P3.LNBQRSA.Q"
]

df = dbnomics.fetch_series(ids)[["Subject","period","value"]]
df = df.pivot_table(columns=['Subject'], index='period')
df.columns = df.columns.droplevel()
df = df.rename(columns={
        'Final consumption expenditure':'consumption',
        'Gross capital formation':'investment',
        'Gross domestic product':'production'
})

df.columns = ['consumption', 'investment', 'production']

df = df.dropna()

for c in df.columns:
    cycle, trend = hpfilter(df[c])
    df[f"{c}_cycle"] = (cycle-trend)/trend
    df[f"{c}_trend"] = trend

print(f"σ(C)/σ(Y) = {df['consumption_cycle'].std()/df['production_cycle'].std()}")
print(f"σ(I)/σ(Y) = {df['investment_cycle'].std()/df['production_cycle'].std()}")


σ(C)/σ(Y) = 0.695080232231917
σ(I)/σ(Y) = 3.320828267976735