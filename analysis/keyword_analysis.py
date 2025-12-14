#!/usr/bin/env python3
"""
Keyword Analysis Script
Identifies high-impact keywords and patterns affecting LLM efficiency
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import Counter
import re
import argparse


class KeywordAnalyzer:
    def __init__(self, results_dir: str = "../results"):
        self.results_dir = Path(results_dir)
        self.data = []
        
        # Keywords to track
        self.instruction_keywords = [
            'explain', 'describe', 'analyze', 'summarize', 'write',
            'create', 'generate', 'provide', 'tell', 'show'
        ]
        
        self.verbose_modifiers = [
            'detailed', 'comprehensive', 'thoroughly', 'extensively',
            'in detail', 'step by step', 'carefully', 'complete'
        ]
        
        self.reasoning_keywords = [
            'think', 'reason', 'logic', 'because', 'therefore',
            'conclude', 'infer', 'deduce'
        ]
        
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
    
    def extract_keywords(self, df: pd.DataFrame):
        """Extract keyword features from prompts"""
        print("\n🔍 Extracting keywords...")
        
        # Add keyword presence columns
        for keyword in self.instruction_keywords:
            df[f'has_{keyword}'] = df['promptText'].str.contains(
                keyword, case=False, na=False, regex=False
            )
        
        for modifier in self.verbose_modifiers:
            safe_name = modifier.replace(' ', '_')
            df[f'has_{safe_name}'] = df['promptText'].str.contains(
                modifier, case=False, na=False, regex=False
            )
        
        # Count keywords per prompt
        df['instruction_count'] = df['promptText'].apply(
            lambda x: sum(1 for kw in self.instruction_keywords if kw in x.lower())
        )
        
        df['verbose_modifier_count'] = df['promptText'].apply(
            lambda x: sum(1 for mod in self.verbose_modifiers if mod in x.lower())
        )
        
        return df
    
    def analyze_keyword_impact(self, df: pd.DataFrame):
        """Analyze impact of each keyword on latency and energy"""
        print("\n📊 Keyword Impact Analysis")
        print("=" * 80)
        
        results = []
        
        # Analyze instruction keywords
        for keyword in self.instruction_keywords:
            col_name = f'has_{keyword}'
            if col_name in df.columns:
                with_kw = df[df[col_name]]
                without_kw = df[~df[col_name]]
                
                if len(with_kw) > 5 and len(without_kw) > 5:
                    impact = self._calculate_impact(with_kw, without_kw, keyword)
                    if impact:
                        results.append(impact)
        
        # Analyze verbose modifiers
        for modifier in self.verbose_modifiers:
            safe_name = modifier.replace(' ', '_')
            col_name = f'has_{safe_name}'
            if col_name in df.columns:
                with_mod = df[df[col_name]]
                without_mod = df[~df[col_name]]
                
                if len(with_mod) > 3 and len(without_mod) > 3:
                    impact = self._calculate_impact(with_mod, without_mod, modifier, keyword_type='modifier')
                    if impact:
                        results.append(impact)
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        if not results_df.empty:
            results_df = results_df.sort_values('latency_increase_pct', ascending=False)
            print("\nTop Impact Keywords (by latency increase):")
            print(results_df.head(15).to_string(index=False))
            
            return results_df
        else:
            print("Insufficient data for keyword analysis")
            return pd.DataFrame()
    
    def _calculate_impact(self, with_kw, without_kw, keyword, keyword_type='instruction'):
        """Calculate impact metrics for a keyword"""
        try:
            # Latency impact
            lat_with = with_kw['totalTime'].mean()
            lat_without = without_kw['totalTime'].mean()
            lat_increase_pct = ((lat_with - lat_without) / lat_without) * 100
            
            # Energy impact (if available)
            energy_increase_pct = None
            if 'estimatedEnergyJ' in with_kw.columns:
                eng_with = with_kw['estimatedEnergyJ'].mean()
                eng_without = without_kw['estimatedEnergyJ'].mean()
                if eng_without > 0:
                    energy_increase_pct = ((eng_with - eng_without) / eng_without) * 100
            
            # Response length impact
            resp_with = with_kw['generatedTokens'].mean()
            resp_without = without_kw['generatedTokens'].mean()
            resp_increase_pct = ((resp_with - resp_without) / resp_without) * 100
            
            return {
                'keyword': keyword,
                'type': keyword_type,
                'n_with': len(with_kw),
                'n_without': len(without_kw),
                'latency_with': lat_with,
                'latency_without': lat_without,
                'latency_increase_pct': lat_increase_pct,
                'energy_increase_pct': energy_increase_pct,
                'response_increase_pct': resp_increase_pct
            }
        except Exception as e:
            print(f"Error calculating impact for {keyword}: {e}")
            return None
    
    def analyze_keyword_combinations(self, df: pd.DataFrame):
        """Analyze combinations of keywords"""
        print("\n📊 Keyword Combination Analysis")
        print("=" * 80)
        
        # High-cost combinations
        high_cost_combinations = []
        
        # Check combinations of verbose modifiers + instruction keywords
        for modifier in self.verbose_modifiers[:5]:  # Top 5 modifiers
            safe_mod = modifier.replace(' ', '_')
            mod_col = f'has_{safe_mod}'
            
            if mod_col not in df.columns:
                continue
                
            for keyword in self.instruction_keywords[:5]:  # Top 5 instructions
                kw_col = f'has_{keyword}'
                
                if kw_col not in df.columns:
                    continue
                
                # Find prompts with both
                with_both = df[df[mod_col] & df[kw_col]]
                with_neither = df[~df[mod_col] & ~df[kw_col]]
                
                if len(with_both) > 2 and len(with_neither) > 2:
                    lat_both = with_both['totalTime'].mean()
                    lat_neither = with_neither['totalTime'].mean()
                    increase_pct = ((lat_both - lat_neither) / lat_neither) * 100
                    
                    if increase_pct > 10:  # Only significant increases
                        high_cost_combinations.append({
                            'combination': f"{modifier} + {keyword}",
                            'count': len(with_both),
                            'latency_increase_pct': increase_pct
                        })
        
        if high_cost_combinations:
            combo_df = pd.DataFrame(high_cost_combinations)
            combo_df = combo_df.sort_values('latency_increase_pct', ascending=False)
            print("\nHigh-Cost Keyword Combinations:")
            print(combo_df.head(10).to_string(index=False))
    
    def identify_optimization_opportunities(self, df: pd.DataFrame, keyword_impact_df: pd.DataFrame):
        """Identify specific optimization opportunities"""
        print("\n💡 Optimization Opportunities")
        print("=" * 80)
        
        if keyword_impact_df.empty:
            print("No keyword impact data available")
            return
        
        # Find high-impact keywords that appear frequently
        high_impact = keyword_impact_df[keyword_impact_df['latency_increase_pct'] > 15]
        frequent_high_impact = high_impact[high_impact['n_with'] > 10]
        
        if not frequent_high_impact.empty:
            print("\n🎯 High Priority Optimizations:")
            print("\nFrequently used keywords with high latency impact:")
            for _, row in frequent_high_impact.iterrows():
                print(f"\n  Keyword: '{row['keyword']}'")
                print(f"    Occurrences: {row['n_with']}")
                print(f"    Latency Impact: +{row['latency_increase_pct']:.1f}%")
                if row['energy_increase_pct']:
                    print(f"    Energy Impact: +{row['energy_increase_pct']:.1f}%")
                print(f"    Recommendation: Consider rephrasing prompts to avoid '{row['keyword']}' when possible")
        
        # Find verbose modifiers
        verbose_high_impact = keyword_impact_df[
            (keyword_impact_df['type'] == 'modifier') & 
            (keyword_impact_df['latency_increase_pct'] > 10)
        ]
        
        if not verbose_high_impact.empty:
            print("\n\n🎯 Verbose Modifiers to Avoid:")
            for _, row in verbose_high_impact.iterrows():
                print(f"  - '{row['keyword']}' (+{row['latency_increase_pct']:.1f}% latency)")
    
    def visualize_keyword_impact(self, keyword_impact_df: pd.DataFrame, output_dir: Path):
        """Create visualizations of keyword impact"""
        print("\n📈 Creating visualizations...")
        
        if keyword_impact_df.empty:
            print("No data to visualize")
            return
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        sns.set_style("whitegrid")
        
        # 1. Top keywords by latency impact
        plt.figure(figsize=(12, 8))
        top_keywords = keyword_impact_df.nlargest(15, 'latency_increase_pct')
        
        colors = ['red' if x > 20 else 'orange' if x > 10 else 'yellow' 
                  for x in top_keywords['latency_increase_pct']]
        
        plt.barh(range(len(top_keywords)), top_keywords['latency_increase_pct'], color=colors)
        plt.yticks(range(len(top_keywords)), top_keywords['keyword'])
        plt.xlabel('Latency Increase (%)')
        plt.title('Top 15 Keywords by Latency Impact')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(output_dir / 'keyword_impact_latency.png', dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {output_dir / 'keyword_impact_latency.png'}")
        
        # 2. Energy vs Latency impact scatter
        if 'energy_increase_pct' in keyword_impact_df.columns:
            plt.figure(figsize=(10, 8))
            valid_data = keyword_impact_df.dropna(subset=['energy_increase_pct'])
            
            plt.scatter(valid_data['latency_increase_pct'], 
                       valid_data['energy_increase_pct'],
                       s=100, alpha=0.6)
            
            # Add labels for significant keywords
            for _, row in valid_data.iterrows():
                if abs(row['latency_increase_pct']) > 15 or abs(row['energy_increase_pct']) > 15:
                    plt.annotate(row['keyword'], 
                               (row['latency_increase_pct'], row['energy_increase_pct']),
                               fontsize=8, alpha=0.7)
            
            plt.xlabel('Latency Increase (%)')
            plt.ylabel('Energy Increase (%)')
            plt.title('Keyword Impact: Energy vs Latency')
            plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
            plt.axvline(x=0, color='gray', linestyle='--', linewidth=0.5)
            plt.tight_layout()
            plt.savefig(output_dir / 'keyword_impact_scatter.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved: {output_dir / 'keyword_impact_scatter.png'}")
    
    def generate_optimization_rules(self, keyword_impact_df: pd.DataFrame, output_path: Path):
        """Generate machine-readable optimization rules"""
        print("\n📝 Generating optimization rules...")
        
        if keyword_impact_df.empty:
            return
        
        rules = {
            'high_cost_keywords': [],
            'verbose_modifiers': [],
            'recommended_alternatives': {}
        }
        
        # High cost keywords (>15% latency increase)
        high_cost = keyword_impact_df[keyword_impact_df['latency_increase_pct'] > 15]
        rules['high_cost_keywords'] = high_cost['keyword'].tolist()
        
        # Verbose modifiers
        verbose = keyword_impact_df[keyword_impact_df['type'] == 'modifier']
        rules['verbose_modifiers'] = verbose['keyword'].tolist()
        
        # Suggested alternatives (simplified for demonstration)
        alternatives = {
            'explain in detail': 'explain',
            'describe thoroughly': 'describe',
            'provide a comprehensive': 'provide',
            'analyze carefully': 'analyze'
        }
        rules['recommended_alternatives'] = alternatives
        
        # Save as JSON
        with open(output_path, 'w') as f:
            json.dump(rules, f, indent=2)
        
        print(f"✅ Saved: {output_path}")
    
    def run_full_analysis(self, output_dir: str = "../results/analysis"):
        """Run complete keyword analysis pipeline"""
        df = self.load_results()
        
        if df.empty:
            print("❌ No data to analyze")
            return
        
        # Extract keywords
        df = self.extract_keywords(df)
        
        # Run analyses
        keyword_impact_df = self.analyze_keyword_impact(df)
        self.analyze_keyword_combinations(df)
        self.identify_optimization_opportunities(df, keyword_impact_df)
        
        # Generate outputs
        output_path = Path(output_dir)
        self.visualize_keyword_impact(keyword_impact_df, output_path)
        
        if not keyword_impact_df.empty:
            keyword_impact_df.to_csv(output_path / 'keyword_impact.csv', index=False)
            self.generate_optimization_rules(keyword_impact_df, output_path / 'optimization_rules.json')
        
        print(f"\n✅ Analysis complete! Results saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Analyze keyword impact on LLM efficiency')
    parser.add_argument('--results-dir', default='../results', help='Directory containing result JSON files')
    parser.add_argument('--output-dir', default='../results/analysis', help='Output directory for analysis')
    
    args = parser.parse_args()
    
    analyzer = KeywordAnalyzer(args.results_dir)
    analyzer.run_full_analysis(args.output_dir)


if __name__ == "__main__":
    main()

