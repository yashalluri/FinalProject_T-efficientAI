# iOS Simulator Quick Start

If you want to start developing using the iOS Simulator while setting up your physical device, follow these steps.

## Prerequisites

- ✅ Mac with Xcode installed
- ✅ macOS Ventura 13.0+ or Sonoma 14.0+
- ✅ Xcode 15.0+
- ❌ No iPhone needed (yet)
- ❌ No Apple Developer account needed (for simulator only)

## Step 1: Open Project in Xcode

```bash
cd /Users/yashalluri/Desktop/FinalProject
open ios_app/PromptOptimizer.xcodeproj
```

If you don't have an Xcode project yet, you'll need to create one first.

## Step 2: Create Xcode Project (If Needed)

If the `.xcodeproj` doesn't exist yet:

1. Open Xcode
2. File → New → Project
3. Choose "iOS" → "App"
4. Settings:
   - **Product Name**: PromptOptimizer
   - **Interface**: SwiftUI
   - **Language**: Swift
   - **Save in**: `/Users/yashalluri/Desktop/FinalProject/ios_app/`

5. Add the Swift files we created:
   - Drag files from `ios_app/PromptOptimizer/` into Xcode project navigator
   - Check "Copy items if needed"
   - Check "Create groups"

## Step 3: Select Simulator

In Xcode toolbar (top left):

```
iPhone 16 Pro Max (Simulator)  ▼
```

Click dropdown → Choose:
- **iPhone 16 Pro Max** (matches your target device)
- Or any iPhone with iOS 17.0+

## Step 4: Build and Run

Click the **Play** button (▶️) or press **Cmd+R**

First build takes 2-5 minutes. Subsequent builds are faster.

## Step 5: Using the Simulator

### Basic Controls

- **Rotate**: Cmd+Left/Right Arrow
- **Home button**: Cmd+Shift+H
- **Screenshot**: Cmd+S
- **Shake gesture**: Ctrl+Cmd+Z

### Simulator Features

✅ Works:
- UI testing
- Navigation
- App logic
- Debugging
- SwiftUI previews

⚠️ Limited/Different:
- Performance (faster than real device)
- Memory usage (different patterns)
- Battery (N/A)
- Thermal state (always normal)

## Step 6: Test Basic Functionality

In the app simulator:

1. ✅ Check UI loads correctly
2. ✅ Test navigation between views
3. ✅ Try entering a prompt
4. ✅ Check if optimization suggestions appear
5. ⚠️ Model loading (may not work without actual model file)
6. ⚠️ Inference (will be simulated/placeholder)

## Step 7: Mock Data for Development

Since you can't run real LLM inference in simulator efficiently, use mock data:

### In `LLMRunner.swift`:

The current implementation already has placeholder/mock inference. This is perfect for simulator testing.

### In `PerformanceProfiler.swift`:

Energy readings will return `nil` or placeholder values in simulator - this is expected.

## Debugging in Simulator

### View Console Output

In Xcode:
- **View** → **Debug Area** → **Show Debug Area** (Cmd+Shift+Y)
- See print statements and errors here

### Breakpoints

1. Click line number in code editor (blue marker appears)
2. Run app
3. Execution pauses at breakpoint
4. Inspect variables in debug area

### Memory Graph

- **Debug** → **Memory Graph**
- Check for memory leaks
- View object allocations

## Common Issues

### "No such module" Error

```
Solution:
1. Clean build folder: Product → Clean Build Folder (Cmd+Shift+K)
2. Rebuild: Product → Build (Cmd+B)
```

### Simulator Crashes

```
Solution:
1. Reset simulator: Device → Erase All Content and Settings
2. Restart Xcode
3. Rebuild
```

### Code Signing Issues

```
For simulator, you shouldn't need code signing.

If asked:
1. Select project in navigator
2. Signing & Capabilities tab
3. Uncheck "Automatically manage signing" for simulator builds
```

## Limitations to Remember

### For Research - You CANNOT:

- ❌ Collect valid energy measurements
- ❌ Collect valid performance metrics
- ❌ Test thermal behavior
- ❌ Measure battery impact
- ❌ Validate real-world latency
- ❌ Use results in research paper

### For Development - You CAN:

- ✅ Test UI/UX
- ✅ Debug app logic
- ✅ Fix crashes
- ✅ Prototype features
- ✅ Learn Swift/SwiftUI
- ✅ Prepare for device deployment

## Transition to Physical Device

When ready to collect real data:

### 1. Connect iPhone

- USB-C cable to Mac
- Trust computer on iPhone
- Enable Developer Mode

### 2. Change Target in Xcode

- Top toolbar: Select **your actual iPhone** from dropdown
- Will show as "Yashwanth's iPhone" or similar

### 3. Build to Device

- First time: Xcode will install provisioning profile
- May need Apple ID for free developer account
- Subsequent builds are fast

### 4. Start Real Measurements

Now you can collect valid research data! 🎉

## Development Workflow

### Recommended Approach:

```
1. Write code on Mac
2. Test in Simulator (quick iteration)
3. When feature works → deploy to iPhone
4. Verify on iPhone
5. Collect measurements on iPhone
6. Analyze data on Mac
```

### Time Estimates:

- Simulator build: 30 seconds - 2 minutes
- Device build: 1-3 minutes (first time)
- Device build: 30 seconds (subsequent)

## Next Steps

After getting familiar with simulator:

1. ✅ Review the app architecture
2. ✅ Understand the code structure  
3. ✅ Test UI flows
4. ✅ Prepare datasets on Mac
5. ✅ Plan experiments
6. ⏸️ **Then switch to physical device for measurements**

## Getting Help

### Xcode Issues

- View → Navigators → Show Report Navigator (Cmd+9)
- Check build errors and warnings

### Swift Errors

- Most errors have fix-it suggestions (yellow/red icons)
- Click for automatic fixes

### Simulator Issues

- If simulator is slow: Close other apps
- If simulator freezes: Device → Restart
- Nuclear option: Delete simulator and create new one

## Summary

**Simulator is great for**: Learning, developing, debugging ✅

**Physical device required for**: All research measurements ⚠️

**Start here**: Build in simulator to learn

**Finish here**: Collect all data on iPhone 16 Pro Max 📱

Ready to start? Run:

```bash
open ios_app/PromptOptimizer.xcodeproj
```

Then click ▶️ and experiment! 🚀

