//
//  PromptOptimizer.swift
//  PromptOptimizer
//
//  Prompt optimization engine
//

import Foundation

class PromptOptimizer {
    
    // Optimization rules
    private let rules = OptimizationRules()
    
    // Keywords that increase verbosity
    private let verboseKeywords = [
        "explain", "analyze", "describe in detail", "elaborate",
        "provide a comprehensive", "thoroughly", "extensively"
    ]
    
    // Keywords that reduce efficiency
    private let inefficientPhrases = [
        "step by step", "think carefully", "make sure to",
        "please provide", "I would like you to"
    ]
    
    struct OptimizationSuggestion {
        let optimizedPrompt: String
        let changes: [String]
        let estimatedLatencyReduction: Double // percentage
        let estimatedEnergyReduction: Double  // percentage
        let qualityImpact: String // "maintained", "improved", "slightly reduced"
    }
    
    // MARK: - Main Optimization
    
    func optimize(_ prompt: String) -> String {
        var optimized = prompt
        
        // Apply optimization rules
        optimized = removeRedundancy(optimized)
        optimized = simplifyInstructions(optimized)
        optimized = removeVerboseTriggers(optimized)
        optimized = consolidateQuestions(optimized)
        optimized = optimizeFormatting(optimized)
        
        return optimized
    }
    
    func optimizeWithDetails(_ prompt: String) -> OptimizationSuggestion {
        var changes: [String] = []
        var optimized = prompt
        
        // Track each optimization
        let original = optimized
        
        optimized = removeRedundancy(optimized)
        if optimized != original {
            changes.append("Removed redundant phrasing")
        }
        
        let beforeInstructions = optimized
        optimized = simplifyInstructions(optimized)
        if optimized != beforeInstructions {
            changes.append("Simplified instructions")
        }
        
        let beforeVerbose = optimized
        optimized = removeVerboseTriggers(optimized)
        if optimized != beforeVerbose {
            changes.append("Removed verbose triggers")
        }
        
        let beforeConsolidate = optimized
        optimized = consolidateQuestions(optimized)
        if optimized != beforeConsolidate {
            changes.append("Consolidated questions")
        }
        
        let beforeFormat = optimized
        optimized = optimizeFormatting(optimized)
        if optimized != beforeFormat {
            changes.append("Optimized formatting")
        }
        
        // Estimate improvements
        let latencyReduction = estimateLatencyReduction(original: prompt, optimized: optimized)
        let energyReduction = estimateEnergyReduction(original: prompt, optimized: optimized)
        let qualityImpact = assessQualityImpact(original: prompt, optimized: optimized)
        
        return OptimizationSuggestion(
            optimizedPrompt: optimized,
            changes: changes,
            estimatedLatencyReduction: latencyReduction,
            estimatedEnergyReduction: energyReduction,
            qualityImpact: qualityImpact
        )
    }
    
    // MARK: - Optimization Rules
    
    private func removeRedundancy(_ prompt: String) -> String {
        var result = prompt
        
        // Remove redundant politeness
        result = result.replacingOccurrences(of: "Please ", with: "")
        result = result.replacingOccurrences(of: "Could you ", with: "")
        result = result.replacingOccurrences(of: "I would like you to ", with: "")
        result = result.replacingOccurrences(of: "Can you please ", with: "")
        
        // Remove redundant instructions
        result = result.replacingOccurrences(of: "Make sure to ", with: "")
        result = result.replacingOccurrences(of: "Be sure to ", with: "")
        
        return result
    }
    
    private func simplifyInstructions(_ prompt: String) -> String {
        var result = prompt
        
        // Simplify complex instructions
        let simplifications = [
            "Provide a detailed explanation of": "Explain",
            "Give me a comprehensive overview of": "Describe",
            "I need you to analyze": "Analyze",
            "Can you help me understand": "Explain",
            "Please describe in detail": "Describe",
            "Thoroughly explain": "Explain"
        ]
        
        for (complex, simple) in simplifications {
            result = result.replacingOccurrences(of: complex, with: simple, options: .caseInsensitive)
        }
        
        return result
    }
    
    private func removeVerboseTriggers(_ prompt: String) -> String {
        var result = prompt
        
        // Remove phrases that trigger verbose responses
        let triggers = [
            " in great detail",
            " as thoroughly as possible",
            " with extensive examples",
            " and elaborate on each point",
            " covering all aspects"
        ]
        
        for trigger in triggers {
            result = result.replacingOccurrences(of: trigger, with: "", options: .caseInsensitive)
        }
        
        // Replace verbose keywords
        result = result.replacingOccurrences(of: "elaborate on", with: "explain")
        result = result.replacingOccurrences(of: "expound upon", with: "describe")
        
        return result
    }
    
    private func consolidateQuestions(_ prompt: String) -> String {
        var result = prompt
        
        // Combine multiple similar questions
        // This is a simplified version - production would use NLP
        
        // Remove duplicate question marks
        while result.contains("??") {
            result = result.replacingOccurrences(of: "??", with: "?")
        }
        
        return result
    }
    
    private func optimizeFormatting(_ prompt: String) -> String {
        var result = prompt
        
        // Remove excessive whitespace
        result = result.replacingOccurrences(of: "\\s+", with: " ", options: .regularExpression)
        result = result.trimmingCharacters(in: .whitespacesAndNewlines)
        
        // Remove excessive punctuation
        result = result.replacingOccurrences(of: "!!!", with: "!")
        result = result.replacingOccurrences(of: "!!", with: "!")
        
        return result
    }
    
    // MARK: - Estimation Functions
    
    private func estimateLatencyReduction(original: String, optimized: String) -> Double {
        // Estimate based on:
        // 1. Prompt length reduction
        // 2. Removal of verbose keywords
        // 3. Simplified instructions
        
        let lengthReduction = Double(original.count - optimized.count) / Double(original.count)
        let verboseKeywordCount = verboseKeywords.filter { original.lowercased().contains($0) }.count
        let inefficientPhraseCount = inefficientPhrases.filter { original.lowercased().contains($0) }.count
        
        // Rough estimation formula
        var reduction = lengthReduction * 20.0 // 20% max from length
        reduction += Double(verboseKeywordCount) * 5.0 // 5% per verbose keyword
        reduction += Double(inefficientPhraseCount) * 3.0 // 3% per inefficient phrase
        
        return min(reduction, 50.0) // Cap at 50%
    }
    
    private func estimateEnergyReduction(original: String, optimized: String) -> Double {
        // Energy reduction typically correlates with latency reduction
        // But can be slightly different due to computational complexity
        
        let latencyReduction = estimateLatencyReduction(original: original, optimized: optimized)
        
        // Energy reduction is typically 70-90% of latency reduction
        return latencyReduction * 0.8
    }
    
    private func assessQualityImpact(original: String, optimized: String) -> String {
        let changeMagnitude = Double(abs(original.count - optimized.count)) / Double(original.count)
        
        if changeMagnitude < 0.1 {
            return "maintained"
        } else if changeMagnitude < 0.3 {
            // Small changes - quality maintained if we removed fluff
            let hasVerboseTriggers = verboseKeywords.contains { original.lowercased().contains($0) }
            return hasVerboseTriggers ? "improved" : "maintained"
        } else {
            return "slightly reduced"
        }
    }
    
    // MARK: - Analysis Functions
    
    func analyzePrompt(_ prompt: String) -> PromptAnalysis {
        let wordCount = prompt.split(separator: " ").count
        let charCount = prompt.count
        
        let hasVerboseKeywords = verboseKeywords.contains { prompt.lowercased().contains($0) }
        let hasInefficientPhrases = inefficientPhrases.contains { prompt.lowercased().contains($0) }
        
        let complexity = calculateComplexity(prompt)
        let estimatedTokens = wordCount * 13 / 10 // Rough estimate: 1.3 tokens per word
        
        return PromptAnalysis(
            wordCount: wordCount,
            charCount: charCount,
            estimatedTokens: estimatedTokens,
            hasVerboseKeywords: hasVerboseKeywords,
            hasInefficientPhrases: hasInefficientPhrases,
            complexity: complexity,
            optimizationPotential: hasVerboseKeywords || hasInefficientPhrases ? "high" : "low"
        )
    }
    
    private func calculateComplexity(_ prompt: String) -> String {
        let wordCount = prompt.split(separator: " ").count
        let sentenceCount = prompt.components(separatedBy: CharacterSet(charactersIn: ".!?")).filter { !$0.isEmpty }.count
        let avgWordsPerSentence = Double(wordCount) / max(Double(sentenceCount), 1)
        
        if avgWordsPerSentence > 20 {
            return "high"
        } else if avgWordsPerSentence > 10 {
            return "medium"
        } else {
            return "low"
        }
    }
}

// MARK: - Supporting Structures

struct PromptAnalysis {
    let wordCount: Int
    let charCount: Int
    let estimatedTokens: Int
    let hasVerboseKeywords: Bool
    let hasInefficientPhrases: Bool
    let complexity: String
    let optimizationPotential: String
}

struct OptimizationRules {
    // This can be expanded with learned rules from experiments
    let rules: [String: String] = [
        "explain_detailed": "explain",
        "describe_comprehensively": "describe",
        "analyze_thoroughly": "analyze"
    ]
}

