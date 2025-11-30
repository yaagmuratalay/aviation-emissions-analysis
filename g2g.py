# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 21:43:30 2025

@author: PC
"""

import pandas as pd
xls= pd.ExcelFile("g2g.xlsx")
df= pd.read_excel("g2g.xlsx", engine="openpyxl",sheet_name="DATA")
print(xls.sheet_names)


df = df[["MARKET_SEGMENT", "FLIGHT_PHASE", 
         "NB_FLIGHTS", "CO2_TONS", "NOX_KG", "SOX_KG"]]

    
num_cols = ["NB_FLIGHTS", "CO2_TONS", "NOX_KG", "SOX_KG"]

for col in num_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "", regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["CO2_PF"]=df["CO2_TONS"] / df["NB_FLIGHTS"]
df["NOX_PF"]=df["NOX_KG"] / df["NB_FLIGHTS"]
df["SOX_PF"]=df["SOX_KG"] / df["NB_FLIGHTS"]
df.dtypes


pivot_co2= df.pivot_table(
    values= "CO2_PF",
    index="MARKET_SEGMENT",
    columns="FLIGHT_PHASE",
    aggfunc="mean")
pivot_co2

pivot_nox= df.pivot_table(
    values= "NOX_PF",
    index="MARKET_SEGMENT",
    columns="FLIGHT_PHASE",
    aggfunc="mean")
pivot_nox

pivot_sox= df.pivot_table(
    values= "SOX_PF",
    index="MARKET_SEGMENT",
    columns="FLIGHT_PHASE",
    aggfunc="mean")
pivot_sox

from scipy.stats import levene

levene(df["CO2_PF"][df["MARKET_SEGMENT"]=="cargo"],
       df["CO2_PF"][df["MARKET_SEGMENT"]=="mainline"],
       df["CO2_PF"][df["MARKET_SEGMENT"]=="lowcost"])


import numpy as np

df = df[df["CO2_PF"] > 0].copy()
df["log_CO2_PF"] = np.log(df["CO2_PF"])

levene(df["log_CO2_PF"][df["MARKET_SEGMENT"]=="cargo"],
       df["log_CO2_PF"][df["MARKET_SEGMENT"]=="mainline"],
       df["log_CO2_PF"][df["MARKET_SEGMENT"]=="lowcost"])




import statsmodels.api as sm
from statsmodels.formula.api import ols

model = ols(
    "log_CO2_PF ~ C(MARKET_SEGMENT) * C(FLIGHT_PHASE)",
    data=df
).fit()

anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
sns.heatmap(pivot_co2,
            annot=True,
            fmt=".2f",
            cmap="viridis",
            linewidths=0.5,
            linecolor="gray")
plt.title("CO2 emissions per flight by market segment x flight phase"
          )
plt.xlabel("flight phase")
plt.ylabel("market segment")
plt.show()



levene(df["NOX_PF"][df["MARKET_SEGMENT"]=="cargo"],
       df["NOX_PF"][df["MARKET_SEGMENT"]=="mainline"],
       df["NOX_PF"][df["MARKET_SEGMENT"]=="lowcost"])

df = df[df["NOX_PF"] > 0].copy()
df["log_NOX_PF"] = np.log(df["NOX_PF"])

levene(df["log_NOX_PF"][df["MARKET_SEGMENT"]=="cargo"],
       df["log_NOX_PF"][df["MARKET_SEGMENT"]=="mainline"],
       df["log_NOX_PF"][df["MARKET_SEGMENT"]=="lowcost"])

model = ols(
    "log_NOX_PF ~ C(MARKET_SEGMENT) * C(FLIGHT_PHASE)",
    data=df
).fit()

anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)

plt.figure(figsize=(12,6))
sns.heatmap(pivot_nox,
            annot=True,
            fmt=".2f",
            cmap="viridis",
            linewidths=0.5,
            linecolor="gray")
plt.title("NOX emissions per flight by market segment x flight phase"
          )
plt.xlabel("flight phase")
plt.ylabel("market segment")
plt.show()


levene(df["SOX_PF"][df["MARKET_SEGMENT"]=="cargo"],
       df["SOX_PF"][df["MARKET_SEGMENT"]=="mainline"],
       df["SOX_PF"][df["MARKET_SEGMENT"]=="lowcost"])


df = df[df["SOX_PF"] > 0].copy()
df["log_SOX_PF"] = np.log(df["SOX_PF"])

levene(df["log_SOX_PF"][df["MARKET_SEGMENT"]=="cargo"],
       df["log_SOX_PF"][df["MARKET_SEGMENT"]=="mainline"],
       df["log_SOX_PF"][df["MARKET_SEGMENT"]=="lowcost"])

plt.figure(figsize=(12,6))
sns.heatmap(pivot_sox,
            annot=True,
            fmt=".2f",
            cmap="viridis",
            linewidths=0.5,
            linecolor="gray")
plt.title("SOX emissions per flight by market segment x flight phase"
          )
plt.xlabel("flight phase")
plt.ylabel("market segment")
plt.show()


total_co2_baseline= df["CO2_TONS"].sum()
co2_by_segment_baseline= df.groupby("MARKET_SEGMENT")["CO2_TONS"].sum()
df_scenario = df.copy()


mask_cruise = df_scenario["FLIGHT_PHASE"] == "cruise"
df_scenario.loc[mask_cruise, "CO2_TONS"] = df_scenario.loc[mask_cruise, "CO2_TONS"] * 0.90


df_scenario["CO2_PF"] = df_scenario["CO2_TONS"] / df_scenario["NB_FLIGHTS"]


total_co2_scenario = df_scenario["CO2_TONS"].sum()


co2_by_segment_scenario = df_scenario.groupby("MARKET_SEGMENT")["CO2_TONS"].sum()

print("Toplam CO2 (scenario):", total_co2_scenario)
print("\nSegment bazında CO2 (scenario):")
print(co2_by_segment_scenario)


summary = pd.DataFrame({
    "CO2_baseline": co2_by_segment_baseline,
    "CO2_scenario": co2_by_segment_scenario
})

summary["absolute_change"] = summary["CO2_scenario"] - summary["CO2_baseline"]
summary["percent_change_%"] = (summary["absolute_change"] / summary["CO2_baseline"]) * 100

print(summary)
print("\nToplam CO2 değişimi:")
print("Baseline:", total_co2_baseline)
print("Scenario:", total_co2_scenario)
print("Mutlak değişim:", total_co2_scenario - total_co2_baseline)
print("Yüzde değişim (%):", (total_co2_scenario - total_co2_baseline) / total_co2_baseline * 100)



segments = summary.index


baseline_vals = summary["CO2_baseline"].values
scenario_vals = summary["CO2_scenario"].values


x = np.arange(len(segments))
width = 0.35

plt.figure(figsize=(14,6))


plt.bar(x - width/2, baseline_vals, width, label="Baseline")


plt.bar(x + width/2, scenario_vals, width, label="Scenario (Cruise –10%)")

plt.title("Baseline vs Scenario CO₂ Emissions\n(Cruise Phase 10% Reduction)")
plt.xlabel("Market Segment")
plt.ylabel("Total CO₂ Emissions (tons)")


plt.xticks(x, segments, rotation=45)

plt.legend()
plt.tight_layout()
plt.show()