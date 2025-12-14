# Setup Guide

## Prerequisites

- Mac running macOS Ventura 13.0+ or Sonoma 14.0+
- Xcode 15.0+
- iPhone 16 Pro Max with iOS 17.0+
- Apple Developer Account
- Python 3.9+
- 15GB+ free disk space

## Step-by-Step Setup

### 1. Clone and Setup Python Environment

```bash
cd /Users/yashalluri/Desktop/FinalProject
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Download LLM Models

```bash
# Create models directory
mkdir -p models

# Download Mistral 7B (recommended)
cd models
# Visit: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF
# Download: mistral-7b-instruct-v0.2.Q4_K_M.gguf
# Place in models/ directory
```

### 3. Setup iOS Development

#### 3a. Install Xcode Command Line Tools
```bash
xcode-select --install
```

#### 3b. Configure Signing
1. Open `ios_app/PromptOptimizer.xcodeproj` in Xcode
2. Select project in navigator
3. Go to "Signing & Capabilities"
4. Select your Team (Apple Developer Account)
5. Xcode will automatically manage provisioning profiles

#### 3c. Enable Developer Mode on iPhone
1. Connect iPhone to Mac via USB-C
2. On iPhone: Settings > Privacy & Security > Developer Mode
3. Enable Developer Mode and restart iPhone
4. Trust the computer when prompted

### 4. Build llama.cpp for iOS

```bash
cd ios_app/
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make clean
# Build for iOS
cmake -B build -G Xcode -DCMAKE_SYSTEM_NAME=iOS -DCMAKE_OSX_DEPLOYMENT_TARGET=17.0
cmake --build build --config Release
```

### 5. Prepare Datasets

```bash
# From project root
python3 datasets/prepare_datasets.py
```

This will:
- Download SQuAD, IMDB, and other datasets
- Create categorized prompt files
- Generate baseline test prompts

### 6. Build and Deploy iOS App

```bash
# Open in Xcode
open ios_app/PromptOptimizer.xcodeproj

# Or build from command line
xcodebuild -project ios_app/PromptOptimizer.xcodeproj \
  -scheme PromptOptimizer \
  -destination 'platform=iOS,name=Yashwanth's iPhone' \
  clean build
```

### 7. Verify Installation

Run the verification script:

```bash
python3 profiling/verify_setup.py
```

This checks:
- Python dependencies installed
- Models present and valid
- iOS app built successfully
- iPhone connected and recognized

## First Test Run

### Run Baseline Measurement

1. Launch app on iPhone
2. App will load model (first time takes ~30 seconds)
3. Tap "Run Baseline Test"
4. Results saved to `results/baseline/`

### View Results

```bash
# Analyze first run
python3 analysis/view_results.py results/baseline/run_001.json
```

## Troubleshooting

### Model Loading Issues
- Ensure model file is in `models/` directory
- Check file isn't corrupted (re-download if needed)
- Verify at least 6GB free RAM on iPhone

### Xcode Build Errors
- Clean build folder: Product > Clean Build Folder
- Delete derived data: ~/Library/Developer/Xcode/DerivedData
- Restart Xcode

### iPhone Connection Issues
- Unplug and replug USB-C cable
- Restart iPhone
- Trust computer again

### Python Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Next Steps

After successful setup:
1. Review [EXPERIMENT_GUIDE.md](EXPERIMENT_GUIDE.md)
2. Start Week 1 tasks
3. Run baseline measurements
4. Begin prompt analysis

## Getting Help

If you encounter issues not covered here:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review error logs in `logs/`
3. Document the issue for discussion

