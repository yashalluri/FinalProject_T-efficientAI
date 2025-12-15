# PromptOptimizer: Efficient LLM Inference on iOS Devices

**AI-powered prompt optimization system for reducing energy consumption and latency via prompt engineering**

**Author:** Yashwanth Alluri  
**Repository:** [https://github.com/yashalluri/FinalProject_T-efficientAI](https://github.com/yashalluri/FinalProject_T-efficientAI)

## Overview

PromptOptimizer is a comprehensive system that automatically optimizes prompts to improve Large Language Model (LLM) inference performance on iOS devices. By analyzing prompt characteristics and their impact on performance metrics (latency, energy consumption, throughput), the system learns to refine prompts for better efficiency while maintaining output quality.

### Key Achievements

- **15-25% latency reduction** across different prompt categories
- **12-20% energy savings** per inference
- **18-33% throughput improvement** (tokens/second)
- **85-92% quality preservation** (semantic similarity)

## Project Structure

```
FinalProject/
├── ios_app_project/           # Xcode iOS application
│   └── PromptOptimizer/       # Main app code
│       ├── App/               # App entry point
│       ├── Views/             # SwiftUI views
│       ├── Optimization/      # Optimization engine
│       ├── LLM/               # LLM integration (llama.cpp)
│       ├── Profiling/         # Performance profiler
│       └── Data/              # Database management
├── ios_app/                   # Alternative iOS app structure
├── optimization/              # Python optimization tools
│   ├── optimizer.py           # Learning-based optimizer
│   └── train_model.py         # Model training
├── analysis/                  # Analysis scripts
│   ├── latency_analysis.py    # Latency profiling
│   ├── energy_analysis.py     # Energy consumption analysis
│   ├── keyword_analysis.py    # Keyword extraction
│   └── generate_final_results.py  # Result aggregation
├── profiling/                 # Profiling utilities
│   └── verify_setup.py        # Setup verification
├── datasets/                   # Prompt datasets
│   ├── qa/                    # Question-answering prompts
│   ├── sentiment/             # Sentiment analysis
│   ├── generation/            # Creative generation
│   └── reasoning/             # Chain-of-thought reasoning
├── results/                   # Experimental results
│   └── final_analysis/        # Analysis charts and summaries
├── scripts/                   # Automation scripts
├── docs/                      # Documentation
└── models/                    # LLM model files (gitignored, 4.1GB+)

```

## Key Features

1. **Real-time Prompt Optimization**: Automatically optimizes prompts for better performance
2. **Comprehensive Profiling**: Measures latency, energy, throughput, and memory usage
3. **Learning-Based Optimization**: Adapts optimization strategies based on performance feedback
4. **Native iOS App**: SwiftUI-based interface with llama.cpp integration
5. **Batch Experiments**: Run experiments across multiple datasets
6. **Performance Analysis**: Python tools for detailed analysis and visualization
7. **Model File Management**: Automatic handling of model file location and loading

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

- **iOS**: Swift, SwiftUI, Objective-C++ bridging
- **LLM Runtime**: llama.cpp (C++), Mistral-7B-Instruct (Q4_K_M quantization)
- **Profiling**: Custom performance profiler, Instruments, MetricKit
- **Analysis**: Python (pandas, numpy, matplotlib, scikit-learn)
- **Storage**: SQLite for iOS, JSON for analysis
- **Models**: GGUF format (4-bit quantization, ~4.1GB)

## Requirements

### iOS Application
- iOS 15.0+
- Xcode 14.0+
- Swift 5.0+
- 4GB+ RAM
- 5GB+ storage for model file

### Python Backend
- Python 3.8+
- Required packages: numpy, pandas, matplotlib, scikit-learn
- See `requirements.txt` for full list

### Model
- Mistral-7B-Instruct-v0.2 (Q4_K_M quantization)
- Format: GGUF
- Size: ~4.1GB (excluded from git)

## Timeline (8 Weeks)

- **Week 1**: Setup environment, finalize prompt dataset
- **Week 2-3**: Baseline efficiency measurements
- **Week 4-5**: Keyword and pattern analysis
- **Week 6**: Implement optimization component
- **Week 7**: Evaluate optimization impact
- **Week 8**: Documentation and presentation

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yashalluri/FinalProject_T-efficientAI.git
cd FinalProject_T-efficientAI
```

### 2. iOS Application Setup

1. **Open Xcode project**:
   ```bash
   open ios_app_project/PromptOptimizer/PromptOptimizer.xcodeproj
   ```

2. **Add model file** (if not already present):
   - Download Mistral-7B-Instruct-v0.2 (Q4_K_M.gguf)
   - Place in: `ios_app_project/PromptOptimizer/PromptOptimizer/Documents/models/`
   - Add to Xcode project as a resource

3. **Build and run**:
   - Select target device/simulator
   - Build (⌘B) and Run (⌘R)

### 3. Python Environment Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run Analysis

```bash
# Run energy analysis
python analysis/energy_analysis.py

# Run latency analysis
python analysis/latency_analysis.py

# Generate final results
python analysis/generate_final_results.py
```

## Usage

### iOS Application

1. Launch the app
2. Load the model (first time only)
3. Enter a prompt in the main view
4. Click "Optimize" to see optimization results
5. Compare original vs optimized performance
6. Run batch experiments across datasets

### Python Analysis

```bash
# Analyze energy consumption
python analysis/energy_analysis.py --input data/results/experimental_data.json

# Analyze latency patterns
python analysis/latency_analysis.py --input data/results/experimental_data.json

# Generate comprehensive results
python analysis/generate_final_results.py --output results/final_analysis/
```

## Documentation

- **Setup Guide**: See project documentation in `docs/` directory
- **iOS Quick Start**: `docs/IOS_QUICK_START.md`
- **Implementation Guide**: `docs/LLAMA_CPP_INTEGRATION_GUIDE.md`
- **Project Summary**: `PROJECT_SUMMARY.md`

## Experimental Results

Results are available in `results/final_analysis/`:
- Performance charts (latency, energy, throughput)
- Statistical summaries
- Category-wise analysis
- Optimization impact visualizations

## Key Components

### ModelFileManager
Handles model file location and ensures availability in app's Documents directory. Automatically checks bundle and Documents, copies from bundle if needed.

### LLMRunner
Manages LLM inference using llama.cpp bridge, handles token generation and streaming responses.

### PerformanceProfiler
Comprehensive performance measurement: latency (token-level), energy estimation, throughput, memory profiling.

### PromptOptimizer
Core optimization engine with learning-based strategies that adapt to device characteristics.

## Architecture

- **SwiftUI**: Modern declarative UI framework
- **MVVM Architecture**: Separation of concerns
- **llama.cpp Integration**: Efficient C++ LLM inference via Objective-C++ bridge
- **SQLite**: Persistent storage for results and experiments

## Reproducibility

To reproduce our experiments:

1. Set up environment (see Quick Start)
2. Load datasets from `datasets/` directory
3. Run batch experiments using the iOS app or Python scripts
4. Analyze results using provided analysis scripts
5. Compare with results in `results/final_analysis/`

## Contributing

This is a research project. For questions or issues, please open an issue on GitHub.

## License

MIT License - Academic Research Project

## Citation

If you use this work in your research, please cite:

```bibtex
@software{promptoptimizer2024,
  title={PromptOptimizer: Efficient LLM Inference on Mobile Devices},
  author={Alluri, Yashwanth},
  year={2024},
  url={https://github.com/yashalluri/FinalProject_T-efficientAI}
}
```

## Acknowledgments

- llama.cpp for efficient LLM inference
- Mistral AI for the Mistral-7B model
- Apple for SwiftUI and iOS development tools

