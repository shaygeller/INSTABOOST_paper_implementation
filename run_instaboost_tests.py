"""
INSTABOOST Test Runner

This module provides functions for running tests to compare the original model
with the INSTABOOST model (both all layers and middle layers only) on various
instruction following tasks.
"""

import os
import ssl
import csv
import time
import datetime
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
from transformerlens_original import OriginalTransformerLens
from transformerlens_instaboost import InstaBoostTransformerLens

# Import the test cases and parameters
from tests.instaboost_test_cases import FINANCIAL_DATA_TEST, ALL_TEST_CASES

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
    
    # Compare original vs all layers
    # print("\n=== Original vs All Layers ===")
    # if original_text == all_layers_text:
    #     print("Outputs are IDENTICAL. INSTABOOST (all layers) did not change the generation.")
    #     all_layers_diff = 0
    #     all_layers_diff_pct = 0
    # else:
    #     print("Outputs are DIFFERENT. INSTABOOST (all layers) successfully changed the generation.")
    #     all_layers_diff = sum(1 for a, b in zip(original_text, all_layers_text) if a != b)
    #     max_len = max(len(original_text), len(all_layers_text))
    #     all_layers_diff_pct = (all_layers_diff / max_len) * 100 if max_len > 0 else 0
    #     print(f"Character-level difference: {all_layers_diff} characters ({all_layers_diff_pct:.2f}%)")
    
    # # Compare original vs middle layers
    # print("\n=== Original vs Middle Layers ===")
    # if original_text == middle_layers_text:
    #     print("Outputs are IDENTICAL. INSTABOOST (middle layers) did not change the generation.")
    #     middle_layers_diff = 0
    #     middle_layers_diff_pct = 0
    # else:
    #     print("Outputs are DIFFERENT. INSTABOOST (middle layers) successfully changed the generation.")
    #     middle_layers_diff = sum(1 for a, b in zip(original_text, middle_layers_text) if a != b)
    #     max_len = max(len(original_text), len(middle_layers_text))
    #     middle_layers_diff_pct = (middle_layers_diff / max_len) * 100 if max_len > 0 else 0
    #     print(f"Character-level difference: {middle_layers_diff} characters ({middle_layers_diff_pct:.2f}%)")
    
    # # Compare all layers vs middle layers
    # print("\n=== All Layers vs Middle Layers ===")
    # if all_layers_text == middle_layers_text:
    #     print("Outputs are IDENTICAL. Both INSTABOOST variants produced the same output.")
    #     layers_diff = 0
    #     layers_diff_pct = 0
    # else:
    #     print("Outputs are DIFFERENT. The two INSTABOOST variants produced different outputs.")
    #     layers_diff = sum(1 for a, b in zip(all_layers_text, middle_layers_text) if a != b)
    #     max_len = max(len(all_layers_text), len(middle_layers_text))
    #     layers_diff_pct = (layers_diff / max_len) * 100 if max_len > 0 else 0
    #     print(f"Character-level difference: {layers_diff} characters ({layers_diff_pct:.2f}%)")
    
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
    original_model: OriginalTransformerLens,
    all_layers_model: InstaBoostTransformerLens,
    middle_layers_model: InstaBoostTransformerLens,
    test_case: Dict[str, Any],
    run_index: int,
    model_params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run a single test case with all three models.
    
    Args:
        original_model: The original model without INSTABOOST
        all_layers_model: The model with INSTABOOST on all layers
        middle_layers_model: The model with INSTABOOST on middle layers only
        test_case: The test case dictionary containing the test parameters
        run_index: The index of the current run
        
    Returns:
        Dictionary with test results and metrics
    """
    print(f"\n=== Running Test Case: {test_case['name']} (Run {run_index + 1}/{model_params['num_runs']}) ===")
    # print instruction and query
    print(f"Instruction: {test_case['instruction']}")
    print(f"Query: {test_case['query']}")
    
    # Get parameters from MODEL_PARAMS
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
        "run_index": run_index,
        "original_output": original_output,
        "all_layers_output": all_layers_output,
        "middle_layers_output": middle_layers_output,
        **comparison_metrics
    }
    
    return results

def initialize_models(model_params: Dict[str, Any],) -> Tuple[OriginalTransformerLens, InstaBoostTransformerLens, InstaBoostTransformerLens]:
    """
    Initialize all three models.
    
    Args:
        model_name: The name of the model to load
        model_path: The path to the local model files
        device: The device to load the model on
        
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
    original_model = OriginalTransformerLens(
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

def save_results_to_csv(results: List[Dict[str, Any]], filename: str) -> None:
    """
    Save test results to a CSV file.
    
    Args:
        results: List of dictionaries with test results
        filename: Name of the CSV file to save to
    """
    # Define CSV columns
    columns = [
        "test_case",
        "run_index",
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
        for result in results:
            writer.writerow({k: result.get(k, "") for k in columns})
    
    print(f"Results saved to {filename}")

def run_all_tests(model_params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Run all test cases with all three models, multiple times each.
    
    Returns:
        List of dictionaries with test results
    """
    # Initialize models
    original_model, all_layers_model, middle_layers_model = initialize_models(model_params=model_params)
    
    all_results = []
    
    # Run all test cases
    for test_case in ALL_TEST_CASES:
        print(f"\n=== Running Test Case: {test_case['name']} ===")
        
        # Run each test multiple times
        for run_idx in range(model_params["num_runs"]):
            results = run_test_case(
                original_model=original_model,
                all_layers_model=all_layers_model,
                middle_layers_model=middle_layers_model,
                test_case=test_case,
                run_index=run_idx,
                model_params=model_params
            )
            all_results.append(results)
    
    return all_results


def generate_results_filename():
    """
    Generate a results filename with a counter and timestamp.
    Returns:
        str: The generated filename.
    """

    if not os.path.exists("results"):
        os.makedirs("results")

    existing_files = [f for f in os.listdir("results") if f.startswith("instaboost_results_") and f.endswith(".csv")]
    counters = []
    for f in existing_files:
        try:
            counter = int(f.split("_")[2])
            counters.append(counter)
        except (IndexError, ValueError):
            continue
    next_counter = max(counters, default=0) + 1
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"results/instaboost_results_{next_counter:03d}_{timestamp}.csv"



if __name__ == "__main__":

    # Run all tests
    print("Running INSTABOOST tests...")

    # Get parameters from config.yaml or environment variables
    model_config = config.get("model", {})
    instaboost_config = config.get("instaboost", {})
    generation_config = config.get("generation", {})
    testing_config = config.get("testing", {})
    
    # Get device from config or auto-detect
    device = get_device()
    
    # Global parameters for the models
    test_params = {
        "model_name": os.getenv("MODEL_NAME", model_config.get("name", "meta-llama/Llama-3.2-1B-Instruct")),
        "device": device,
        "multiplier": float(os.getenv("MULTIPLIER", instaboost_config.get("multiplier", 10.0))),
        "temperature": float(os.getenv("TEMPERATURE", generation_config.get("temperature", 0.0))),
        "top_p": float(os.getenv("TOP_P", generation_config.get("top_p", 1.0))),
        "max_new_tokens": int(os.getenv("MAX_NEW_TOKENS", generation_config.get("max_new_tokens", 150))),
        "num_middle_layers": int(os.getenv("NUM_MIDDLE_LAYERS", instaboost_config.get("num_middle_layers", 5))),
        "num_runs": int(os.getenv("NUM_RUNS", testing_config.get("num_runs", 1))),
    }
    print(f"Using parameters: {test_params}")
    
    # Record start time
    start_time = time.time()
    
    # Run tests
    results = run_all_tests(test_params)
    
    # Record end time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTests completed in {elapsed_time:.2f} seconds")

    # Generate filename with counter and timestamp
    filename = generate_results_filename()
    # Save results to CSV
    save_results_to_csv(results, filename)
    
    print("\nINSTABOOST testing complete!")
