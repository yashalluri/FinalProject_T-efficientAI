#!/usr/bin/env python3
"""
Setup Verification Script
Checks that all prerequisites are properly installed
"""

import sys
import subprocess
from pathlib import Path
import importlib


def check_python_version():
    """Verify Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python 3.9+ required (found {version.major}.{version.minor})")
        return False


def check_python_packages():
    """Verify required Python packages"""
    print("\n📦 Checking Python packages...")
    
    required_packages = [
        'numpy', 'pandas', 'matplotlib', 'seaborn', 
        'sklearn', 'datasets', 'transformers', 'tqdm'
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n  Install missing packages:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    return True


def check_xcode():
    """Check if Xcode is installed"""
    print("\n🔨 Checking Xcode...")
    try:
        result = subprocess.run(['xcodebuild', '-version'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"  ✅ {version}")
            return True
        else:
            print("  ❌ Xcode not found")
            return False
    except FileNotFoundError:
        print("  ❌ Xcode not installed")
        print("  Install from Mac App Store")
        return False


def check_models():
    """Check if model files exist"""
    print("\n🤖 Checking model files...")
    
    models_dir = Path(__file__).parent.parent / "models"
    
    if not models_dir.exists():
        print(f"  ⚠️  Models directory not found: {models_dir}")
        print("  Creating models directory...")
        models_dir.mkdir(parents=True, exist_ok=True)
    
    # Look for GGUF model files
    model_files = list(models_dir.glob("*.gguf"))
    
    if model_files:
        print(f"  ✅ Found {len(model_files)} model(s):")
        for model in model_files:
            size_mb = model.stat().st_size / (1024 * 1024)
            print(f"     - {model.name} ({size_mb:.1f} MB)")
        return True
    else:
        print("  ⚠️  No model files found")
        print("  Download a model from:")
        print("     https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF")
        print(f"  Place in: {models_dir}")
        return False


def check_datasets():
    """Check dataset structure"""
    print("\n📊 Checking datasets...")
    
    datasets_dir = Path(__file__).parent.parent / "datasets"
    
    categories = ['qa', 'sentiment', 'generation', 'reasoning']
    
    if not datasets_dir.exists():
        print(f"  ⚠️  Datasets directory     not found")
        print(f"  Run: python3 datasets/prepare_datasets.py")
        return False
    
    has_data = False
    for category in categories:
        cat_dir = datasets_dir / category
        if cat_dir.exists():
            json_files = list(cat_dir.glob("*.json"))
            if json_files:
                print(f"  ✅ {category}: {len(json_files)} file(s)")
                has_data = True
            else:
                print(f"  ⚠️  {category}: no data")
        else:
            print(f"  ⚠️  {category}: directory not found")
    
    if not has_data:
        print("\n  Run dataset preparation:")
        print("  python3 datasets/prepare_datasets.py")
        return False
    
    return True


def check_ios_app():
    """Check iOS app structure"""
    print("\n📱 Checking iOS app...")
    
    ios_app_dir = Path(__file__).parent.parent / "ios_app"
    
    if not ios_app_dir.exists():
        print("  ⚠️  iOS app directory not found")
        return False
    
    xcodeproj = list(ios_app_dir.glob("*.xcodeproj"))
    if xcodeproj:
        print(f"  ✅ Found Xcode project: {xcodeproj[0].name}")
    else:
        print("  ⚠️  No Xcode project found")
        print("  iOS app needs to be set up in Xcode")
        return False
    
    # Check for key Swift files
    key_files = [
        "PromptOptimizer/App/PromptOptimizerApp.swift",
        "PromptOptimizer/App/ContentView.swift",
        "PromptOptimizer/LLM/LLMRunner.swift"
    ]
    
    missing_files = []
    for file_path in key_files:
        full_path = ios_app_dir / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ⚠️  {file_path} not found")
            missing_files.append(file_path)
    
    return len(missing_files) == 0


def check_results_directory():
    """Check results directory structure"""
    print("\n📁 Checking results directory...")
    
    results_dir = Path(__file__).parent.parent / "results"
    
    subdirs = ['baseline', 'experiments', 'analysis']
    
    for subdir in subdirs:
        dir_path = results_dir / subdir
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {subdir}/")
    
    return True


def check_device_connection():
    """Check if iOS device is connected"""
    print("\n📱 Checking device connection...")
    
    try:
        result = subprocess.run(['xcrun', 'xctrace', 'list', 'devices'],
                               capture_output=True, text=True, timeout=5)
        
        if 'iPhone' in result.stdout:
            # Extract iPhone info
            lines = [l for l in result.stdout.split('\n') if 'iPhone' in l]
            print("  ✅ iPhone detected:")
            for line in lines[:3]:  # Show up to 3 devices
                print(f"     {line.strip()}")
            return True
        else:
            print("  ⚠️  No iPhone detected")
            print("  Connect iPhone via USB-C and trust computer")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ⚠️  Unable to check device connection")
        return False


def print_summary(results):
    """Print summary of checks"""
    print("\n" + "=" * 60)
    print("SETUP VERIFICATION SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(results.values())
    
    for check, status in results.items():
        emoji = "✅" if status else "❌"
        print(f"{emoji} {check}")
    
    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 Setup complete! Ready to start experiments.")
        print("\nNext steps:")
        print("  1. Open iOS app in Xcode")
        print("  2. Build and deploy to iPhone")
        print("  3. Run baseline test")
    else:
        print("\n⚠️  Some items need attention. See details above.")
        print("\nFix the issues and run this script again:")
        print("  python3 profiling/verify_setup.py")


def main():
    print("=" * 60)
    print("SETUP VERIFICATION")
    print("=" * 60)
    
    results = {
        'Python Version': check_python_version(),
        'Python Packages': check_python_packages(),
        'Xcode': check_xcode(),
        'Model Files': check_models(),
        'Datasets': check_datasets(),
        'iOS App': check_ios_app(),
        'Results Directory': check_results_directory(),
        'Device Connection': check_device_connection()
    }
    
    print_summary(results)


if __name__ == "__main__":
    main()

