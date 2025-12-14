#!/usr/bin/env python3
"""
Latency Analysis Script
Analyzes timing metrics from LLM inference results
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict
import argparse


class LatencyAnalyzer:
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
                    self.data.append(data)
            except Exception as e:
                print(f"⚠️  Error loading {file_path}: {e}")
        
        print(f"✅ Loaded {len(self.data)} results")
        return pd.DataFrame(self.data)
    
    def analyze_by_prompt_type(self, df: pd.DataFrame):
        """Analyze latency by prompt category/type"""
        print("\n📊 Latency Analysis by Prompt Type")
        print("=" * 60)
        
        if 'category' in df.columns:
            grouped = df.groupby('category').agg({
                'totalTime': ['mean', 'std', 'min', 'max'],
                'prefillTime': ['mean', 'std'],
                'decodeTime': ['mean', 'std'],
                'tokensPerSecond': ['mean', 'std']
            }).round(3)
            
            print(grouped)
        else:
            print("No category information available")
    
    def analyze_by_prompt_length(self, df: pd.DataFrame):
        """Analyze correlation between prompt length and latency"""
        print("\n📊 Latency vs Prompt Length")
        print("=" * 60)
        
        if 'promptLength' in df.columns and 'totalTime' in df.columns:
            correlation = df['promptLength'].corr(df['totalTime'])
            print(f"Correlation (length vs latency): {correlation:.3f}")
            
            # Bin by length
            df['length_bin'] = pd.cut(df['promptLength'], bins=5, labels=['Very Short', 'Short', 'Medium', 'Long', 'Very Long'])
            length_analysis = df.groupby('length_bin').agg({
                'totalTime': ['mean', 'std'],
                'prefillTime': ['mean'],
                'decodeTime': ['mean']
            }).round(3)
            
            print("\nBy Length Bin:")
            print(length_analysis)
    
    def analyze_by_keywords(self, df: pd.DataFrame):
        """Analyze impact of specific keywords on latency"""
        print("\n📊 Keyword Impact on Latency")
        print("=" * 60)
        
        keywords = ['explain', 'analyze', 'describe', 'write', 'create']
        
        for keyword in keywords:
            with_keyword = df[df['promptText'].str.contains(keyword, case=False, na=False)]
            without_keyword = df[~df['promptText'].str.contains(keyword, case=False, na=False)]
            
            if len(with_keyword) > 0 and len(without_keyword) > 0:
                avg_with = with_keyword['totalTime'].mean()
                avg_without = without_keyword['totalTime'].mean()
                diff_pct = ((avg_with - avg_without) / avg_without) * 100
                
                print(f"\nKeyword: '{keyword}'")
                print(f"  With keyword: {avg_with:.3f}s (n={len(with_keyword)})")
                print(f"  Without keyword: {avg_without:.3f}s (n={len(without_keyword)})")
                print(f"  Difference: {diff_pct:+.1f}%")
    
    def analyze_prefill_vs_decode(self, df: pd.DataFrame):
        """Analyze prefill vs decode time distribution"""
        print("\n📊 Prefill vs Decode Analysis")
        print("=" * 60)
        
        if 'prefillTime' in df.columns and 'decodeTime' in df.columns:
            avg_prefill = df['prefillTime'].mean()
            avg_decode = df['decodeTime'].mean()
            total_avg = avg_prefill + avg_decode
            
            prefill_pct = (avg_prefill / total_avg) * 100
            decode_pct = (avg_decode / total_avg) * 100
            
            print(f"Average Prefill Time: {avg_prefill:.3f}s ({prefill_pct:.1f}%)")
            print(f"Average Decode Time: {avg_decode:.3f}s ({decode_pct:.1f}%)")
            print(f"Prefill/Decode Ratio: {avg_prefill/avg_decode:.2f}")
    
    def visualize_latency_distribution(self, df: pd.DataFrame, output_dir: Path):
        """Create latency distribution visualizations"""
        print("\n📈 Creating visualizations...")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        
        # 1. Total latency distribution
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Histogram
        axes[0, 0].hist(df['totalTime'], bins=30, edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Total Time (s)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Total Latency Distribution')
        
        # Prefill vs Decode
        if 'prefillTime' in df.columns:
            axes[0, 1].scatter(df['prefillTime'], df['decodeTime'], alpha=0.5)
            axes[0, 1].set_xlabel('Prefill Time (s)')
            axes[0, 1].set_ylabel('Decode Time (s)')
            axes[0, 1].set_title('Prefill vs Decode Time')
        
        # Latency vs Prompt Length
        if 'promptLength' in df.columns:
            axes[1, 0].scatter(df['promptLength'], df['totalTime'], alpha=0.5)
            axes[1, 0].set_xlabel('Prompt Length (chars)')
            axes[1, 0].set_ylabel('Total Time (s)')
            axes[1, 0].set_title('Latency vs Prompt Length')
            
            # Add trend line
            z = np.polyfit(df['promptLength'], df['totalTime'], 1)
            p = np.poly1d(z)
            axes[1, 0].plot(df['promptLength'], p(df['promptLength']), "r--", alpha=0.8)
        
        # Tokens per second
        if 'tokensPerSecond' in df.columns:
            axes[1, 1].hist(df['tokensPerSecond'], bins=30, edgecolor='black', alpha=0.7, color='green')
            axes[1, 1].set_xlabel('Tokens/sec')
            axes[1, 1].set_ylabel('Frequency')
            axes[1, 1].set_title('Throughput Distribution')
        
        plt.tight_layout()
        plt.savefig(output_dir / 'latency_overview.png', dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {output_dir / 'latency_overview.png'}")
        
        # 2. Category comparison (if available)
        if 'category' in df.columns:
            plt.figure(figsize=(12, 6))
            df.boxplot(column='totalTime', by='category', ax=plt.gca())
            plt.title('Latency by Prompt Category')
            plt.suptitle('')  # Remove default title
            plt.xlabel('Category')
            plt.ylabel('Total Time (s)')
            plt.tight_layout()
            plt.savefig(output_dir / 'latency_by_category.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {output_dir / 'latency_by_category.png'}")
    
    def generate_report(self, df: pd.DataFrame, output_path: Path):
        """Generate comprehensive text report"""
        print("\n📝 Generating report...")
        
        with open(output_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("LATENCY ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total Inferences Analyzed: {len(df)}\n")
            f.write(f"Analysis Date: {pd.Timestamp.now()}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("SUMMARY STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(df[['totalTime', 'prefillTime', 'decodeTime', 'tokensPerSecond']].describe().to_string())
            f.write("\n\n")
            
            if 'category' in df.columns:
                f.write("-" * 80 + "\n")
                f.write("BY CATEGORY\n")
                f.write("-" * 80 + "\n")
                category_stats = df.groupby('category')['totalTime'].describe()
                f.write(category_stats.to_string())
                f.write("\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("CORRELATIONS\n")
            f.write("-" * 80 + "\n")
            if 'promptLength' in df.columns:
                f.write(f"Prompt Length vs Total Time: {df['promptLength'].corr(df['totalTime']):.3f}\n")
            if 'promptWordCount' in df.columns:
                f.write(f"Word Count vs Total Time: {df['promptWordCount'].corr(df['totalTime']):.3f}\n")
        
        print(f"✅ Saved: {output_path}")
    
    def run_full_analysis(self, output_dir: str = "../results/analysis"):
        """Run complete latency analysis pipeline"""
        df = self.load_results()
        
        if df.empty:
            print("❌ No data to analyze")
            return
        
        # Run analyses
        self.analyze_by_prompt_type(df)
        self.analyze_by_prompt_length(df)
        self.analyze_by_keywords(df)
        self.analyze_prefill_vs_decode(df)
        
        # Generate outputs
        output_path = Path(output_dir)
        self.visualize_latency_distribution(df, output_path)
        self.generate_report(df, output_path / 'latency_report.txt')
        
        # Save processed data
        df.to_csv(output_path / 'processed_data.csv', index=False)
        print(f"\n✅ Analysis complete! Results saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Analyze LLM inference latency')
    parser.add_argument('--results-dir', default='../results', help='Directory containing result JSON files')
    parser.add_argument('--output-dir', default='../results/analysis', help='Output directory for analysis')
    
    args = parser.parse_args()
    
    analyzer = LatencyAnalyzer(args.results_dir)
    analyzer.run_full_analysis(args.output_dir)


if __name__ == "__main__":
    main()

