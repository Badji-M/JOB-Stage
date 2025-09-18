# Script Python (à exécuter localement)
import pandas as pd
url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df = pd.read_csv(url, usecols=["iso_code","country","year","total_ghg"])
# Filtre l'année 2022 et pays (excl. continents / aggregates)
df2022 = df[(df["year"]==2022) & (df["iso_code"].notna()) & (df["country"].notna())]
# Total GHG en MtCO2e (OWID donne en million tonnes?)
# Vérifie l'unité dans le CSV; OWID total_ghg est en MtCO2e (tonnes CO2 eq)
# Supprime NA et garde les pays
vals = df2022["total_ghg"].dropna()
lower_2p5 = vals.quantile(0.025)
print("Nombre d'observations (pays) 2022:", len(vals))
print("2.5th percentile (MtCO2-eq):", lower_2p5)
# Pour vérifier la valeur du Sénégal
sen = df2022[df2022["country"].str.contains("Senegal", case=False)]
print(sen[["country","total_ghg"]])
