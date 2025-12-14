#!/usr/bin/env python3
"""
Train Prediction Model for Prompt Optimization
Uses experimental data to learn latency/energy coefficients
"""

import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

print("=" * 80)
print("TRAINING PREDICTION MODEL")
print("=" * 80)

# Load experimental data
data_path = Path(__file__).parent.parent / 'results' / 'experimental_data_sample.json'
with open(data_path) as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(f"\n📊 Loaded {len(df)} experimental samples")
print(f"Categories: {df['category'].unique().tolist()}")

# Feature engineering
print("\n🔧 Engineering features...")

# Encode categories
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# Create features for optimization
df['has_verbose'] = df['prompt'].str.contains('please|detail|thoroughly|comprehensive', 
                                               case=False, regex=True).astype(int)
df['word_count'] = df['prompt'].apply(lambda x: len(x.split()))
df['char_count'] = df['prompt_length']

# Separate training features
X_features = df[['prompt_length', 'prompt_tokens', 'word_count', 
                 'has_verbose', 'category_encoded']]
y_latency = df['total_time_ms']
y_energy = df['energy_joules']
y_throughput = df['tokens_per_second']

print(f"Features: {X_features.columns.tolist()}")
print(f"Samples: {len(X_features)}")

# Train models
print("\n🤖 Training models...")

# Model 1: Latency prediction
latency_model = LinearRegression()
latency_model.fit(X_features, y_latency)
latency_score = latency_model.score(X_features, y_latency)

print(f"\n✅ Latency Model (R² = {latency_score:.3f})")
print(f"   Coefficients:")
for feature, coef in zip(X_features.columns, latency_model.coef_):
    print(f"      {feature:20s}: {coef:8.4f}")
print(f"   Intercept: {latency_model.intercept_:.4f}")

# Model 2: Energy prediction
energy_model = LinearRegression()
energy_model.fit(X_features, y_energy)
energy_score = energy_model.score(X_features, y_energy)

print(f"\n✅ Energy Model (R² = {energy_score:.3f})")
print(f"   Coefficients:")
for feature, coef in zip(X_features.columns, energy_model.coef_):
    print(f"      {feature:20s}: {coef:8.4f}")
print(f"   Intercept: {energy_model.intercept_:.4f}")

# Model 3: Throughput prediction
throughput_model = LinearRegression()
throughput_model.fit(X_features, y_throughput)
throughput_score = throughput_model.score(X_features, y_throughput)

print(f"\n✅ Throughput Model (R² = {throughput_score:.3f})")
print(f"   Coefficients:")
for feature, coef in zip(X_features.columns, throughput_model.coef_):
    print(f"      {feature:20s}: {coef:8.4f}")
print(f"   Intercept: {throughput_model.intercept_:.4f}")

# Simplified coefficients for Swift implementation
print("\n" + "=" * 80)
print("SIMPLIFIED COEFFICIENTS FOR iOS APP")
print("=" * 80)

# Calculate per-character and per-token impacts
char_impact_latency = latency_model.coef_[0]  # prompt_length coefficient
token_impact_latency = latency_model.coef_[1]  # prompt_tokens coefficient
verbose_penalty_latency = latency_model.coef_[3]  # has_verbose coefficient

char_impact_energy = energy_model.coef_[0]
token_impact_energy = energy_model.coef_[1]
verbose_penalty_energy = energy_model.coef_[3]

print(f"""
📱 USE THESE IN YOUR SWIFT CODE:

// Latency prediction (ms)
let baseLatency = {latency_model.intercept_:.2f}
let latencyPerChar = {char_impact_latency:.4f}
let latencyPerToken = {token_impact_latency:.4f}
let verbosePenalty = {verbose_penalty_latency:.2f}

// Energy prediction (J)
let baseEnergy = {energy_model.intercept_:.2f}
let energyPerChar = {char_impact_energy:.5f}
let energyPerToken = {token_impact_energy:.4f}
let verboseEnergyPenalty = {verbose_penalty_energy:.3f}

// Model performance
// Latency R² = {latency_score:.3f}
// Energy R² = {energy_score:.3f}
""")

# Generate comparison: before vs after optimization
print("\n" + "=" * 80)
print("OPTIMIZATION IMPACT CALCULATION")
print("=" * 80)

# Compare optimized vs non-optimized prompts
optimized_samples = df[df['category'].str.contains('optimized')]
original_samples = df[~df['category'].str.contains('optimized')]

if len(optimized_samples) > 0 and len(original_samples) > 0:
    avg_latency_reduction = (original_samples['total_time_ms'].mean() - 
                            optimized_samples['total_time_ms'].mean()) / original_samples['total_time_ms'].mean()
    
    avg_energy_reduction = (original_samples['energy_joules'].mean() - 
                           optimized_samples['energy_joules'].mean()) / original_samples['energy_joules'].mean()
    
    print(f"""
Average Optimization Impact:
  Latency Reduction: {avg_latency_reduction*100:.1f}%
  Energy Reduction:  {avg_energy_reduction*100:.1f}%

🎯 USE THIS IN YOUR PRESENTATION:
  "My trained model shows optimization achieves {avg_latency_reduction*100:.0f}% latency 
   and {avg_energy_reduction*100:.0f}% energy reduction on average"
""")

# Save model summary
output_path = Path(__file__).parent / 'model_summary.txt'
with open(output_path, 'w') as f:
    f.write("TRAINED MODEL COEFFICIENTS\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Training samples: {len(df)}\n")
    f.write(f"Latency R²: {latency_score:.3f}\n")
    f.write(f"Energy R²: {energy_score:.3f}\n\n")
    f.write("Latency coefficients:\n")
    for feature, coef in zip(X_features.columns, latency_model.coef_):
        f.write(f"  {feature}: {coef:.4f}\n")
    f.write(f"\nEnergy coefficients:\n")
    for feature, coef in zip(X_features.columns, energy_model.coef_):
        f.write(f"  {feature}: {coef:.4f}\n")

print(f"\n✅ Model summary saved to: {output_path}")
print("\n" + "=" * 80)
print("✅ TRAINING COMPLETE!")
print("=" * 80)
print("\nNext: Update your Swift code with these coefficients!")

