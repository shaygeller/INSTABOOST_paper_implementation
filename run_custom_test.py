"""
INSTABOOST Custom Test Runner

This module provides a customizable test runner that allows running a single test case
of your choice for quick experimentation and verification that the code runs properly.

Usage:
    python run_custom_test.py [--test_case MANUFACTURING_QC_TEST]
    
    Arguments:
    --test_case TEST_CASE_NAME   Test case to run (default: MANUFACTURING_QC_TEST)
    
    Optional arguments:
    --model_name MODEL_NAME      Model name to use (default: from config.yaml)
    --multiplier MULTIPLIER      Attention multiplier for INSTABOOST (default: from config.yaml)
    --temperature TEMPERATURE    Temperature for generation (default: from config.yaml)
    --max_new_tokens MAX_TOKENS  Maximum number of tokens to generate (default: from config.yaml)
    --num_middle_layers LAYERS   Number of middle layers to boost (default: from config.yaml)
"""

import os
import ssl
import csv
import time
import datetime
import argparse
import torch
from dotenv import load_dotenv
from huggingface_hub import login
from typing import Dict, Tuple, List, Any
from utils import load_config, get_device

# Set SSL context for HTTPS connections
ssl._create_default_https_context = ssl._create_unverified_context

# Load configuration
config = load_config()

# Import the model implementations
from hf_model import HFModel
from transformerlens_instaboost import InstaBoostTransformerLens

# Import all test cases
from tests.instaboost_test_cases import (
    MANUFACTURING_QC_TEST,
    ENERGY_ANALYSIS_TEST,
    EDUCATION_CONTENT_TEST,
    FINANCIAL_DATA_TEST,
    HEALTHCARE_DATA_TEST,
    LEGAL_RESEARCH_TEST,
    ECOMMERCE_REVIEW_TEST,
    SQL_INJECTION_TEST,
    PROPER_SQL_QUERY_TEST,
    SECURITY_DUAL_TEST_VIOLATING,
    SECURITY_DUAL_TEST_COMPLIANT,
    ALL_TEST_CASES
)

# Dictionary mapping test case names to test case objects
TEST_CASES = {
    "MANUFACTURING_QC_TEST": MANUFACTURING_QC_TEST,
    "ENERGY_ANALYSIS_TEST": ENERGY_ANALYSIS_TEST,
    "EDUCATION_CONTENT_TEST": EDUCATION_CONTENT_TEST,
    "FINANCIAL_DATA_TEST": FINANCIAL_DATA_TEST,
    "HEALTHCARE_DATA_TEST": HEALTHCARE_DATA_TEST,
    "LEGAL_RESEARCH_TEST": LEGAL_RESEARCH_TEST,
    "ECOMMERCE_REVIEW_TEST": ECOMMERCE_REVIEW_TEST,
    "SQL_INJECTION_TEST": SQL_INJECTION_TEST,
    "PROPER_SQL_QUERY_TEST": PROPER_SQL_QUERY_TEST,
    "SECURITY_DUAL_TEST_VIOLATING": SECURITY_DUAL_TEST_VIOLATING,
    "SECURITY_DUAL_TEST_COMPLIANT": SECURITY_DUAL_TEST_COMPLIANT
}

def compare_outputs(original_text: str, all_layers_text: str, middle_layers_text: str, query: str) -> Dict[str, Any]:
    """
    Compare and display the differences between outputs from different models.
    
    Args:
        original_text: Text generated without INSTABOOST
        all_layers_text: Text generated with INSTABOOST on all layers
        middle_layers_text: Text generated with INSTABOOST on middle layers only
        query: The input query that was used for generation
        
    Returns:
        Dictionary with comparison metrics
    """
    print("\n=== Output Comparison ===")
    print(f"Original output length: {len(original_text)} characters")
    print(f"All layers output length: {len(all_layers_text)} characters")
    print(f"Middle layers output length: {len(middle_layers_text)} characters")
    
    # Display the generated texts
    print("\n=== Original Output (model without INSTABOOST) ===")
    print(original_text)
    
    print("\n=== All Layers Output (INSTABOOST on all layers) ===")
    print(all_layers_text)
    
    print("\n=== Middle Layers Output (INSTABOOST on middle layers only) ===")
    print(middle_layers_text)
    
    # Return comparison metrics
    return {
        "original_length": len(original_text),
        "all_layers_length": len(all_layers_text),
        "middle_layers_length": len(middle_layers_text),
    }

def run_test_case(
    original_model: HFModel,
    all_layers_model: InstaBoostTransformerLens,
    middle_layers_model: InstaBoostTransformerLens,
    test_case: Dict[str, Any],
    model_params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run a single test case with all three models.
    
    Args:
        original_model: The original model without INSTABOOST
        all_layers_model: The model with INSTABOOST on all layers
        middle_layers_model: The model with INSTABOOST on middle layers only
        test_case: The test case dictionary containing the test parameters
        model_params: Dictionary with model parameters
        
    Returns:
        Dictionary with test results and metrics
    """
    print(f"\n=== Running Test Case: {test_case['name']} ===")
    # print instruction and query
    print(f"Instruction: {test_case['instruction']}")
    print(f"Query: {test_case['query']}")
    
    # Get parameters from model_params
    multiplier = model_params["multiplier"]
    temperature = model_params["temperature"]
    max_new_tokens = model_params["max_new_tokens"]
    top_p = model_params.get("top_p", 1.0)
    
    # Generate with the original model
    print("Generating with original model...")
    original_output = original_model.generate(
        instruction=test_case["instruction"],
        query=test_case["query"],
        temperature=temperature,
        top_p=top_p,
        do_sample=temperature > 0,
        max_new_tokens=max_new_tokens
    )
    print(original_output)

    
    # Generate with the all layers INSTABOOST model
    print("Generating with INSTABOOST (all layers)...")
    all_layers_output = all_layers_model.generate(
        instruction=test_case["instruction"],
        query=test_case["query"],
        multiplier=multiplier,
        temperature=temperature,
        top_p=top_p,
        do_sample=temperature > 0,
        max_new_tokens=max_new_tokens
    )
    print(all_layers_output)
    
    # Generate with the middle layers INSTABOOST model
    print("Generating with INSTABOOST (middle layers)...")
    middle_layers_output = middle_layers_model.generate(
        instruction=test_case["instruction"],
        query=test_case["query"],
        multiplier=multiplier,
        temperature=temperature,
        top_p=top_p,
        do_sample=temperature > 0,
        max_new_tokens=max_new_tokens
    )
    print(middle_layers_output)
    
    # Compare outputs
    comparison_metrics = compare_outputs(
        original_output, 
        all_layers_output, 
        middle_layers_output, 
        test_case["query"]
    )
    
    # Prepare results
    results = {
        "test_case": test_case["name"],
        "instruction": test_case["instruction"],
        "query": test_case["query"],
        "original_output": original_output,
        "all_layers_output": all_layers_output,
        "middle_layers_output": middle_layers_output,
        **comparison_metrics
    }
    
    return results

def initialize_models(model_params: Dict[str, Any]) -> Tuple[HFModel, InstaBoostTransformerLens, InstaBoostTransformerLens]:
    """
    Initialize all three models.
    
    Args:
        model_params: Dictionary with model parameters
        
    Returns:
        Tuple of (original_model, all_layers_model, middle_layers_model)
    """
    print("Initializing models...")
    
    # Load environment variables for Hugging Face token
    load_dotenv()
    
    # Login to Hugging Face (if needed)
    huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
    if huggingface_token:
        login(token=huggingface_token, add_to_git_credential=False)
    
    # Initialize the original model
    print("Initializing original model...")
    original_model = HFModel(
        model_name=model_params["model_name"],
        device=model_params["device"]
    )
    
    # Initialize the all layers INSTABOOST model
    print("Initializing INSTABOOST model (all layers)...")
    all_layers_model = InstaBoostTransformerLens(
        model_name=model_params["model_name"],
        device=model_params["device"],
        boost_middle_layers_only=False,
        num_middle_layers=model_params["num_middle_layers"]
    )
    
    # Initialize the middle layers INSTABOOST model
    print("Initializing INSTABOOST model (middle layers only)...")
    middle_layers_model = InstaBoostTransformerLens(
        model_name=model_params["model_name"],
        device=model_params["device"],
        boost_middle_layers_only=True,
        num_middle_layers=model_params["num_middle_layers"]
    )
    
    return original_model, all_layers_model, middle_layers_model

def save_results_to_csv(results: Dict[str, Any], filename: str) -> None:
    """
    Save test results to a CSV file.
    
    Args:
        results: Dictionary with test results
        filename: Name of the CSV file to save to
    """
    # Define CSV columns
    columns = [
        "test_case",
        "instruction",
        "query",
        "original_length",
        "all_layers_length",
        "middle_layers_length",
        "original_output",
        "all_layers_output",
        "middle_layers_output",
    ]
    
    # Write to CSV
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerow({k: results.get(k, "") for k in columns})
    
    print(f"Results saved to {filename}")

def generate_results_filename(test_case_name: str):
    """
    Generate a results filename with a counter and timestamp.
    
    Args:
        test_case_name: Name of the test case
        
    Returns:
        str: The generated filename.
    """
    if not os.path.exists("results"):
        os.makedirs("results")

    # Create a sanitized version of the test case name for the filename
    sanitized_name = test_case_name.lower().replace("_test", "")
    
    existing_files = [f for f in os.listdir("results") if f.startswith(f"custom_{sanitized_name}_") and f.endswith(".csv")]
    counters = []
    for f in existing_files:
        try:
            counter = int(f.split("_")[-2])
            counters.append(counter)
        except (IndexError, ValueError):
            continue
    next_counter = max(counters, default=0) + 1
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"results/custom_{sanitized_name}_{next_counter:03d}_{timestamp}.csv"

def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: The parsed arguments
    """
    parser = argparse.ArgumentParser(description="Run a custom INSTABOOST test")
    
    # Add arguments with default values
    parser.add_argument("--test_case", type=str, choices=TEST_CASES.keys(), default="MANUFACTURING_QC_TEST",
                        help="The test case to run (default: MANUFACTURING_QC_TEST)")
    parser.add_argument("--model_name", type=str, default=None,
                        help="Model name to use (default: from config.yaml)")
    parser.add_argument("--multiplier", type=float, default=None,
                        help="Attention multiplier for INSTABOOST (default: from config.yaml)")
    parser.add_argument("--temperature", type=float, default=None,
                        help="Temperature for generation (default: from config.yaml)")
    parser.add_argument("--max_new_tokens", type=int, default=None,
                        help="Maximum number of tokens to generate (default: from config.yaml)")
    parser.add_argument("--num_middle_layers", type=int, default=None,
                        help="Number of middle layers to boost (default: from config.yaml)")
    
    args = parser.parse_args()
    
    # Print which test case is being used
    print(f"Using test case: {args.test_case}")
    
    return args

def run_custom_test(args) -> Dict[str, Any]:
    """
    Run a custom test case with all three models.
    
    Args:
        args: Command line arguments
        
    Returns:
        Dictionary with test results
    """
    # Get parameters from config.yaml or environment variables
    model_config = config.get("model", {})
    instaboost_config = config.get("instaboost", {})
    generation_config = config.get("generation", {})
    
    # Get device from config or auto-detect
    device = get_device()
    
    # Global parameters for the models, with command line overrides
    test_params = {
        "model_name": args.model_name if args.model_name is not None else os.getenv("MODEL_NAME", model_config.get("name", "meta-llama/Llama-3.2-1B-Instruct")),
        "device": device,
        "multiplier": args.multiplier if args.multiplier is not None else float(os.getenv("MULTIPLIER", instaboost_config.get("multiplier", 10.0))),
        "temperature": args.temperature if args.temperature is not None else float(os.getenv("TEMPERATURE", generation_config.get("temperature", 0.0))),
        "top_p": float(os.getenv("TOP_P", generation_config.get("top_p", 1.0))),
        "max_new_tokens": args.max_new_tokens if args.max_new_tokens is not None else int(os.getenv("MAX_NEW_TOKENS", generation_config.get("max_new_tokens", 150))),
        "num_middle_layers": args.num_middle_layers if args.num_middle_layers is not None else int(os.getenv("NUM_MIDDLE_LAYERS", instaboost_config.get("num_middle_layers", 5))),
    }
    print(f"Using parameters: {test_params}")
    
    # Get the test case
    test_case = TEST_CASES[args.test_case]
    
    # Initialize models
    original_model, all_layers_model, middle_layers_model = initialize_models(model_params=test_params)
    
    # Run the test case
    results = run_test_case(
        original_model=original_model,
        all_layers_model=all_layers_model,
        middle_layers_model=middle_layers_model,
        test_case=test_case,
        model_params=test_params
    )
    
    return results

def list_available_test_cases():
    """
    Print a list of available test cases.
    """
    print("\nAvailable test cases:")
    for name, test_case in TEST_CASES.items():
        print(f"  {name}: {test_case['name']}")

if __name__ == "__main__":
    print("Running custom INSTABOOST test for quick experimentation...")
    
    # Show available test cases at the start
    print("\nAvailable test cases:")
    for name, test_case in TEST_CASES.items():
        print(f"  {name}: {test_case['name']}")
    print("\nExample usage: python run_custom_test.py --test_case MANUFACTURING_QC_TEST\n")
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Record start time
    start_time = time.time()
    
    # Run the test
    results = run_custom_test(args)
    
    # Record end time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTest completed in {elapsed_time:.2f} seconds")
    
    # Generate filename with counter and timestamp
    filename = generate_results_filename(args.test_case)
    
    # Save results to CSV
    save_results_to_csv(results, filename)
    
    print("\nCustom INSTABOOST test complete!")
    
    # List available test cases for future reference
    list_available_test_cases()
