# 🚀 START HERE - You Have iPhone, Now What?

Since you have your iPhone 16 Pro Max, here are your **exact next steps** to get from code to working system.

## 📋 Checklist - Do These in Order

### ✅ Step 1: Install Xcode (30-60 min)

```bash
# Open Mac App Store
# Search "Xcode"
# Click "Get" or "Install"
# Wait (it's ~15GB, takes time)
```

**While Xcode installs**, continue to Step 2!

---

### ✅ Step 2: Setup Python Environment (5 min)

```bash
# Open Terminal, navigate to project
cd /Users/yashalluri/Desktop/FinalProject

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output**: All packages install successfully ✅

---

### ✅ Step 3: Prepare Datasets (10 min)

```bash
# Still in Terminal, with venv activated
python3 datasets/prepare_datasets.py
```

**Expected output**: 
```
✅ Loaded 100 SQuAD prompts
✅ Loaded 100 IMDB prompts
✅ Loaded 100 generation prompts
✅ Loaded 100 reasoning prompts
✅ Dataset preparation complete!
```

---

### ✅ Step 4: Download LLM Model (20-30 min)

**Choose ONE model to start:**

#### Option A: Mistral 7B (Recommended, ~4.4GB)
1. Go to: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF
2. Click "Files and versions"
3. Download: `mistral-7b-instruct-v0.2.Q4_K_M.gguf`
4. Move to: `/Users/yashalluri/Desktop/FinalProject/models/`

#### Option B: Gemma 7B (~4.9GB)
1. Go to: https://huggingface.co/lmstudio-ai/gemma-7b-it-GGUF
2. Download: `gemma-7b-it.Q4_K_M.gguf`
3. Move to `models/` folder

```bash
# Create models folder if needed
mkdir -p /Users/yashalluri/Desktop/FinalProject/models

# Verify model is there
ls -lh /Users/yashalluri/Desktop/FinalProject/models/
```

---

### ✅ Step 5: Create Xcode Project (15 min)

**NOW Xcode should be installed. Open it:**

```bash
# Launch Xcode
open -a Xcode
```

**Create new project:**

1. **Welcome screen** → "Create a new Xcode project"
2. **Choose template:**
   - Platform: **iOS**
   - Template: **App**
   - Click **Next**

3. **Project settings:**
   - **Product Name**: `PromptOptimizer`
   - **Team**: Select your Apple ID (or "None" if not logged in)
   - **Organization Identifier**: `com.yourname` (or anything)
   - **Interface**: **SwiftUI** ⚠️ Important!
   - **Language**: **Swift** ⚠️ Important!
   - **Storage**: **None** (uncheck all boxes)
   - Click **Next**

4. **Save location:**
   - Navigate to: `/Users/yashalluri/Desktop/FinalProject/`
   - Create new folder: `ios_app_project`
   - Save there
   - ⚠️ **UNCHECK** "Create Git repository"

5. **Xcode opens your new project** ✅

---

### ✅ Step 6: Add Swift Files to Project (10 min)

**In Xcode:**

1. **Delete default files:**
   - Right-click `ContentView.swift` → Delete → "Move to Trash"
   - Right-click `PromptOptimizerApp.swift` → Delete → "Move to Trash"

2. **Add our files:**
   - In Finder, open: `/Users/yashalluri/Desktop/FinalProject/ios_app/PromptOptimizer/`
   
   - **Drag these folders** into Xcode project navigator:
     - `App/` folder
     - `LLM/` folder
     - `Profiling/` folder
     - `Optimization/` folder
   
   - When dialog appears:
     - ✅ Check "Copy items if needed"
     - ✅ Check "Create groups"
     - ✅ Target: PromptOptimizer
     - Click **Finish**

3. **Your project structure should look like:**
   ```
   PromptOptimizer
   ├── App/
   │   ├── PromptOptimizerApp.swift
   │   └── ContentView.swift
   ├── LLM/
   │   └── LLMRunner.swift
   ├── Profiling/
   │   └── PerformanceProfiler.swift
   └── Optimization/
       └── PromptOptimizer.swift
   ```

---

### ✅ Step 7: Configure Project Settings (5 min)

**In Xcode:**

1. **Click project name** (blue icon) at top of navigator
2. **Select "PromptOptimizer" target** (not project)
3. **General tab:**
   - **Minimum Deployments**: iOS 17.0
   - **iPhone**: Check ✅
   - **iPad**: Uncheck ⬜

4. **Signing & Capabilities tab:**
   - **Team**: Select your Apple ID
   - If not logged in: Xcode → Preferences → Accounts → Add Apple ID
   - **Free account works fine!**

---

### ✅ Step 8: Connect Your iPhone (5 min)

1. **Connect iPhone to Mac** via USB-C cable
2. **On iPhone:**
   - Settings → Privacy & Security → Developer Mode
   - Toggle **ON**
   - Restart iPhone
   - **Trust this computer** (popup)

3. **In Xcode:**
   - Top bar: Device dropdown (currently says "iPhone 15 Pro" or similar)
   - Select **your iPhone** (e.g., "Yashwanth's iPhone")
   - It should show connected (not "unavailable")

---

### ✅ Step 9: First Build! (5-10 min)

**In Xcode:**

1. **Product menu** → **Clean Build Folder** (Cmd+Shift+K)
2. **Product menu** → **Build** (Cmd+B)

**Expected:**
- Build progress bar appears
- Some warnings OK (ignore for now)
- Should say "Build Succeeded" ✅

**If errors:**
- Most common: Missing imports
- Check that all files are added
- Check iOS version is 17.0+

---

### ✅ Step 10: Deploy to iPhone! (First time: 5 min)

**In Xcode:**

1. Click **Play button** ▶️ (or Cmd+R)
2. **On iPhone**: You may see "Untrusted Developer"
   - Settings → General → VPN & Device Management
   - Trust your Apple ID
   - Go back to home screen
3. **App launches!** 🎉

---

### ✅ Step 11: First Test Run (10 min)

**On your iPhone (app is now running):**

1. **Load Model:**
   - Tap menu (•••) → "Load Model"
   - Wait ~30 seconds (model loading)
   - Should say "Model Loaded: Mistral 7B" ✅

2. **Test a prompt:**
   - Type: "What is the capital of France?"
   - Tap "Run Inference"
   - Wait for results
   - See timing metrics! 🎉

3. **Try baseline test:**
   - Menu → "Run Baseline Test"
   - App runs 10 prompts automatically
   - Takes ~5-10 minutes
   - Results saved automatically

---

### ✅ Step 12: View Results (5 min)

**Back on Mac:**

```bash
# Navigate to project
cd /Users/yashalluri/Desktop/FinalProject

# Check results (results are in app documents, need to export)
# For now, view in app or export via Xcode

# Or run analysis on any exported results:
python3 analysis/latency_analysis.py --results-dir results/
```

---

## 🎯 You're Done with Setup! What Now?

### Week 1 Goals (This Week):
- ✅ Complete all 12 steps above
- ✅ Run baseline test successfully
- ✅ Export first results
- ✅ Verify data looks reasonable

### Week 2-3 Goals:
- Run all prompt categories (QA, sentiment, etc.)
- Collect 200+ inferences
- Start analysis

---

## ❓ Troubleshooting

### "Build Failed" in Xcode
```bash
# Clean and rebuild
Cmd+Shift+K (clean)
Cmd+B (build)
```

### "Code signing error"
- Xcode → Preferences → Accounts
- Add your Apple ID
- Select it as Team in project settings

### "No such module 'MetricKit'"
- Check Minimum Deployment: iOS 17.0+
- MetricKit available iOS 13+

### "Cannot load model"
- Verify model file exists in models/ folder
- Check it's GGUF format (not GGML)
- Check filename matches code

### iPhone not showing in Xcode
- Unplug and replug USB-C
- Trust computer on iPhone
- Restart Xcode

### App crashes on launch
- Check Xcode console for error
- Verify all files added correctly
- Try clean build

---

## 📞 Current Status Check

After completing these steps, you should have:

- ✅ Xcode installed
- ✅ Python environment setup
- ✅ Datasets prepared (400+ prompts)
- ✅ Model downloaded (~4-5GB)
- ✅ iOS app created in Xcode
- ✅ All Swift files added
- ✅ iPhone connected and trusted
- ✅ App deployed to iPhone
- ✅ First inference completed
- ✅ Baseline test run
- ✅ Results collected

**If you have all ✅ above → You're ready for Week 2 (experiments)!**

**If stuck on any step → Tell me which step and what error!**

---

## 🚀 Quick Start Summary

```bash
# Terminal commands (copy-paste):
cd /Users/yashalluri/Desktop/FinalProject
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 datasets/prepare_datasets.py
```

Then:
1. Download model from HuggingFace
2. Create Xcode project
3. Add Swift files
4. Connect iPhone
5. Build and Run!

**Time estimate: 2-3 hours total** (mostly waiting for downloads)

---

## 🎓 Learning Resources

While downloads happen:
- Read: [EXPERIMENT_GUIDE.md](docs/EXPERIMENT_GUIDE.md)
- Review: Swift files to understand code
- Plan: Which experiments to run first

---

## ✅ Next Message to Me

After you complete these steps, tell me:

1. ✅ "Done with Step X" (where are you?)
2. ❌ "Stuck on Step X with error: ___"
3. ❓ "Question about: ___"

**Ready? Start with Step 1!** 🚀

