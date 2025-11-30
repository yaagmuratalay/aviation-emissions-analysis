# aviation-emissions-analysis
Analysis of flight-phase emissions (CO₂, NOx, SOx) using EUROCONTROL Gate-to-Gate data. Includes two-way ANOVA, heatmaps and a 10% cruise efficiency what-if scenario.

1. Project Overview
The aim of this project is to explore how emissions vary across:
Flight phases (climb, cruise, descent, taxi-in, taxi-out)
Market segments (cargo, mainline, lowcost, regional, business, other)
and to assess how operational improvements—specifically enhancing cruise efficiency—can reduce total system-wide emissions.


2. Dataset
Source: EUROCONTROL FlyingGreen – Gate-to-Gate Emission Model
Variables include:
MARKET_SEGMENT
FLIGHT_PHASE
CO2_TONS, NOX_KG, SOX_KG
NB_FLIGHTS
YEAR, MONTH
The dataset provides phase-level emissions based on real flight trajectories.


3. Data Processing
Replaced commas with dots in numeric fields
Converted emission values to numeric
Created per-flight indicators (e.g., CO2_PF)
Built pivot tables for segment × phase analysis
Applied log-transformation for statistical robustness


4. Analyses Performed
Two-Way ANOVA
Investigated effects of:
Market segment
Flight phase
Interaction effect (segment × phase)
Key finding:
Both main effects and the interaction are highly significant (p < 0.001), indicating strong differences across segments and phases.
Heatmap Visualizations;
Heatmaps were created for:
CO₂ per flight
NOx per flight
SOx per flight
Cruise and climb phases dominate emissions, especially for cargo and mainline operations.


5. What-If Scenario: 10% Cruise Efficiency Improvement
A scenario was modelled where cruise-phase emissions were reduced by 10% for all segments.
Results:
Total CO₂ decreases by 8.92%
Mainline and cargo experience the largest reductions
Regional and business show smaller reductions due to shorter cruise duration
This demonstrates that even small improvements in cruise efficiency lead to substantial environmental benefits.


6. Key Insights
Cruise phase = dominant emission source (≈ 70%)
Cargo & mainline = highest emission intensity
Log-transformed ANOVA shows strong interaction effects
Cruise efficiency improvements → large system-wide reductions


7. Future Work
Machine learning clustering (segment profiling)
PCA on emission signatures
Short-haul replacement scenarios
Taxi-out optimization modelling

