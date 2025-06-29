# INSTABOOST Test Runners

This directory contains test runners for the INSTABOOST implementation. These test runners allow you to run tests with different configurations and test cases to evaluate the effectiveness of the INSTABOOST technique.

## Available Test Runners

### 1. `run_instaboost_tests.py`

The main test runner that runs all test cases with all three models (original, INSTABOOST on all layers, and INSTABOOST on middle layers only).

**Usage:**
```bash
python run_instaboost_tests.py
```

This will run all test cases defined in `tests/instaboost_test_cases.py` with the parameters defined in the `config.yaml` file or environment variables.

### 2. `run_custom_test.py`

A customizable test runner that allows you to run a single test case of your choice with custom parameters.

**Usage:**
```bash
python run_custom_test.py [--test_case TEST_CASE_NAME] [--model_name MODEL_NAME] [--multiplier MULTIPLIER] [--temperature TEMPERATURE] [--max_new_tokens MAX_TOKENS] [--num_middle_layers LAYERS]
```

**Arguments:**
- `--test_case`: The name of the test case to run (e.g., MANUFACTURING_QC_TEST, SQL_INJECTION_TEST). If not provided, defaults to MANUFACTURING_QC_TEST.

**Optional Arguments:**
- `--model_name`: Model name to use (default: from config.yaml)
- `--multiplier`: Attention multiplier for INSTABOOST (default: from config.yaml)
- `--temperature`: Temperature for generation (default: from config.yaml)
- `--max_new_tokens`: Maximum number of tokens to generate (default: from config.yaml)
- `--num_middle_layers`: Number of middle layers to boost (default: from config.yaml)

**Example:**
```bash
python run_custom_test.py --test_case MANUFACTURING_QC_TEST --multiplier 20.0 --temperature 0.1
```

This will run the MANUFACTURING_QC_TEST test case with a multiplier of 20.0 and a temperature of 0.1, while using the default values from config.yaml for the other parameters.

## Available Test Cases

The following test cases are available for use with the `run_custom_test.py` script:

- `MANUFACTURING_QC_TEST`: Manufacturing - Quality Control Analysis with Simple JSON Extraction (Simple)
- `ENERGY_ANALYSIS_TEST`: Energy - Geoscience Data Analysis with Simple JSON Extraction (Simple)
- `EDUCATION_CONTENT_TEST`: Education - Lesson Plan Creation with Simple JSON Extraction (Simple)
- `FINANCIAL_DATA_TEST`: Finance - Bypassing Confidentiality Guidelines (Hard)
- `HEALTHCARE_DATA_TEST`: Healthcare - Patient Data Extraction with Conflicting Instructions (Hard)
- `LEGAL_RESEARCH_TEST`: Legal - Case Law Research with Conflicting Instructions (Hard)
- `ECOMMERCE_REVIEW_TEST`: E-commerce - Product Review Manipulation (Hard)
- `SQL_INJECTION_TEST`: Database - SQL Injection Attempt (Hard)
- `PROPER_SQL_QUERY_TEST`: Database - Proper SQL Query Request (Simple)
- `SECURITY_DUAL_TEST_VIOLATING`: Security - Information Request (Violating Guidelines)
- `SECURITY_DUAL_TEST_COMPLIANT`: Security - Information Request (Compliant with Guidelines)

You can see a full list of available test cases by running `run_custom_test.py` with any valid test case and looking at the output at the end of the run.

## Test Results

All test runners save their results to CSV files in the `results/` directory. The CSV files contain the following information:

- Test case name
- Instruction and query
- Original output (from the model without INSTABOOST)
- All layers output (from the model with INSTABOOST on all layers)
- Middle layers output (from the model with INSTABOOST on middle layers only)
- Output lengths for each model

The filename includes a counter and timestamp to avoid overwriting previous results.

## Interpreting the Results

The test runners compare the outputs from the three models:

1. **Original Model**: The model without INSTABOOST
2. **All Layers Model**: The model with INSTABOOST applied to all layers
3. **Middle Layers Model**: The model with INSTABOOST applied only to the middle layers

The comparison includes:
- Output lengths for each model
- The full text output from each model

You can use these results to evaluate how well the INSTABOOST technique improves instruction following in different scenarios. For example:

- In hard test cases (e.g., SQL_INJECTION_TEST), the original model might comply with harmful requests, while the INSTABOOST models might correctly refuse.
- In simple test cases (e.g., MANUFACTURING_QC_TEST), all models should perform well, but the INSTABOOST models might show more precise adherence to the instruction format.

## Configuration

All test runners use the configuration from the `config.yaml` file and environment variables. The following parameters can be configured:

- `model.name`: The name of the model to use (default: "meta-llama/Llama-3.2-1B-Instruct")
- `instaboost.multiplier`: The attention multiplier for INSTABOOST (default: 10.0)
- `instaboost.num_middle_layers`: The number of middle layers to boost (default: 5)
- `generation.temperature`: The temperature for generation (default: 0.0)
- `generation.top_p`: The top-p value for generation (default: 1.0)
- `generation.max_new_tokens`: The maximum number of new tokens to generate (default: 150)
- `testing.num_runs`: The number of times to run each test case (default: 1)

These parameters can also be overridden with environment variables:
- `MODEL_NAME`
- `MULTIPLIER`
- `NUM_MIDDLE_LAYERS`
- `TEMPERATURE`
- `TOP_P`
- `MAX_NEW_TOKENS`
- `NUM_RUNS`

## Device Selection

The test runners automatically detect the available device (CUDA, MPS, or CPU) and use it for model inference. You can see the selected device in the output when running the tests.
