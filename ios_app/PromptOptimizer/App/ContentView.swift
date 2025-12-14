//
//  ContentView.swift
//  PromptOptimizer
//
//  Main user interface
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var appState: AppState
    @StateObject private var llmRunner = LLMRunner()
    @StateObject private var profiler = PerformanceProfiler()
    
    @State private var selectedPrompt: String = ""
    @State private var promptInput: String = ""
    @State private var optimizedPrompt: String = ""
    @State private var showingResults: Bool = false
    @State private var isRunningTest: Bool = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Model Status Section
                    modelStatusSection
                    
                    // Prompt Input Section
                    promptInputSection
                    
                    // Optimization Section
                    optimizationSection
                    
                    // Action Buttons
                    actionButtonsSection
                    
                    // Results Preview
                    if let results = appState.lastResults {
                        resultsPreviewSection(results: results)
                    }
                }
                .padding()
            }
            .navigationTitle("Prompt Optimizer")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Menu {
                        Button("Load Model") {
                            loadModel()
                        }
                        Button("Run Baseline Test") {
                            runBaselineTest()
                        }
                        Button("Export Results") {
                            exportResults()
                        }
                        Button("Settings") {
                            // Navigate to settings
                        }
                    } label: {
                        Image(systemName: "ellipsis.circle")
                    }
                }
            }
        }
    }
    
    // MARK: - View Components
    
    var modelStatusSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Model Status")
                .font(.headline)
            
            HStack {
                Circle()
                    .fill(appState.modelLoaded ? Color.green : Color.red)
                    .frame(width: 12, height: 12)
                
                Text(appState.modelLoaded ? "Model Loaded: \(appState.currentModel)" : "No Model Loaded")
                    .font(.subheadline)
                
                Spacer()
                
                if !appState.modelLoaded {
                    Button("Load") {
                        loadModel()
                    }
                    .buttonStyle(.bordered)
                }
            }
            
            if appState.isInferencing {
                ProgressView("Running inference...")
                    .progressViewStyle(.linear)
            }
        }
        .padding()
        .background(Color.gray.opacity(0.1))
        .cornerRadius(10)
    }
    
    var promptInputSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Enter Prompt")
                .font(.headline)
            
            TextEditor(text: $promptInput)
                .frame(minHeight: 100)
                .padding(8)
                .background(Color.gray.opacity(0.1))
                .cornerRadius(8)
                .onChange(of: promptInput) { newValue in
                    // Auto-optimize when user stops typing (debounced)
                    optimizePromptDebounced()
                }
            
            HStack {
                Text("\(promptInput.count) chars")
                    .font(.caption)
                    .foregroundColor(.gray)
                
                Spacer()
                
                Text("\(promptInput.split(separator: " ").count) words")
                    .font(.caption)
                    .foregroundColor(.gray)
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(10)
        .shadow(radius: 2)
    }
    
    var optimizationSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Text("Optimized Prompt")
                    .font(.headline)
                
                Spacer()
                
                if !optimizedPrompt.isEmpty {
                    Button("Use This") {
                        promptInput = optimizedPrompt
                    }
                    .buttonStyle(.borderedProminent)
                    .controlSize(.small)
                }
            }
            
            if optimizedPrompt.isEmpty {
                Text("Enter a prompt above to see optimization suggestions")
                    .font(.subheadline)
                    .foregroundColor(.gray)
                    .italic()
            } else {
                Text(optimizedPrompt)
                    .padding()
                    .background(Color.green.opacity(0.1))
                    .cornerRadius(8)
                
                // Efficiency prediction
                efficiencyComparison
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(10)
        .shadow(radius: 2)
    }
    
    var efficiencyComparison: some View {
        VStack(spacing: 8) {
            HStack {
                Label("Est. Latency", systemImage: "clock")
                    .font(.caption)
                Spacer()
                Text("-15%")
                    .font(.caption)
                    .foregroundColor(.green)
            }
            
            HStack {
                Label("Est. Energy", systemImage: "battery.100")
                    .font(.caption)
                Spacer()
                Text("-12%")
                    .font(.caption)
                    .foregroundColor(.green)
            }
            
            HStack {
                Label("Quality", systemImage: "checkmark.seal")
                    .font(.caption)
                Spacer()
                Text("Maintained")
                    .font(.caption)
                    .foregroundColor(.blue)
            }
        }
        .padding()
        .background(Color.gray.opacity(0.05))
        .cornerRadius(8)
    }
    
    var actionButtonsSection: some View {
        VStack(spacing: 12) {
            Button(action: runInference) {
                HStack {
                    Image(systemName: "play.circle.fill")
                    Text("Run Inference")
                }
                .frame(maxWidth: .infinity)
                .padding()
                .background(appState.modelLoaded ? Color.blue : Color.gray)
                .foregroundColor(.white)
                .cornerRadius(10)
            }
            .disabled(!appState.modelLoaded || promptInput.isEmpty || isRunningTest)
            
            HStack(spacing: 12) {
                Button(action: { runBatchTest() }) {
                    HStack {
                        Image(systemName: "list.bullet")
                        Text("Batch Test")
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.orange)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .disabled(!appState.modelLoaded || isRunningTest)
                
                Button(action: { showingResults = true }) {
                    HStack {
                        Image(systemName: "chart.bar")
                        Text("View Results")
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.purple)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
            }
        }
    }
    
    func resultsPreviewSection(results: InferenceResults) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Latest Results")
                .font(.headline)
            
            Grid(alignment: .leading, horizontalSpacing: 20, verticalSpacing: 8) {
                GridRow {
                    Text("Total Time:")
                        .font(.subheadline)
                    Text(String(format: "%.2f s", results.totalTime))
                        .font(.subheadline)
                        .bold()
                }
                
                GridRow {
                    Text("Tokens/sec:")
                        .font(.subheadline)
                    Text(String(format: "%.1f", results.tokensPerSecond))
                        .font(.subheadline)
                        .bold()
                }
                
                GridRow {
                    Text("Memory:")
                        .font(.subheadline)
                    Text(String(format: "%.0f MB", results.peakMemoryMB))
                        .font(.subheadline)
                        .bold()
                }
                
                if let energy = results.estimatedEnergyJ {
                    GridRow {
                        Text("Energy:")
                            .font(.subheadline)
                        Text(String(format: "%.2f J", energy))
                            .font(.subheadline)
                            .bold()
                    }
                }
            }
        }
        .padding()
        .background(Color.blue.opacity(0.1))
        .cornerRadius(10)
    }
    
    // MARK: - Actions
    
    func loadModel() {
        Task {
            appState.modelLoaded = false
            appState.currentModel = "Loading..."
            
            // Simulate model loading (replace with actual implementation)
            do {
                try await llmRunner.loadModel(name: "mistral-7b-instruct-v0.2.Q4_K_M")
                await MainActor.run {
                    appState.modelLoaded = true
                    appState.currentModel = "Mistral 7B"
                }
            } catch {
                print("Error loading model: \(error)")
                await MainActor.run {
                    appState.currentModel = "Load Failed"
                }
            }
        }
    }
    
    func optimizePromptDebounced() {
        // Implement debounced optimization
        Task {
            try? await Task.sleep(nanoseconds: 500_000_000) // 0.5s delay
            optimizePrompt()
        }
    }
    
    func optimizePrompt() {
        let optimizer = PromptOptimizer()
        optimizedPrompt = optimizer.optimize(promptInput)
    }
    
    func runInference() {
        guard !promptInput.isEmpty else { return }
        
        isRunningTest = true
        appState.isInferencing = true
        
        Task {
            do {
                let results = try await llmRunner.runInference(
                    prompt: promptInput,
                    profiler: profiler
                )
                
                await MainActor.run {
                    appState.lastResults = results
                    appState.isInferencing = false
                    isRunningTest = false
                }
            } catch {
                print("Inference error: \(error)")
                await MainActor.run {
                    appState.isInferencing = false
                    isRunningTest = false
                }
            }
        }
    }
    
    func runBaselineTest() {
        isRunningTest = true
        
        Task {
            // Load baseline prompts and run tests
            print("Running baseline test...")
            try? await Task.sleep(nanoseconds: 2_000_000_000)
            
            await MainActor.run {
                isRunningTest = false
            }
        }
    }
    
    func runBatchTest() {
        // Implement batch testing
        print("Running batch test...")
    }
    
    func exportResults() {
        // Implement results export
        print("Exporting results...")
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(AppState())
    }
}

