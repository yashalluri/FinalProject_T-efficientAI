//
//  PerformanceProfiler.swift
//  PromptOptimizer
//
//  Performance and energy profiling
//

import Foundation
import MetricKit
import UIKit

class PerformanceProfiler: NSObject, ObservableObject {
    
    // Metrics storage
    struct ProfilingMetrics {
        var startTime: Date
        var endTime: Date?
        var firstTokenLatency: Double = 0
        var peakMemoryMB: Double = 0
        var averageMemoryMB: Double = 0
        var estimatedEnergyJ: Double? = nil
        var cpuEnergyJ: Double? = nil
        var gpuEnergyJ: Double? = nil
        var thermalState: String = "unknown"
        var batteryLevelStart: Float = 0
        var batteryLevelEnd: Float = 0
    }
    
    private var currentMetrics: ProfilingMetrics?
    private var memoryReadings: [Double] = []
    private var energyMonitor: EnergyMonitor?
    
    override init() {
        super.init()
        setupMetricKit()
        energyMonitor = EnergyMonitor()
    }
    
    // MARK: - MetricKit Setup
    
    private func setupMetricKit() {
        MXMetricManager.shared.add(self)
    }
    
    // MARK: - Profiling Control
    
    func startProfiling() {
        let startTime = Date()
        
        currentMetrics = ProfilingMetrics(
            startTime: startTime,
            endTime: nil,
            batteryLevelStart: UIDevice.current.batteryLevel
        )
        
        memoryReadings = []
        
        // Start energy monitoring
        energyMonitor?.startMonitoring()
        
        // Start periodic memory sampling
        startMemorySampling()
        
        print("📊 Profiling started at \(startTime)")
    }
    
    func stopProfiling() -> ProfilingMetrics {
        let endTime = Date()
        
        // Stop energy monitoring
        let energyData = energyMonitor?.stopMonitoring()
        
        // Calculate metrics
        guard var metrics = currentMetrics else {
            return ProfilingMetrics(startTime: Date(), endTime: Date())
        }
        
        metrics.endTime = endTime
        metrics.batteryLevelEnd = UIDevice.current.batteryLevel
        metrics.peakMemoryMB = memoryReadings.max() ?? 0
        metrics.averageMemoryMB = memoryReadings.isEmpty ? 0 : memoryReadings.reduce(0, +) / Double(memoryReadings.count)
        metrics.estimatedEnergyJ = energyData?.totalEnergyJ
        metrics.cpuEnergyJ = energyData?.cpuEnergyJ
        metrics.gpuEnergyJ = energyData?.gpuEnergyJ
        metrics.thermalState = getThermalState()
        
        print("📊 Profiling stopped. Duration: \(endTime.timeIntervalSince(metrics.startTime))s")
        
        return metrics
    }
    
    // MARK: - Memory Sampling
    
    private func startMemorySampling() {
        // Sample memory every 100ms during inference
        Task {
            while currentMetrics?.endTime == nil {
                let memoryMB = getMemoryUsageMB()
                memoryReadings.append(memoryMB)
                try? await Task.sleep(nanoseconds: 100_000_000) // 100ms
            }
        }
    }
    
    private func getMemoryUsageMB() -> Double {
        var info = mach_task_basic_info()
        var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size)/4
        
        let kerr: kern_return_t = withUnsafeMutablePointer(to: &info) {
            $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                task_info(mach_task_self_,
                         task_flavor_t(MACH_TASK_BASIC_INFO),
                         $0,
                         &count)
            }
        }
        
        if kerr == KERN_SUCCESS {
            return Double(info.resident_size) / 1024.0 / 1024.0
        }
        return 0
    }
    
    private func getThermalState() -> String {
        switch ProcessInfo.processInfo.thermalState {
        case .nominal: return "nominal"
        case .fair: return "fair"
        case .serious: return "serious"
        case .critical: return "critical"
        @unknown default: return "unknown"
        }
    }
}

// MARK: - MXMetricManagerSubscriber

extension PerformanceProfiler: MXMetricManagerSubscriber {
    func didReceive(_ payloads: [MXMetricPayload]) {
        for payload in payloads {
            // Process CPU metrics
            if let cpuMetrics = payload.cpuMetrics {
                print("📈 CPU Time: \(cpuMetrics.cumulativeCPUTime)")
            }
            
            // Process GPU metrics
            if let gpuMetrics = payload.gpuMetrics {
                print("📈 GPU Time: \(gpuMetrics.cumulativeGPUTime)")
            }
            
            // Process memory metrics
            if let memoryMetrics = payload.memoryMetrics {
                print("📈 Peak Memory: \(memoryMetrics.peakMemoryUsage)")
            }
            
            // Process display metrics
            if let displayMetrics = payload.displayMetrics {
                print("📈 Display APL: \(displayMetrics.averagePixelLuminance)")
            }
        }
    }
}

// MARK: - Energy Monitor

class EnergyMonitor {
    struct EnergyData {
        var totalEnergyJ: Double
        var cpuEnergyJ: Double?
        var gpuEnergyJ: Double?
        var networkEnergyJ: Double?
        var displayEnergyJ: Double?
    }
    
    private var startBatteryLevel: Float = 0
    private var startTime: Date?
    private var cpuUsageStart: Double = 0
    
    func startMonitoring() {
        startTime = Date()
        startBatteryLevel = UIDevice.current.batteryLevel
        cpuUsageStart = getCPUUsage()
        
        // Enable battery monitoring
        UIDevice.current.isBatteryMonitoringEnabled = true
    }
    
    func stopMonitoring() -> EnergyData? {
        guard let startTime = startTime else { return nil }
        
        let endBatteryLevel = UIDevice.current.batteryLevel
        let duration = Date().timeIntervalSince(startTime)
        let cpuUsageEnd = getCPUUsage()
        
        // Estimate energy consumption
        // iPhone 16 Pro Max has ~4,685 mAh battery @ 3.7V ≈ 62.4 Wh ≈ 224,640 J
        let batteryCapacityJ: Double = 224_640
        let batteryDrop = Double(startBatteryLevel - endBatteryLevel)
        let estimatedEnergyJ = batteryDrop * batteryCapacityJ
        
        // Estimate CPU energy (rough approximation)
        // iPhone 16 Pro A18 Pro: ~5W typical, 15W peak
        let avgCPUPower = 5.0 // Watts
        let cpuEnergyJ = avgCPUPower * duration * (cpuUsageEnd - cpuUsageStart) / 100.0
        
        return EnergyData(
            totalEnergyJ: estimatedEnergyJ,
            cpuEnergyJ: cpuEnergyJ,
            gpuEnergyJ: nil, // Would need Metal profiling
            networkEnergyJ: nil,
            displayEnergyJ: nil
        )
    }
    
    private func getCPUUsage() -> Double {
        var totalUsageOfCPU: Double = 0.0
        var threadsList: thread_act_array_t?
        var threadsCount = mach_msg_type_number_t(0)
        
        let threadsResult = withUnsafeMutablePointer(to: &threadsList) {
            return $0.withMemoryRebound(to: thread_act_array_t?.self, capacity: 1) {
                task_threads(mach_task_self_, $0, &threadsCount)
            }
        }
        
        if threadsResult == KERN_SUCCESS, let threadsList = threadsList {
            for index in 0..<threadsCount {
                var threadInfo = thread_basic_info()
                var threadInfoCount = mach_msg_type_number_t(THREAD_INFO_MAX)
                
                let infoResult = withUnsafeMutablePointer(to: &threadInfo) {
                    $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                        thread_info(threadsList[Int(index)], thread_flavor_t(THREAD_BASIC_INFO), $0, &threadInfoCount)
                    }
                }
                
                if infoResult == KERN_SUCCESS {
                    let threadBasicInfo = threadInfo
                    if threadBasicInfo.flags & TH_FLAGS_IDLE == 0 {
                        totalUsageOfCPU += (Double(threadBasicInfo.cpu_usage) / Double(TH_USAGE_SCALE)) * 100.0
                    }
                }
            }
            
            vm_deallocate(mach_task_self_, vm_address_t(UInt(bitPattern: threadsList)), vm_size_t(Int(threadsCount) * MemoryLayout<thread_t>.stride))
        }
        
        return totalUsageOfCPU
    }
}

