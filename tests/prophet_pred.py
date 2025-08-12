import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# 1. Charger les données préparées
df_prophet = pd.read_csv("df_prophet_boisson.csv", parse_dates=["ds"])

# 2. Entraîner Prophet
model = Prophet()
model.fit(df_prophet)

# 3. Générer les dates futures (30 jours de prévision)
future = model.make_future_dataframe(periods=30)

# 4. Prédire
forecast = model.predict(future)

# 5. Afficher le résultat (graphique)
fig1 = model.plot(forecast)
plt.title("Prévision des ventes Boisson")
plt.show()

# 6. Trouver la dernière date connue
last_date = df_prophet["ds"].max()
one_week_later = last_date + pd.Timedelta(days=7)
one_month_later = last_date + pd.Timedelta(days=30)

# 7. Trouver la prédiction la plus proche de 1 semaine et 1 mois après la dernière date
def get_closest_pred(forecast, target_date):
    idx = (forecast['ds'] - target_date).abs().argsort()[:1]
    return forecast.iloc[idx]['ds'].values[0], forecast.iloc[idx]['yhat'].values[0]

ds_1w, yhat_1w = get_closest_pred(forecast, one_week_later)
ds_1m, yhat_1m = get_closest_pred(forecast, one_month_later)

print(f"Montant prédit dans 1 semaine ({pd.to_datetime(ds_1w).date()}): {yhat_1w:.2f}")
print(f"Montant prédit dans 1 mois ({pd.to_datetime(ds_1m).date()}): {yhat_1m:.2f}")