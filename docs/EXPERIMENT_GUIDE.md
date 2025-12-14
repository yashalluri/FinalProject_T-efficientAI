# Experiment Guide

This guide walks you through running the experiments for your research project.

## Timeline & Milestones

### Week 1: Setup & Baseline (Current)
- [ ] Complete environment setup
- [ ] Download and test model
- [ ] Run baseline test set
- [ ] Verify data collection pipeline

### Week 2-3: Systematic Measurements
- [ ] Run all prompt categories (QA, sentiment, generation, reasoning)
- [ ] Collect 100+ inferences per category
- [ ] Document any issues or anomalies
- [ ] Perform initial data analysis

### Week 4-5: Keyword & Pattern Analysis
- [ ] Analyze keyword impact
- [ ] Identify high-cost patterns
- [ ] Test specific keyword variations
- [ ] Operator-level profiling (if possible)

### Week 6: Optimization Implementation
- [ ] Implement optimization rules
- [ ] Test optimization engine
- [ ] Compare optimized vs original prompts
- [ ] Measure improvement metrics

### Week 7: Evaluation
- [ ] Run comprehensive evaluation
- [ ] Statistical significance testing
- [ ] Refine optimization approach
- [ ] Collect final results

### Week 8: Documentation
- [ ] Finalize all analysis
- [ ] Create visualizations
- [ ] Write final report
- [ ] Prepare presentation

## Running Experiments

### 1. Baseline Measurements

**Goal**: Establish baseline performance metrics

**Steps**:
```bash
# 1. Load baseline dataset
cd FinalProject
python3 datasets/prepare_datasets.py

# 2. Run on device
# - Open iOS app
# - Tap "Run Baseline Test"
# - Wait for completion (~10 minutes)

# 3. Analyze results
python3 analysis/latency_analysis.py --results-dir results/baseline
```

**Expected Output**:
- 10 inference results
- Average latency: 2-5s per inference
- Average throughput: 5-15 tokens/sec

### 2. Category-Specific Tests

**Goal**: Compare different prompt types

**For each category** (QA, Sentiment, Generation, Reasoning):

```bash
# 1. Load category prompts in app
# 2. Run batch test
# 3. Analyze

python3 analysis/latency_analysis.py --results-dir results/qa
python3 analysis/energy_analysis.py --results-dir results/qa
```

**What to track**:
- Average latency per category
- Energy consumption patterns
- Response length correlation
- Variance within category

### 3. Keyword Impact Studies

**Goal**: Identify high-cost keywords

**Controlled Experiments**:

Create prompt pairs that differ only in target keyword:

```
Control: "Describe photosynthesis"
Test:    "Explain photosynthesis in detail"
```

**Test keywords**:
- explain vs describe vs summarize
- detailed vs comprehensive vs thorough
- "step by step" vs direct question
- "please" and politeness phrases

**Analysis**:
```bash
python3 analysis/keyword_analysis.py --results-dir results/keywords
```

### 4. Optimization Validation

**Goal**: Measure optimization effectiveness

**Protocol**:
1. Select 50 diverse prompts
2. Generate optimized versions
3. Run both original and optimized
4. Compare metrics

**Metrics to compare**:
- Latency reduction %
- Energy reduction %
- Response quality (manual evaluation)
- Statistical significance (t-test)

```bash
python3 profiling/compare_optimizations.py
```

## Data Collection Best Practices

### Device Conditions

**Keep consistent**:
- Battery level: 80-100%
- Thermal state: Keep device cool
- Background apps: Close all
- Display brightness: 50%
- No charging during tests

**Record for each run**:
- Battery level
- Thermal state
- Time of day
- Device temperature (if available)

### Sample Size Guidelines

- **Baseline**: 10 prompts × 3 runs = 30 samples
- **Per category**: 25 prompts × 2 runs = 50 samples
- **Keyword tests**: 10 pairs × 3 runs = 60 samples
- **Optimization validation**: 50 prompts × 2 versions = 100 samples

**Total**: ~300-400 inferences

### Handling Issues

**If app crashes**:
1. Note which prompt caused crash
2. Check device logs
3. Try shorter version
4. Document in issues log

**If results seem anomalous**:
1. Re-run the test
2. Check thermal throttling
3. Verify battery level
4. Compare with baseline

## Analysis Scripts

### Basic Analysis

```bash
# Latency analysis
python3 analysis/latency_analysis.py

# Energy analysis
python3 analysis/energy_analysis.py

# Keyword analysis
python3 analysis/keyword_analysis.py

# View specific result
python3 analysis/view_results.py results/result_12345.json
```

### Statistical Testing

```bash
# Compare two prompt sets
python3 analysis/compare_sets.py \
  --set1 results/original/ \
  --set2 results/optimized/
```

### Generating Reports

```bash
# Generate comprehensive report
python3 analysis/generate_report.py \
  --output final_report.pdf
```

## Jupyter Notebooks

For interactive analysis:

```bash
jupyter notebook analysis/notebooks/
```

Available notebooks:
- `01_exploratory_analysis.ipynb` - Initial data exploration
- `02_keyword_analysis.ipynb` - Keyword impact visualization
- `03_optimization_eval.ipynb` - Optimization effectiveness
- `04_statistical_tests.ipynb` - Hypothesis testing

## Tips for Success

### Measurement Tips

1. **Warmup runs**: First 2-3 inferences may be slower (model caching)
2. **Batch testing**: Run multiple prompts in sequence for efficiency
3. **Cool-down**: Let device cool between batches
4. **Time of day**: Avoid running during device backups or updates

### Analysis Tips

1. **Check distributions**: Look for outliers before averaging
2. **Control for confounds**: Prompt length, response length affect metrics
3. **Multiple comparisons**: Use Bonferroni correction for many tests
4. **Effect sizes**: Report practical significance, not just p-values

### Documentation Tips

1. **Log everything**: Keep detailed notes on each experiment session
2. **Version control**: Track which model version, app version used
3. **Raw data**: Always save raw JSON results
4. **Reproducibility**: Document exact steps to reproduce findings

## Expected Findings

Based on literature and preliminary tests, expect to find:

### Latency
- ✅ Strong correlation with output length (r > 0.7)
- ✅ Moderate correlation with prompt length (r ~ 0.4-0.6)
- ✅ Keywords like "explain", "analyze" increase latency 10-30%
- ✅ Chain-of-thought prompts 20-40% longer latency

### Energy
- ✅ Very strong correlation with latency (r > 0.9)
- ✅ Slightly lower correlation with output length alone
- ✅ Verbose keywords increase energy 15-25%
- ✅ Optimization can save 10-20% energy

### Optimization
- ✅ Removing politeness saves 5-10% latency
- ✅ Removing verbose modifiers saves 10-15% latency
- ✅ Simplifying instructions saves 8-12% latency
- ✅ Combined optimizations: 15-25% total savings

## Troubleshooting Common Issues

### "Model loading failed"
- Check model file exists in `models/` folder
- Verify GGUF format (not GGML or other)
- Ensure enough free space (8GB+)

### "Memory warning"
- Close other apps
- Restart device
- Use smaller model (4-bit quantization)

### "Results not saving"
- Check app permissions
- Verify storage space
- Check file paths in settings

### "Inconsistent results"
- Check thermal throttling
- Verify battery level stable
- Increase sample size
- Check for background processes

## Next Steps After Experiments

1. ✅ Complete all measurements
2. ✅ Run statistical analyses
3. ✅ Validate optimization effectiveness
4. ✅ Write findings section
5. ✅ Create visualizations
6. ✅ Prepare presentation
7. ✅ Document limitations
8. ✅ Propose future work

