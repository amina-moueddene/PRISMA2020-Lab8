import pandas as pd
import numpy as np

# 1. Chargement des grilles d'extraction et de Quality Assessment (22 études)
df_ext = pd.read_csv("data/fulltext_extraction_22_studies.csv")
df_qa = pd.read_csv("data/quality_assessment_Q1-Q10.csv")

# Fusion sur l'identifiant unique 'record'
df = pd.merge(df_ext, df_qa, on="record", suffixes=("", "_qa"))

# 2. Normalisation des termes clés
platform_map = {
    "Airborne (manned)": "Airborne",
    "Airborne": "Airborne",
    "UAV (multirotor)": "UAV",
    "UAV": "UAV",
    "Satellite": "Satellite",
    "Satellite + airborne (reference)": "Satellite + Airborne"
}

df["platform_norm"] = df["platform"].map(platform_map).fillna(df["platform"])

# 3. Statistiques descriptives de Quality Assessment (Q1-Q10 sur 20)
print("=== Synthèse Quality Assessment (22 études) ===")
print(f"Médiane globale : {df['quality_total_out_of_20'].median():.1f} / 20")
print(f"Moyenne globale : {df['quality_total_out_of_20'].mean():.2f} / 20")
print(f"Min / Max       : {df['quality_total_out_of_20'].min()} / {df['quality_total_out_of_20'].max()}")

print("\n=== Médiane QA par famille d'IA ===")
print(df.groupby("ai_family")["quality_total_out_of_20"].agg(["count", "median", "mean"]))

print("\n=== Répartition par niveau de validation (V0-V4) ===")
print(df["validation_level"].value_counts().sort_index())

# 4. Export du jeu de données consolidé prêt pour le Lab 9
df.to_csv("data/lab8_consolidated_extraction_qa.csv", index=False)
print("\nFichier consolidé exporté : data/lab8_consolidated_extraction_qa.csv")
