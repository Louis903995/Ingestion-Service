import pandas as pd

# 1. Charger le CSV
df = pd.read_csv("tickets.csv", parse_dates=["date"])

# 2. Choisir la catégorie à prédire
categorie = "Boisson"  # Change ici selon la catégorie souhaitée

# 3. Filtrer et agréger par date
df_cat = df[df["catégorie"] == categorie]
df_daily = df_cat.groupby("date").montant.sum().reset_index()

# 4. Adapter pour Prophet
df_prophet = df_daily.rename(columns={"date": "ds", "montant": "y"})

# 5. Sauvegarder pour le script Prophet
df_prophet.to_csv("df_prophet_boisson.csv", index=False)
print(df_prophet.tail())