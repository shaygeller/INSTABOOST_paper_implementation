# INSTABOOST Test Suites

This directory contains various test suites for evaluating the effectiveness of the INSTABOOST technique in improving instruction following capabilities of large language models.

## Overview

The INSTABOOST technique enhances instruction following by boosting attention to the instruction part of the prompt. These test suites are designed to evaluate different aspects of instruction following and measure the improvement provided by INSTABOOST compared to the original model.

## Test Suite Structure

Each test case follows a common structure:
```python
{
    "name": "Test Name",
    "instruction": "System prompt / instruction",
    "query": "User query / input",
    "description": "Description of the test and expected behavior"
}
```

## Test Suites

### 1. Core Test Cases (`instaboost_test_cases.py`)

The main test suite containing a variety of test cases, including:

- **Hard Tasks**: Challenging scenarios where the unboosted model might struggle to follow instructions correctly
- **Simple Tasks**: Basic scenarios that both models should handle correctly
- **Dual Guideline Tests**: Pairs of tests with similar contexts but different compliance with guidelines

These test cases evaluate the model's ability to adhere to guidelines, refuse inappropriate requests, and follow instructions in various domains.

### 2. JSON Extraction Tests (`json_extraction_test_cases.py`)

Tests focused on extracting information into JSON format while adhering to specific guidelines:

- **Positive Cases**: Scenarios where the model should extract permitted information into JSON format
- **Negative Cases**: Scenarios where the model should refuse to extract sensitive or prohibited information

Each test pair evaluates both compliance with guidelines and the ability to perform data extraction and calculations. The JSON structures are intentionally flat (no nesting) for simplicity and include mathematical calculations like averages, totals, and ratios.

Test categories include:
- Personal Data Extraction
- Financial Transaction Analysis
- Medical Research Data
- Security Vulnerability Analysis
- Content Moderation Analysis

### 3. Multi-Choice Extraction Tests (`multi_choice_test_cases.py`)

Tests focused on selecting exactly one option from a list of choices:

- Each test provides a list of options in the instruction and data to classify in the query
- The model must return ONLY the category name without additional text
- Tests the model's ability to follow strict output format instructions

Test categories include:
- Product Category Classification
- Customer Review Sentiment Analysis
- Medical Symptom Urgency Classification
- Programming Language Identification
- Movie Genre Classification

### 4. Instruction Conflict Resolution Tests (`instruction_conflict_tests.py`)

Tests with conflicting instructions between the system prompt and user query:

- System instructions contradict user requests
- Tests if INSTABOOST helps prioritize system instructions over contradictory user requests
- Evaluates the model's ability to maintain adherence to primary guidelines

### 5. Multi-Step Reasoning Tests (`multi_step_reasoning_tests.py`)

Tests requiring specific reasoning steps before providing an answer:

- Mathematical problems with required solution steps
- Logical puzzles with specific reasoning rules
- Tests if INSTABOOST helps maintain attention on the required reasoning process

### 6. Format Adherence Tests (`format_adherence_tests.py`)

Tests with specific output format requirements:

- Generating responses in specific schemas
- Creating outputs with required section headers
- Following unusual formatting rules
- Tests if INSTABOOST helps maintain attention on format constraints

### 7. Context Length Sensitivity Tests (`context_length_tests.py`)

Tests with important instructions in different parts of the prompt:

- Critical instructions at beginning, middle, or end
- Surrounded by less relevant information
- Tests if INSTABOOST helps maintain attention across long contexts

### 8. Instruction Precision Tests (`instruction_precision_tests.py`)

Tests with very specific, detailed requirements:

- Tasks with specific structural constraints
- Requirements with multiple detailed parameters
- Tests if INSTABOOST helps maintain attention on fine details

### 9. Distraction Resistance Tests (`distraction_resistance_tests.py`)

Tests with deliberate distractions or irrelevant information:

- Instructions with tangential information
- Tasks embedded in unrelated scenarios
- Tests if INSTABOOST helps maintain focus on core instructions

### 10. Constraint Adherence Tests (`constraint_adherence_tests.py`)

Tests with specific constraints throughout the response:

- Writing with lexical constraints
- Generating explanations with vocabulary limitations
- Tests if INSTABOOST helps maintain awareness of constraints

### 11. Temporal Consistency Tests (`temporal_consistency_tests.py`)

Tests requiring consistent awareness of time-related instructions:

- Narrating events in specific order
- Maintaining consistent tense
- Tests if INSTABOOST helps maintain temporal context

### 12. Negation Handling Tests (`negation_handling_tests.py`)

Tests with instructions defined by what NOT to do:

- Explaining concepts without specific elements
- Solving problems with approach restrictions
- Tests if INSTABOOST helps maintain attention on negated instructions

### 13. Instruction Hierarchy Tests (`instruction_hierarchy_tests.py`)

Tests with primary and secondary instructions of different importance:

- Critical requirements paired with preferences
- Core tasks paired with enhancements
- Tests if INSTABOOST helps prioritize instructions appropriately

## Running the Tests

The tests are run using the `run_instaboost_tests.py` script in the root directory. This script:

1. Initializes three models:
   - Original model (without INSTABOOST)
   - All layers INSTABOOST model
   - Middle layers INSTABOOST model

2. Runs each test case with all three models

3. Compares the outputs and saves the results to a CSV file

## Interpreting Results

The test results help evaluate:

1. **Instruction Following Improvement**: How much better the INSTABOOST models adhere to instructions compared to the original model

2. **Refusal Appropriateness**: Whether models correctly refuse inappropriate requests

3. **Output Format Adherence**: How well models follow specific output format requirements

4. **Reasoning Process Adherence**: How well models follow specified reasoning processes

5. **Constraint Maintenance**: How well models maintain awareness of constraints throughout responses

These metrics provide a comprehensive evaluation of the INSTABOOST technique's effectiveness in improving instruction following capabilities.
