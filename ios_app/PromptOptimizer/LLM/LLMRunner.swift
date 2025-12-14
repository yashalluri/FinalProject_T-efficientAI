//
//  LLMRunner.swift
//  PromptOptimizer
//
//  Manages LLM inference using llama.cpp
//

import Foundation
import UIKit

class LLMRunner: ObservableObject {
    @Published var isLoaded: Bool = false
    @Published var currentModel: String = ""
    
    private var modelPath: String?
    private var contextSize: Int = 2048
    private var maxTokens: Int = 512
    
    // MARK: - Model Loading
    
    func loadModel(name: String) async throws {
        print("📦 Loading model: \(name)")
        
        // Get model path from bundle or documents
        guard let path = getModelPath(name: name) else {
            throw LLMError.modelNotFound
        }
        
        modelPath = path
        
        // Initialize llama.cpp context
        // This is a placeholder - actual implementation would call llama.cpp C API
        try await initializeLlamaCpp(modelPath: path)
        
        await MainActor.run {
            self.isLoaded = true
            self.currentModel = name
        }
        
        print("✅ Model loaded successfully")
    }
    
    private func getModelPath(name: String) -> String? {
        // Check app bundle first
        if let bundlePath = Bundle.main.path(forResource: name, ofType: "gguf") {
            return bundlePath
        }
        
        // Check documents directory
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let modelPath = documentsPath.appendingPathComponent("models/\(name).gguf")
        
        if FileManager.default.fileExists(atPath: modelPath.path) {
            return modelPath.path
        }
        
        return nil
    }
    
    private func initializeLlamaCpp(modelPath: String) async throws {
        // Placeholder for actual llama.cpp initialization
        // In real implementation, this would:
        // 1. Load model weights
        // 2. Initialize KV cache
        // 3. Setup sampling parameters
        
        try await Task.sleep(nanoseconds: 2_000_000_000) // Simulate loading time
    }
    
    // MARK: - Inference
    
    func runInference(prompt: String, profiler: PerformanceProfiler) async throws -> InferenceResults {
        guard isLoaded else {
            throw LLMError.modelNotLoaded
        }
        
        print("🚀 Starting inference for prompt: \(prompt.prefix(50))...")
        
        // Start profiling
        profiler.startProfiling()
        
        let startTime = Date()
        
        // Tokenize prompt
        let promptTokens = tokenize(prompt)
        print("📝 Prompt tokens: \(promptTokens.count)")
        
        // Prefill phase - process prompt tokens
        let prefillStart = Date()
        try await prefillPhase(tokens: promptTokens)
        let prefillTime = Date().timeIntervalSince(prefillStart)
        print("⏱️ Prefill time: \(prefillTime)s")
        
        // Decode phase - generate tokens
        let decodeStart = Date()
        let generatedTokens = try await decodePhase(maxTokens: maxTokens)
        let decodeTime = Date().timeIntervalSince(decodeStart)
        print("⏱️ Decode time: \(decodeTime)s")
        
        let totalTime = Date().timeIntervalSince(startTime)
        
        // Stop profiling
        let metrics = profiler.stopProfiling()
        
        // Detokenize output
        let outputText = detokenize(generatedTokens)
        
        // Calculate metrics
        let tokensPerSecond = Double(generatedTokens.count) / decodeTime
        let prefillTPS = Double(promptTokens.count) / prefillTime
        let decodeTPS = Double(generatedTokens.count) / decodeTime
        
        // Create results
        let results = InferenceResults(
            id: UUID().uuidString,
            timestamp: Date(),
            promptId: "manual_\(Int(Date().timeIntervalSince1970))",
            promptText: prompt,
            promptLength: prompt.count,
            promptWordCount: prompt.split(separator: " ").count,
            prefillTime: prefillTime,
            decodeTime: decodeTime,
            totalTime: totalTime,
            firstTokenLatency: metrics.firstTokenLatency,
            tokensPerSecond: tokensPerSecond,
            prefillTokensPerSecond: prefillTPS,
            decodeTokensPerSecond: decodeTPS,
            promptTokens: promptTokens.count,
            generatedTokens: generatedTokens.count,
            totalTokens: promptTokens.count + generatedTokens.count,
            peakMemoryMB: metrics.peakMemoryMB,
            averageMemoryMB: metrics.averageMemoryMB,
            estimatedEnergyJ: metrics.estimatedEnergyJ,
            cpuEnergyJ: metrics.cpuEnergyJ,
            gpuEnergyJ: metrics.gpuEnergyJ,
            outputText: outputText,
            outputLength: outputText.count,
            modelName: currentModel,
            modelSize: "7B-Q4",
            deviceModel: UIDevice.current.model,
            iosVersion: UIDevice.current.systemVersion,
            batteryLevel: UIDevice.current.batteryLevel,
            thermalState: getThermalState()
        )
        
        // Save results
        try saveResults(results)
        
        print("✅ Inference complete!")
        return results
    }
    
    private func prefillPhase(tokens: [Int]) async throws {
        // Placeholder for actual prefill
        // In real implementation, this would process all prompt tokens at once
        try await Task.sleep(nanoseconds: UInt64(Double(tokens.count) * 10_000_000)) // ~10ms per token
    }
    
    private func decodePhase(maxTokens: Int) async throws -> [Int] {
        // Placeholder for actual decoding
        // In real implementation, this would generate tokens one by one
        var tokens: [Int] = []
        
        for _ in 0..<min(maxTokens, 100) {
            try await Task.sleep(nanoseconds: 50_000_000) // ~50ms per token
            tokens.append(Int.random(in: 0..<32000)) // Random token ID
            
            // Stop if EOS token (placeholder)
            if tokens.count > 20 && Bool.random() {
                break
            }
        }
        
        return tokens
    }
    
    // MARK: - Tokenization
    
    private func tokenize(_ text: String) -> [Int] {
        // Placeholder tokenization
        // Real implementation would use llama.cpp tokenizer
        let words = text.split(separator: " ")
        return words.map { _ in Int.random(in: 0..<32000) }
    }
    
    private func detokenize(_ tokens: [Int]) -> String {
        // Placeholder detokenization
        // Real implementation would use llama.cpp detokenizer
        let words = (0..<tokens.count).map { _ in 
            ["The", "cat", "sat", "on", "the", "mat", "and", "looked", "around"].randomElement()!
        }
        return words.joined(separator: " ")
    }
    
    // MARK: - Utilities
    
    private func getThermalState() -> String {
        switch ProcessInfo.processInfo.thermalState {
        case .nominal: return "nominal"
        case .fair: return "fair"
        case .serious: return "serious"
        case .critical: return "critical"
        @unknown default: return "unknown"
        }
    }
    
    private func saveResults(_ results: InferenceResults) throws {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        let data = try encoder.encode(results)
        
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let resultsDir = documentsPath.appendingPathComponent("results")
        
        let filename = "result_\(Int(results.timestamp.timeIntervalSince1970)).json"
        let filePath = resultsDir.appendingPathComponent(filename)
        
        try data.write(to: filePath)
        print("💾 Saved results to: \(filePath.lastPathComponent)")
    }
}

// MARK: - Error Types

enum LLMError: Error {
    case modelNotFound
    case modelNotLoaded
    case inferenceError(String)
    case tokenizationError
}

