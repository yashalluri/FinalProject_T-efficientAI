#!/usr/bin/env python3
"""
Dataset Preparation Script
Downloads and prepares prompt datasets for LLM efficiency testing
"""

import json
import os
import random
from pathlib import Path
from typing import List, Dict
import requests
from datasets import load_dataset
from tqdm import tqdm


class DatasetPreparer:
    def __init__(self, base_dir: str = "datasets"):
        self.base_dir = Path(base_dir)
        self.categories = {
            "qa": self.base_dir / "qa",
            "sentiment": self.base_dir / "sentiment",
            "generation": self.base_dir / "generation",
            "reasoning": self.base_dir / "reasoning"
        }
        
        # Create directories
        for category_path in self.categories.values():
            category_path.mkdir(parents=True, exist_ok=True)
    
    def prepare_squad_qa(self, num_samples: int = 500):
        """Prepare SQuAD question-answering prompts"""
        print("📥 Downloading SQuAD dataset...")
        
        try:
            dataset = load_dataset("squad", split="validation")
            
            prompts = []
            for i, item in enumerate(tqdm(dataset, desc="Processing SQuAD")):
                if i >= num_samples:
                    break
                
                context = item['context']
                question = item['question']
                
                # Create different prompt variations
                variations = [
                    f"Answer the following question based on the context.\n\nContext: {context}\n\nQuestion: {question}",
                    f"Question: {question}\n\nContext: {context}",
                    f"{question}\n\n{context}",
                    f"Given the context below, answer the question.\n\nContext: {context}\n\nQ: {question}\nA:",
                ]
                
                for var_idx, prompt_text in enumerate(variations):
                    prompts.append({
                        "id": f"squad_{i}_{var_idx}",
                        "prompt": prompt_text,
                        "category": "qa",
                        "subcategory": "factual",
                        "source": "squad",
                        "length": len(prompt_text),
                        "word_count": len(prompt_text.split()),
                        "has_context": True,
                        "variation": var_idx
                    })
            
            output_file = self.categories["qa"] / "squad_prompts.json"
            with open(output_file, 'w') as f:
                json.dump(prompts, f, indent=2)
            
            print(f"✅ Saved {len(prompts)} SQuAD prompts to {output_file}")
            return prompts
        
        except Exception as e:
            print(f"❌ Error preparing SQuAD: {e}")
            return []
    
    def prepare_sentiment_analysis(self, num_samples: int = 500):
        """Prepare sentiment analysis prompts from IMDB"""
        print("📥 Downloading IMDB dataset...")
        
        try:
            dataset = load_dataset("imdb", split="test")
            
            prompts = []
            for i, item in enumerate(tqdm(dataset, desc="Processing IMDB")):
                if i >= num_samples:
                    break
                
                text = item['text'][:500]  # Truncate long reviews
                
                # Different prompt formulations
                variations = [
                    f"Analyze the sentiment of this review: {text}",
                    f"Is this review positive or negative?\n\n{text}",
                    f"What is the sentiment (positive/negative) of the following text?\n\n{text}",
                    f"Review: {text}\n\nSentiment:",
                    f"Determine if this movie review is positive or negative and explain why:\n\n{text}",
                ]
                
                for var_idx, prompt_text in enumerate(variations):
                    prompts.append({
                        "id": f"imdb_{i}_{var_idx}",
                        "prompt": prompt_text,
                        "category": "sentiment",
                        "subcategory": "movie_review",
                        "source": "imdb",
                        "length": len(prompt_text),
                        "word_count": len(prompt_text.split()),
                        "variation": var_idx
                    })
            
            output_file = self.categories["sentiment"] / "imdb_prompts.json"
            with open(output_file, 'w') as f:
                json.dump(prompts, f, indent=2)
            
            print(f"✅ Saved {len(prompts)} IMDB prompts to {output_file}")
            return prompts
        
        except Exception as e:
            print(f"❌ Error preparing IMDB: {e}")
            return []
    
    def prepare_generation_prompts(self, num_samples: int = 300):
        """Prepare text generation prompts"""
        print("📝 Creating generation prompts...")
        
        # Creative writing prompts
        creative_topics = [
            "Write a short story about an AI that learns to dream",
            "Describe a futuristic city in the year 2100",
            "Create a poem about the ocean",
            "Write a product description for a smartwatch",
            "Draft an email to a colleague about a project update",
            "Compose a thank you letter to a mentor",
            "Write instructions for making coffee",
            "Describe how photosynthesis works",
            "Explain quantum computing to a 10-year-old",
            "Write a blog post about sustainable living"
        ]
        
        # Instruction-heavy variations
        instruction_prefixes = [
            "Please ",
            "I need you to ",
            "Can you ",
            "Write ",
            "Generate ",
            "Create ",
            "Compose ",
            "Draft ",
        ]
        
        prompts = []
        for i, topic in enumerate(creative_topics * (num_samples // len(creative_topics) + 1)):
            if len(prompts) >= num_samples:
                break
            
            prefix = random.choice(instruction_prefixes)
            
            # Create variations
            variations = [
                f"{topic}",
                f"{prefix}{topic.lower()}",
                f"{topic}. Be detailed and creative.",
                f"{topic}. Keep it concise.",
                f"{prefix}{topic.lower()}. Make it engaging and informative.",
            ]
            
            for var_idx, prompt_text in enumerate(variations[:3]):  # Limit variations
                prompts.append({
                    "id": f"gen_{len(prompts)}",
                    "prompt": prompt_text,
                    "category": "generation",
                    "subcategory": "creative",
                    "source": "manual",
                    "length": len(prompt_text),
                    "word_count": len(prompt_text.split()),
                    "variation": var_idx
                })
        
        output_file = self.categories["generation"] / "creative_prompts.json"
        with open(output_file, 'w') as f:
            json.dump(prompts[:num_samples], f, indent=2)
        
        print(f"✅ Saved {len(prompts[:num_samples])} generation prompts to {output_file}")
        return prompts[:num_samples]
    
    def prepare_reasoning_prompts(self, num_samples: int = 200):
        """Prepare chain-of-thought reasoning prompts"""
        print("🧠 Creating reasoning prompts...")
        
        reasoning_problems = [
            {
                "problem": "If a train travels 120 miles in 2 hours, what is its average speed?",
                "type": "math"
            },
            {
                "problem": "All birds have wings. Penguins are birds. Do penguins have wings?",
                "type": "logic"
            },
            {
                "problem": "A farmer has 17 sheep. All but 9 die. How many are left?",
                "type": "math"
            },
            {
                "problem": "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
                "type": "logic"
            },
            {
                "problem": "What comes next in the sequence: 2, 4, 8, 16, 32, ?",
                "type": "pattern"
            },
            {
                "problem": "You have a 3-gallon jug and a 5-gallon jug. How can you measure exactly 4 gallons?",
                "type": "puzzle"
            },
        ]
        
        prompts = []
        for i, item in enumerate(reasoning_problems * (num_samples // len(reasoning_problems) + 1)):
            if len(prompts) >= num_samples:
                break
            
            problem = item["problem"]
            
            # Different reasoning prompt styles
            variations = [
                f"{problem}",
                f"Solve this step by step: {problem}",
                f"Think through this carefully and explain your reasoning: {problem}",
                f"Let's break this down: {problem}",
                f"Analyze this problem and provide a detailed solution: {problem}",
                f"{problem}\n\nLet's think step by step:",
                f"{problem}\n\nPlease show your work.",
            ]
            
            for var_idx, prompt_text in enumerate(variations):
                prompts.append({
                    "id": f"reason_{len(prompts)}",
                    "prompt": prompt_text,
                    "category": "reasoning",
                    "subcategory": item["type"],
                    "source": "manual",
                    "length": len(prompt_text),
                    "word_count": len(prompt_text.split()),
                    "variation": var_idx,
                    "requires_cot": var_idx > 0  # Chain-of-thought required
                })
        
        output_file = self.categories["reasoning"] / "reasoning_prompts.json"
        with open(output_file, 'w') as f:
            json.dump(prompts[:num_samples], f, indent=2)
        
        print(f"✅ Saved {len(prompts[:num_samples])} reasoning prompts to {output_file}")
        return prompts[:num_samples]
    
    def create_baseline_test_set(self):
        """Create a curated baseline test set with diverse prompts"""
        print("📊 Creating baseline test set...")
        
        baseline_prompts = [
            # Short factual
            {"prompt": "What is the capital of France?", "type": "short_factual"},
            {"prompt": "Who wrote Romeo and Juliet?", "type": "short_factual"},
            
            # Medium factual
            {"prompt": "Explain how photosynthesis works.", "type": "medium_factual"},
            {"prompt": "What are the main causes of climate change?", "type": "medium_factual"},
            
            # Long factual
            {"prompt": "Provide a detailed explanation of how the internet works, including DNS, TCP/IP, and HTTP.", "type": "long_factual"},
            
            # Creative short
            {"prompt": "Write a haiku about technology.", "type": "creative_short"},
            
            # Creative long
            {"prompt": "Write a short story about a robot learning to paint. Make it emotional and engaging.", "type": "creative_long"},
            
            # Analytical
            {"prompt": "Analyze the pros and cons of remote work.", "type": "analytical"},
            {"prompt": "Compare and contrast democracy and monarchy.", "type": "analytical"},
            
            # Instruction-heavy
            {"prompt": "Please carefully analyze the following and provide a detailed, step-by-step explanation with examples: What is machine learning?", "type": "instruction_heavy"},
        ]
        
        baseline = []
        for i, item in enumerate(baseline_prompts):
            baseline.append({
                "id": f"baseline_{i}",
                "prompt": item["prompt"],
                "type": item["type"],
                "length": len(item["prompt"]),
                "word_count": len(item["prompt"].split())
            })
        
        output_file = self.base_dir / "baseline_test_set.json"
        with open(output_file, 'w') as f:
            json.dump(baseline, f, indent=2)
        
        print(f"✅ Saved baseline test set to {output_file}")
        return baseline
    
    def generate_summary(self):
        """Generate summary statistics of prepared datasets"""
        print("\n📈 Dataset Summary:")
        print("=" * 60)
        
        total_prompts = 0
        for category, path in self.categories.items():
            category_count = 0
            for json_file in path.glob("*.json"):
                with open(json_file) as f:
                    data = json.load(f)
                    category_count += len(data)
            
            print(f"{category.upper():12} : {category_count:4} prompts")
            total_prompts += category_count
        
        print("=" * 60)
        print(f"{'TOTAL':12} : {total_prompts:4} prompts")
        print()
    
    def run_all(self):
        """Run all dataset preparation steps"""
        print("🚀 Starting dataset preparation...\n")
        
        self.prepare_squad_qa(num_samples=100)  # Reduced for faster testing
        self.prepare_sentiment_analysis(num_samples=100)
        self.prepare_generation_prompts(num_samples=100)
        self.prepare_reasoning_prompts(num_samples=100)
        self.create_baseline_test_set()
        self.generate_summary()
        
        print("✅ Dataset preparation complete!")


if __name__ == "__main__":
    preparer = DatasetPreparer()
    preparer.run_all()

