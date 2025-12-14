#!/usr/bin/env python3
"""
Energy Analysis Script
Analyzes energy consumption metrics from LLM inference results
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import argparse


class EnergyAnalyzer:
    def __init__(self, results_dir: str = "../results"):
        self.results_dir = Path(results_dir)
        self.data = []
        
    def load_results(self, pattern: str = "*.json"):
        """Load all result JSON files"""
        print(f"📂 Loading results from {self.results_dir}...")
        
        result_files = list(self.results_dir.rglob(pattern))
        
        for file_path in result_files:
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    # Only include if energy data is available
                    if 'estimatedEnergyJ' in data and data['estimatedEnergyJ'] is not None:
                        self.data.append(data)
            except Exception as e:
                print(f"⚠️  Error loading {file_path}: {e}")
        
        print(f"✅ Loaded {len(self.data)} results with energy data")
        return pd.DataFrame(self.data)
    
    def calculate_energy_per_token(self, df: pd.DataFrame):
        """Calculate energy per token metrics"""
        df['energyPerToken'] = df['estimatedEnergyJ'] / df['totalTokens']
        df['energyPerOutputToken'] = df['estimatedEnergyJ'] / df['generatedTokens']
        return df
    
    def analyze_energy_distribution(self, df: pd.DataFrame):
        """Analyze overall energy distribution"""
        print("\n📊 Energy Consumption Analysis")
        print("=" * 60)
        
        print(f"Total Energy Consumed: {df['estimatedEnergyJ'].sum():.2f} J")
        print(f"Average Energy per Inference: {df['estimatedEnergyJ'].mean():.3f} J")
        print(f"Std Dev: {df['estimatedEnergyJ'].std():.3f} J")
        print(f"Min: {df['estimatedEnergyJ'].min():.3f} J")
        print(f"Max: {df['estimatedEnergyJ'].max():.3f} J")
        
        if 'energyPerToken' in df.columns:
            print(f"\nAverage Energy per Token: {df['energyPerToken'].mean():.4f} J/token")
            print(f"Average Energy per Output Token: {df['energyPerOutputToken'].mean():.4f} J/token")
    
    def analyze_by_prompt_type(self, df: pd.DataFrame):
        """Analyze energy by prompt category"""
        print("\n📊 Energy by Prompt Type")
        print("=" * 60)
        
        if 'category' in df.columns:
            grouped = df.groupby('category').agg({
                'estimatedEnergyJ': ['mean', 'std', 'sum'],
                'energyPerToken': ['mean', 'std']
            }).round(4)
            
            print(grouped)
    
    def analyze_energy_vs_latency(self, df: pd.DataFrame):
        """Analyze relationship between energy and latency"""
        print("\n📊 Energy vs Latency Correlation")
        print("=" * 60)
        
        correlation = df['estimatedEnergyJ'].corr(df['totalTime'])
        print(f"Correlation (energy vs latency): {correlation:.3f}")
        
        # Energy efficiency (tokens per joule)
        df['tokensPerJoule'] = df['totalTokens'] / df['estimatedEnergyJ']
        print(f"\nAverage Efficiency: {df['tokensPerJoule'].mean():.2f} tokens/J")
    
    def analyze_by_response_length(self, df: pd.DataFrame):
        """Analyze how response length affects energy"""
        print("\n📊 Energy vs Response Length")
        print("=" * 60)
        
        correlation = df['estimatedEnergyJ'].corr(df['generatedTokens'])
        print(f"Correlation (energy vs output tokens): {correlation:.3f}")
        
        # Bin by response length
        df['response_bin'] = pd.cut(df['generatedTokens'], 
                                     bins=5, 
                                     labels=['Very Short', 'Short', 'Medium', 'Long', 'Very Long'])
        
        length_analysis = df.groupby('response_bin').agg({
            'estimatedEnergyJ': ['mean', 'std'],
            'energyPerToken': ['mean']
        }).round(4)
        
        print("\nBy Response Length:")
        print(length_analysis)
    
    def analyze_keyword_impact(self, df: pd.DataFrame):
        """Analyze energy impact of specific keywords"""
        print("\n📊 Keyword Impact on Energy")
        print("=" * 60)
        
        keywords = ['explain', 'analyze', 'describe', 'write', 'detail']
        
        results = []
        for keyword in keywords:
            with_kw = df[df['promptText'].str.contains(keyword, case=False, na=False)]
            without_kw = df[~df['promptText'].str.contains(keyword, case=False, na=False)]
            
            if len(with_kw) > 0 and len(without_kw) > 0:
                avg_with = with_kw['estimatedEnergyJ'].mean()
                avg_without = without_kw['estimatedEnergyJ'].mean()
                diff_pct = ((avg_with - avg_without) / avg_without) * 100
                
                results.append({
                    'keyword': keyword,
                    'with': avg_with,
                    'without': avg_without,
                    'diff_pct': diff_pct,
                    'n_with': len(with_kw)
                })
        
        results_df = pd.DataFrame(results)
        print(results_df.to_string(index=False))
    
    def calculate_battery_impact(self, df: pd.DataFrame):
        """Calculate battery drain implications"""
        print("\n📊 Battery Impact Analysis")
        print("=" * 60)
        
        # iPhone 16 Pro Max: 4,685 mAh @ 3.7V ≈ 62.4 Wh ≈ 224,640 J
        total_battery_j = 224_640
        
        avg_energy = df['estimatedEnergyJ'].mean()
        inferences_per_charge = total_battery_j / avg_energy
        
        print(f"Average Energy per Inference: {avg_energy:.2f} J")
        print(f"Estimated Inferences per Full Charge: {inferences_per_charge:.0f}")
        print(f"Battery % per Inference: {(avg_energy/total_battery_j)*100:.3f}%")
        
        # Time estimates
        if 'totalTime' in df.columns:
            avg_time = df['totalTime'].mean()
            total_time_hours = (inferences_per_charge * avg_time) / 3600
            print(f"Continuous Operation Time: {total_time_hours:.1f} hours")
    
    def visualize_energy_metrics(self, df: pd.DataFrame, output_dir: Path):
        """Create energy visualization charts"""
        print("\n📈 Creating visualizations...")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        sns.set_style("whitegrid")
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Energy distribution
        axes[0, 0].hist(df['estimatedEnergyJ'], bins=30, edgecolor='black', alpha=0.7, color='red')
        axes[0, 0].set_xlabel('Energy (J)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Energy Consumption Distribution')
        
        # 2. Energy vs Latency
        axes[0, 1].scatter(df['totalTime'], df['estimatedEnergyJ'], alpha=0.5, color='orange')
        axes[0, 1].set_xlabel('Total Time (s)')
        axes[0, 1].set_ylabel('Energy (J)')
        axes[0, 1].set_title('Energy vs Latency')
        
        # Add trend line
        z = np.polyfit(df['totalTime'], df['estimatedEnergyJ'], 1)
        p = np.poly1d(z)
        axes[0, 1].plot(df['totalTime'], p(df['totalTime']), "r--", alpha=0.8)
        
        # 3. Energy vs Output Length
        axes[1, 0].scatter(df['generatedTokens'], df['estimatedEnergyJ'], alpha=0.5, color='green')
        axes[1, 0].set_xlabel('Generated Tokens')
        axes[1, 0].set_ylabel('Energy (J)')
        axes[1, 0].set_title('Energy vs Response Length')
        
        # 4. Energy per token
        if 'energyPerToken' in df.columns:
            axes[1, 1].hist(df['energyPerToken'], bins=30, edgecolor='black', alpha=0.7, color='purple')
            axes[1, 1].set_xlabel('Energy per Token (J/token)')
            axes[1, 1].set_ylabel('Frequency')
            axes[1, 1].set_title('Energy Efficiency Distribution')
        
        plt.tight_layout()
        plt.savefig(output_dir / 'energy_overview.png', dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {output_dir / 'energy_overview.png'}")
        
        # Category comparison if available
        if 'category' in df.columns:
            plt.figure(figsize=(12, 6))
            df.boxplot(column='estimatedEnergyJ', by='category', ax=plt.gca())
            plt.title('Energy Consumption by Prompt Category')
            plt.suptitle('')
            plt.xlabel('Category')
            plt.ylabel('Energy (J)')
            plt.tight_layout()
            plt.savefig(output_dir / 'energy_by_category.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {output_dir / 'energy_by_category.png'}")
    
    def generate_report(self, df: pd.DataFrame, output_path: Path):
        """Generate comprehensive energy report"""
        print("\n📝 Generating report...")
        
        with open(output_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("ENERGY CONSUMPTION ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total Inferences Analyzed: {len(df)}\n")
            f.write(f"Analysis Date: {pd.Timestamp.now()}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("SUMMARY STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(df[['estimatedEnergyJ', 'energyPerToken', 'tokensPerJoule']].describe().to_string())
            f.write("\n\n")
            
            # Battery impact
            total_battery_j = 224_640
            avg_energy = df['estimatedEnergyJ'].mean()
            inferences_per_charge = total_battery_j / avg_energy
            
            f.write("-" * 80 + "\n")
            f.write("BATTERY IMPACT\n")
            f.write("-" * 80 + "\n")
            f.write(f"Inferences per Full Charge: {inferences_per_charge:.0f}\n")
            f.write(f"Battery % per Inference: {(avg_energy/total_battery_j)*100:.3f}%\n\n")
            
            if 'category' in df.columns:
                f.write("-" * 80 + "\n")
                f.write("BY CATEGORY\n")
                f.write("-" * 80 + "\n")
                category_stats = df.groupby('category')['estimatedEnergyJ'].describe()
                f.write(category_stats.to_string())
                f.write("\n\n")
        
        print(f"✅ Saved: {output_path}")
    
    def run_full_analysis(self, output_dir: str = "../results/analysis"):
        """Run complete energy analysis pipeline"""
        df = self.load_results()
        
        if df.empty:
            print("❌ No energy data to analyze")
            return
        
        # Calculate derived metrics
        df = self.calculate_energy_per_token(df)
        
        # Run analyses
        self.analyze_energy_distribution(df)
        self.analyze_by_prompt_type(df)
        self.analyze_energy_vs_latency(df)
        self.analyze_by_response_length(df)
        self.analyze_keyword_impact(df)
        self.calculate_battery_impact(df)
        
        # Generate outputs
        output_path = Path(output_dir)
        self.visualize_energy_metrics(df, output_path)
        self.generate_report(df, output_path / 'energy_report.txt')
        
        # Save processed data
        df.to_csv(output_path / 'energy_data.csv', index=False)
        print(f"\n✅ Analysis complete! Results saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Analyze LLM inference energy consumption')
    parser.add_argument('--results-dir', default='../results', help='Directory containing result JSON files')
    parser.add_argument('--output-dir', default='../results/analysis', help='Output directory for analysis')
    
    args = parser.parse_args()
    
    analyzer = EnergyAnalyzer(args.results_dir)
    analyzer.run_full_analysis(args.output_dir)


if __name__ == "__main__":
    main()

