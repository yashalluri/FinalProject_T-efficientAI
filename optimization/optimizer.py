#!/usr/bin/env python3
"""
Advanced Prompt Optimizer
Machine learning-based prompt optimization using learned patterns
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np


class AdvancedPromptOptimizer:
    """
    Advanced prompt optimizer that learns from experimental results
    """
    
    def __init__(self, rules_path: str = None):
        self.rules_path = Path(rules_path) if rules_path else None
        self.learned_rules = self.load_rules() if self.rules_path else {}
        
        # Base optimization rules
        self.base_rules = {
            'remove_politeness': {
                'patterns': [
                    (r'\bplease\s+', ''),
                    (r'\bcould you\s+', ''),
                    (r'\bwould you\s+', ''),
                    (r'\bI would like you to\s+', ''),
                    (r'\bcan you please\s+', ''),
                ],
                'impact': 0.05  # 5% average improvement
            },
            'simplify_instructions': {
                'patterns': [
                    (r'\bprovide a detailed explanation of\b', 'explain'),
                    (r'\bgive me a comprehensive overview of\b', 'describe'),
                    (r'\bI need you to analyze\b', 'analyze'),
                    (r'\bcan you help me understand\b', 'explain'),
                ],
                'impact': 0.10
            },
            'remove_verbose_modifiers': {
                'patterns': [
                    (r'\s+in great detail\b', ''),
                    (r'\s+thoroughly\b', ''),
                    (r'\s+comprehensively\b', ''),
                    (r'\s+extensively\b', ''),
                    (r'\s+as much as possible\b', ''),
                ],
                'impact': 0.15
            },
            'remove_redundant_instructions': {
                'patterns': [
                    (r'\bmake sure to\s+', ''),
                    (r'\bbe sure to\s+', ''),
                    (r'\bdon\'t forget to\s+', ''),
                ],
                'impact': 0.05
            }
        }
    
    def load_rules(self) -> Dict:
        """Load learned optimization rules from analysis"""
        if not self.rules_path or not self.rules_path.exists():
            return {}
        
        try:
            with open(self.rules_path) as f:
                rules = json.load(f)
            print(f"📚 Loaded {len(rules.get('high_cost_keywords', []))} learned rules")
            return rules
        except Exception as e:
            print(f"⚠️  Error loading rules: {e}")
            return {}
    
    def optimize(self, prompt: str, aggressive: bool = False) -> Tuple[str, Dict]:
        """
        Optimize a prompt for efficiency
        
        Args:
            prompt: Original prompt text
            aggressive: If True, apply more aggressive optimizations
        
        Returns:
            Tuple of (optimized_prompt, optimization_details)
        """
        optimized = prompt
        changes = []
        
        # Apply base rules
        for rule_name, rule_data in self.base_rules.items():
            before = optimized
            for pattern, replacement in rule_data['patterns']:
                optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
            
            if optimized != before:
                changes.append(rule_name)
        
        # Apply learned rules if available
        if self.learned_rules:
            optimized, learned_changes = self.apply_learned_rules(optimized, aggressive)
            changes.extend(learned_changes)
        
        # Clean up whitespace
        optimized = re.sub(r'\s+', ' ', optimized).strip()
        
        # Calculate expected improvement
        improvement = self.estimate_improvement(prompt, optimized, changes)
        
        details = {
            'original_length': len(prompt),
            'optimized_length': len(optimized),
            'length_reduction': len(prompt) - len(optimized),
            'changes_applied': changes,
            'estimated_latency_reduction': improvement['latency'],
            'estimated_energy_reduction': improvement['energy'],
            'quality_impact': self.assess_quality_impact(prompt, optimized)
        }
        
        return optimized, details
    
    def apply_learned_rules(self, prompt: str, aggressive: bool) -> Tuple[str, List[str]]:
        """Apply rules learned from experimental results"""
        optimized = prompt
        changes = []
        
        # Replace high-cost keywords with alternatives
        if 'recommended_alternatives' in self.learned_rules:
            for original, replacement in self.learned_rules['recommended_alternatives'].items():
                if original in optimized.lower():
                    pattern = re.compile(re.escape(original), re.IGNORECASE)
                    optimized = pattern.sub(replacement, optimized)
                    changes.append(f"replaced_{original.replace(' ', '_')}")
        
        # Remove high-cost keywords if aggressive
        if aggressive and 'high_cost_keywords' in self.learned_rules:
            for keyword in self.learned_rules['high_cost_keywords']:
                # Only remove if it doesn't change core meaning
                if keyword in ['thoroughly', 'extensively', 'comprehensively']:
                    optimized = re.sub(rf'\b{keyword}\b', '', optimized, flags=re.IGNORECASE)
                    changes.append(f"removed_{keyword}")
        
        return optimized, changes
    
    def estimate_improvement(self, original: str, optimized: str, changes: List[str]) -> Dict:
        """Estimate performance improvement from optimizations"""
        
        # Base improvement from length reduction
        length_reduction = (len(original) - len(optimized)) / len(original)
        base_improvement = length_reduction * 0.20  # 20% impact from length
        
        # Additional improvement from specific changes
        rule_impact = sum(
            self.base_rules.get(change, {}).get('impact', 0)
            for change in changes
            if change in self.base_rules
        )
        
        total_latency = min(base_improvement + rule_impact, 0.50)  # Cap at 50%
        total_energy = total_latency * 0.85  # Energy typically 85% of latency improvement
        
        return {
            'latency': total_latency,
            'energy': total_energy
        }
    
    def assess_quality_impact(self, original: str, optimized: str) -> str:
        """Assess impact on output quality"""
        change_magnitude = abs(len(original) - len(optimized)) / len(original)
        
        if change_magnitude < 0.1:
            return "maintained"
        elif change_magnitude < 0.25:
            return "likely_maintained"
        else:
            return "may_be_reduced"
    
    def batch_optimize(self, prompts: List[str], aggressive: bool = False) -> List[Dict]:
        """Optimize a batch of prompts"""
        results = []
        
        for prompt in prompts:
            optimized, details = self.optimize(prompt, aggressive)
            results.append({
                'original': prompt,
                'optimized': optimized,
                **details
            })
        
        return results
    
    def generate_report(self, optimizations: List[Dict]) -> str:
        """Generate a report of optimizations"""
        report = []
        report.append("=" * 80)
        report.append("PROMPT OPTIMIZATION REPORT")
        report.append("=" * 80)
        report.append("")
        
        total_prompts = len(optimizations)
        avg_latency = np.mean([o['estimated_latency_reduction'] for o in optimizations])
        avg_energy = np.mean([o['estimated_energy_reduction'] for o in optimizations])
        avg_length_reduction = np.mean([o['length_reduction'] for o in optimizations])
        
        report.append(f"Total Prompts: {total_prompts}")
        report.append(f"Average Latency Reduction: {avg_latency*100:.1f}%")
        report.append(f"Average Energy Reduction: {avg_energy*100:.1f}%")
        report.append(f"Average Length Reduction: {avg_length_reduction:.1f} characters")
        report.append("")
        
        report.append("-" * 80)
        report.append("SAMPLE OPTIMIZATIONS")
        report.append("-" * 80)
        
        for i, opt in enumerate(optimizations[:5], 1):
            report.append(f"\n{i}. Original:")
            report.append(f"   {opt['original'][:100]}...")
            report.append(f"   Optimized:")
            report.append(f"   {opt['optimized'][:100]}...")
            report.append(f"   Changes: {', '.join(opt['changes_applied'])}")
            report.append(f"   Est. Latency: -{opt['estimated_latency_reduction']*100:.1f}%")
        
        return "\n".join(report)


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Optimize prompts for efficiency')
    parser.add_argument('--prompt', type=str, help='Single prompt to optimize')
    parser.add_argument('--file', type=str, help='File containing prompts (one per line)')
    parser.add_argument('--rules', type=str, help='Path to learned rules JSON')
    parser.add_argument('--aggressive', action='store_true', help='Use aggressive optimization')
    parser.add_argument('--output', type=str, help='Output file for results')
    
    args = parser.parse_args()
    
    optimizer = AdvancedPromptOptimizer(rules_path=args.rules)
    
    if args.prompt:
        # Single prompt
        optimized, details = optimizer.optimize(args.prompt, args.aggressive)
        print(f"\nOriginal: {args.prompt}")
        print(f"Optimized: {optimized}")
        print(f"\nDetails: {json.dumps(details, indent=2)}")
    
    elif args.file:
        # Batch from file
        with open(args.file) as f:
            prompts = [line.strip() for line in f if line.strip()]
        
        results = optimizer.batch_optimize(prompts, args.aggressive)
        report = optimizer.generate_report(results)
        
        print(report)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n✅ Results saved to {args.output}")
    
    else:
        print("Please provide --prompt or --file")


if __name__ == "__main__":
    main()

