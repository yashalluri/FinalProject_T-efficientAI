# What You Need to Provide

## Hardware Requirements

✅ **iPhone 16 Pro Max** - You mentioned you have this
- Ensure iOS 17.0+ is installed
- At least 10GB free storage for models
- Developer mode enabled
- USB-C cable for development

## Software & Accounts

### 1. Apple Developer Account
- **Cost**: $99/year (or free if testing on your own device only)
- **Why**: Required to deploy apps to physical iPhone
- **Sign up**: https://developer.apple.com/

### 2. Xcode Installation
- **Download**: Mac App Store (free)
- **Version**: Xcode 15.0+
- **Size**: ~15GB
- **Why**: Required to build and deploy iOS app

### 3. Mac Computer
- **Requirement**: macOS Ventura 13.0+ or Sonoma 14.0+
- **Why**: iOS development requires Xcode which only runs on macOS
- **If you don't have one**: Consider alternative approaches listed below

## Model Files (Choose One or More)

Download quantized models in GGUF format:

### Option 1: Mistral 7B (Recommended)
- **Model**: `mistral-7b-instruct-v0.2.Q4_K_M.gguf`
- **Size**: ~4.4GB
- **Download**: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF

### Option 2: Gemma 7B
- **Model**: `gemma-7b-it-Q4_K_M.gguf`
- **Size**: ~4.9GB
- **Download**: https://huggingface.co/lmstudio-ai/gemma-7b-it-GGUF

### Option 3: Vicuna 7B
- **Model**: `vicuna-7b-v1.5.Q4_K_M.gguf`
- **Size**: ~4.1GB
- **Download**: https://huggingface.co/TheBloke/vicuna-7B-v1.5-GGUF

**Instructions**:
1. Create account on HuggingFace
2. Download your chosen model file(s)
3. Place in `FinalProject/models/` directory
4. Models are gitignored for size reasons

## Dataset Access (Optional - We'll Auto-Download)

If you want to manually curate datasets:

### Q&A Datasets
- **SQuAD**: https://rajpurkar.github.io/SQuAD-explorer/
- **WebGLM-QA**: https://github.com/THUDM/WebGLM

### Sentiment Analysis
- **IMDB**: https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews
- **Yelp**: https://www.yelp.com/dataset

### Text Generation
- **OpenOrca**: https://huggingface.co/datasets/Open-Orca/OpenOrca
- **HelpSteer**: https://huggingface.co/datasets/nvidia/HelpSteer

## Python Environment

Install on your Mac:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Required packages (we'll generate requirements.txt):
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- jupyter
- datasets (HuggingFace)

## Time Commitments

- **Week 1**: ~8-10 hours (setup, learning)
- **Week 2-7**: ~6-8 hours per week (running experiments, analysis)
- **Week 8**: ~10-12 hours (final documentation, presentation)

## Your Action Items

### Immediate (Week 1)
1. ✅ Confirm you have iPhone 16 Pro Max
2. ⬜ Check iOS version (Settings > General > About)
3. ⬜ Install Xcode from Mac App Store
4. ⬜ Sign up for Apple Developer (or use free tier)
5. ⬜ Download at least one LLM model file
6. ⬜ Install Python dependencies

### This Week
7. ⬜ Connect iPhone to Mac, enable Developer Mode
8. ⬜ Build and deploy test app to verify setup
9. ⬜ Run first baseline measurement
10. ⬜ Review generated prompt datasets

### Ongoing
- Run daily measurements (15-30 min)
- Review analysis results weekly
- Provide feedback on optimization effectiveness

## Alternative Approaches

### Option A: Simulator for Development (Recommended for Learning)
**IMPORTANT**: Simulator can be used for development but NOT for research measurements!

✅ **Good for**:
- Learning iOS development
- Testing app UI and logic
- Debugging and fixing crashes
- Initial app development

❌ **Cannot be used for**:
- Energy measurements (no battery)
- Performance measurements (different CPU)
- Any research data (different hardware)

See detailed guide: [SIMULATOR_VS_DEVICE.md](docs/SIMULATOR_VS_DEVICE.md)

**To use simulator**:
1. Open Xcode project
2. Select "iPhone 16 Pro Max Simulator" from device dropdown
3. Click Run (▶️)
4. ⚠️ Remember: Switch to physical device for ALL measurements!

### Option B: Cloud Mac (If No Mac Available)
- **MacStadium**: Rent Mac mini in cloud ($79-99/month)
- **MacinCloud**: Pay-per-hour Mac access
- **AWS Mac instances**: EC2 mac1.metal or mac2.metal
- Still need physical iPhone for measurements

### Option C: Simplified Python-Only Approach
- Skip native iOS app development
- Use MLC LLM Python bindings with iOS device connected
- More limited profiling capabilities
- Still need physical iPhone
- Still valuable research outcomes

## Questions or Issues?

Document any blockers you encounter, and I'll help solve them!

## Progress Tracking

Track your setup progress:
- [ ] Hardware ready
- [ ] Xcode installed
- [ ] Developer account configured
- [ ] Model downloaded
- [ ] Python environment set up
- [ ] First app build successful
- [ ] First measurement completed

