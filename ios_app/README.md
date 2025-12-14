# iOS App - Prompt Optimizer

Native iOS application for running LLMs locally and measuring performance metrics.

## Architecture

```
PromptOptimizer/
├── App/
│   ├── PromptOptimizerApp.swift     # App entry point
│   ├── ContentView.swift             # Main UI
│   └── Views/                        # UI components
├── LLM/
│   ├── LLMRunner.swift               # LLM inference engine
│   ├── ModelLoader.swift             # Model loading
│   └── TokenCounter.swift            # Token utilities
├── Profiling/
│   ├── PerformanceProfiler.swift    # Metrics collection
│   ├── EnergyMonitor.swift          # Energy measurement
│   └── MetricsLogger.swift          # Data logging
├── Optimization/
│   ├── PromptOptimizer.swift        # Optimization engine
│   └── OptimizationRules.swift      # Rules database
└── Resources/
    └── Info.plist

```

## Building

### Prerequisites
- Xcode 15.0+
- iOS 17.0+ deployment target
- llama.cpp built for iOS

### Build Steps

1. Open project:
```bash
open PromptOptimizer.xcodeproj
```

2. Select your iPhone as target device

3. Update Bundle Identifier in project settings

4. Build and Run (Cmd+R)

## Integration with llama.cpp

The app uses llama.cpp for local inference:

1. Build llama.cpp as iOS framework
2. Link framework in Xcode project
3. Call C++ functions via Swift bridging

See `LLMRunner.swift` for integration details.

## Profiling on Device

### Energy Measurement
Uses MetricKit to capture:
- CPU energy
- GPU energy
- Network energy
- Display energy

### Performance Metrics
- Prefill latency
- Decode latency (per token)
- Total inference time
- Tokens per second
- Peak memory usage

### Data Export
Metrics saved as JSON to app documents directory, accessible via:
- Files app on iPhone
- Xcode: Window > Devices and Simulators > Download Container

## Testing

Run baseline test:
1. Launch app
2. Tap "Load Model"
3. Tap "Run Baseline Test"
4. View results in app or export

## Troubleshooting

### Model Loading Fails
- Check model file in app bundle
- Verify GGUF format
- Ensure enough memory available

### Profiling Not Working
- Run on physical device (not simulator)
- Grant necessary permissions
- Check MetricKit entitlements

### Build Errors
- Clean build folder
- Update llama.cpp to latest
- Check minimum iOS version

