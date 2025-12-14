//
//  PromptOptimizerApp.swift
//  PromptOptimizer
//
//  Main application entry point
//

import SwiftUI

@main
struct PromptOptimizerApp: App {
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
    }
}

/// Global application state
class AppState: ObservableObject {
    @Published var modelLoaded: Bool = false
    @Published var currentModel: String = ""
    @Published var isInferencing: Bool = false
    @Published var lastResults: InferenceResults?
    
    init() {
        setupDirectories()
    }
    
    private func setupDirectories() {
        let fileManager = FileManager.default
        let documentsPath = fileManager.urls(for: .documentDirectory, in: .userDomainMask)[0]
        
        let directories = ["results", "logs", "exports"]
        for dir in directories {
            let dirPath = documentsPath.appendingPathComponent(dir)
            try? fileManager.createDirectory(at: dirPath, withIntermediateDirectories: true)
        }
    }
}

/// Structure to hold inference results
struct InferenceResults: Codable, Identifiable {
    let id: String
    let timestamp: Date
    let promptId: String
    let promptText: String
    let promptLength: Int
    let promptWordCount: Int
    
    // Timing metrics
    let prefillTime: Double  // seconds
    let decodeTime: Double   // seconds
    let totalTime: Double    // seconds
    let firstTokenLatency: Double
    
    // Throughput
    let tokensPerSecond: Double
    let prefillTokensPerSecond: Double
    let decodeTokensPerSecond: Double
    
    // Token counts
    let promptTokens: Int
    let generatedTokens: Int
    let totalTokens: Int
    
    // Memory
    let peakMemoryMB: Double
    let averageMemoryMB: Double
    
    // Energy (if available)
    let estimatedEnergyJ: Double?
    let cpuEnergyJ: Double?
    let gpuEnergyJ: Double?
    
    // Output
    let outputText: String
    let outputLength: Int
    
    // Model info
    let modelName: String
    let modelSize: String
    
    // Device info
    let deviceModel: String
    let iosVersion: String
    let batteryLevel: Double
    let thermalState: String
}

