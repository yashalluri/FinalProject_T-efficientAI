# Optimizing Prompt Efficiency for Large Language Models on Smartphones

**Reducing Energy Consumption and Latency via Prompt Engineering**

Group 4: Yashwanth Alluri

## Overview

This project investigates how prompt design affects energy consumption and latency when running Large Language Models (LLMs) locally on iPhone 16 Pro Max. The system analyzes prompt characteristics and provides real-time optimization recommendations to reduce inference costs while maintaining output quality.

## Project Structure

```
FinalProject/
├── ios_app/                    # Native iOS application
│   ├── PromptOptimizer/       # Main app code
│   ├── LLMRunner/             # LLM inference engine
│   └── Profiler/              # Performance measurement
├── datasets/                   # Prompt datasets
│   ├── qa/                    # Question answering prompts
│   ├── sentiment/             # Sentiment analysis prompts
│   ├── generation/            # Text generation prompts
│   └── reasoning/             # Chain-of-thought prompts
├── analysis/                   # Data analysis scripts
│   ├── latency_analysis.py
│   ├── energy_analysis.py
│   └── keyword_analysis.py
├── optimization/              # Prompt optimization engine
│   ├── optimizer.py
│   └── rules/
├── profiling/                 # Profiling utilities
├── models/                    # LLM model files (gitignored)
├── results/                   # Experimental results
└── docs/                      # Documentation

```

## Key Features

1. **Local LLM Inference**: Run Mistral 7B, Gemma 7B, or Vicuna 7B on iPhone
2. **Real-time Profiling**: Measure latency, energy, throughput, and memory
3. **Prompt Analysis**: Identify high-cost keywords and patterns
4. **Optimization Engine**: Suggest efficient prompt alternatives
5. **Dataset Management**: Organize and categorize diverse prompts

## Research Questions

- Which prompt keywords increase decoding time and energy?
- How do different prompt types impact resource usage?
- Can we generate smartphone-specific prompt guidelines?

## Metrics Tracked

- **Latency**: Prefill time, decode time, total inference time
- **Energy**: Joules per inference, joules per token
- **Throughput**: Tokens per second
- **Memory**: Peak memory usage
- **Quality**: Optional output quality metrics

## Technology Stack

- **iOS**: Swift, SwiftUI
- **LLM Runtime**: llama.cpp / MLC LLM for iOS
- **Profiling**: Instruments, MetricKit
- **Analysis**: Python (pandas, numpy, matplotlib)
- **Models**: Quantized GGUF format (4-bit, 8-bit)

## Timeline (8 Weeks)

- **Week 1**: Setup environment, finalize prompt dataset
- **Week 2-3**: Baseline efficiency measurements
- **Week 4-5**: Keyword and pattern analysis
- **Week 6**: Implement optimization component
- **Week 7**: Evaluate optimization impact
- **Week 8**: Documentation and presentation

## Getting Started

**🎯 HAVE IPHONE 16 PRO MAX?** → [START_HERE.md](START_HERE.md) - **Your complete action plan!**

**Key Guides:**
- 🚀 **[START_HERE.md](START_HERE.md)** - **Step-by-step setup checklist (START HERE!)**
- 💡 [QUICK_START.md](QUICK_START.md) - Simulator vs Device explained
- 📱 [SETUP.md](docs/SETUP.md) - Detailed setup guide
- 💻 [SIMULATOR_QUICKSTART.md](docs/SIMULATOR_QUICKSTART.md) - Using iOS Simulator for development
- ⚠️ [SIMULATOR_VS_DEVICE.md](docs/SIMULATOR_VS_DEVICE.md) - Why physical device is required for research
- 📊 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete overview of what's built

## What You Need to Provide

See [REQUIREMENTS_FROM_YOU.md](REQUIREMENTS_FROM_YOU.md) for a complete list of items needed from you.

## License

MIT License - Academic Research Project

