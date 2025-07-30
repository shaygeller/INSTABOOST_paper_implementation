"""
INSTABOOST Tokens Per Second Test Runner

This script measures the tokens per second (TPS) performance of the three model variants:
1. Original model (without INSTABOOST)
2. INSTABOOST with all layers
3. INSTABOOST with middle layers only

Usage:
    python run_tokens_per_second_test.py [--model_name MODEL_NAME]
"""

import os
import ssl
import csv
import time
import datetime
import argparse
import torch
import numpy as np
from dotenv import load_dotenv
from huggingface_hub import login
from typing import Dict, Tuple, List, Any

# Set SSL context for HTTPS connections
ssl._create_default_https_context = ssl._create_unverified_context

# Import the model implementations
from hf_model import HFModel
from transformerlens_instaboost import InstaBoostTransformerLens
from utils import load_config, get_device
from model_utils import initialize_models

# Import test prompts
from tests.tokens_per_second_test import (
    TOKENS_PER_SECOND_TEST_PROMPTS,
    calculate_tokens_per_second,
    estimate_token_count
)

def run_tokens_per_second_test(
    original_model: HFModel,
    all_layers_model: InstaBoostTransformerLens,
    middle_layers_model: InstaBoostTransformerLens,
    test_prompt: Dict[str, Any],
    model_params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run a tokens per second test with all three models.
    
    Args:
        original_model: The original model without INSTABOOST
        all_layers_model: The model with INSTABOOST on all layers
        middle_layers_model: The model with INSTABOOST on middle layers only
        test_prompt: The test prompt dictionary containing the prompt parameters
        model_params: Dictionary with model parameters
        
    Returns:
        Dictionary with test results and metrics
    """
    print(f"\n=== Running TPS Test: {test_prompt['name']} ===")
    print(f"Instruction: {test_prompt['instruction']}")
    print(f"Query: {test_prompt['query']}")
    
    # Get parameters from model_params
    multiplier = model_params["multiplier"]
    temperature = model_params["temperature"]
    max_new_tokens = model_params["max_new_tokens"]
    top_p = model_params.get("top_p", 1.0)
    
    # Generate with the original model
    print("Generating with original model...")
    start_time = time.time()
    original_output = original_model.generate(
        instruction=test_prompt["instruction"],
        query=test_prompt["query"],
        temperature=temperature,
        top_p=top_p,
        do_sample=temperature > 0,
        max_new_tokens=max_new_tokens
    )
    original_time = time.time() - start_time
    original_tokens = estimate_token_count(original_output)
    original_tps = calculate_tokens_per_second(original_tokens, original_time)
    print(f"Original model: {original_tokens} tokens in {original_time:.2f}s = {original_tps:.2f} tokens/sec")
    
    # Generate with the all layers INSTABOOST model
    print("Generating with INSTABOOST (all layers)...")
    start_time = time.time()
    all_layers_output = all_layers_model.generate(
        instruction=test_prompt["instruction"],
        query=test_prompt["query"],
        multiplier=multiplier,
        temperature=temperature,
        top_p=top_p,
        do_sample=temperature > 0,
        max_new_tokens=max_new_tokens
    )
    all_layers_time = time.time() - start_time
    all_layers_tokens = estimate_token_count(all_layers_output)
    all_layers_tps = calculate_tokens_per_second(all_layers_tokens, all_layers_time)
    print(f"All layers model: {all_layers_tokens} tokens in {all_layers_time:.2f}s = {all_layers_tps:.2f} tokens/sec")
    
    # Generate with the middle layers INSTABOOST model
    print("Generating with INSTABOOST (middle layers)...")
    start_time = time.time()
    middle_layers_output = middle_layers_model.generate(
        instruction=test_prompt["instruction"],
        query=test_prompt["query"],
        multiplier=multiplier,
        temperature=temperature,
        top_p=top_p,
        do_sample=temperature > 0,
        max_new_tokens=max_new_tokens
    )
    middle_layers_time = time.time() - start_time
    middle_layers_tokens = estimate_token_count(middle_layers_output)
    middle_layers_tps = calculate_tokens_per_second(middle_layers_tokens, middle_layers_time)
    print(f"Middle layers model: {middle_layers_tokens} tokens in {middle_layers_time:.2f}s = {middle_layers_tps:.2f} tokens/sec")
    
    # Calculate performance impact percentages
    original_baseline = 100.0
    all_layers_percentage = (all_layers_tps / original_tps) * 100 if original_tps > 0 else 0
    middle_layers_percentage = (middle_layers_tps / original_tps) * 100 if original_tps > 0 else 0
    
    print("\n=== Performance Impact ===")
    print(f"Original model: {original_baseline:.2f}% (baseline)")
    print(f"All layers model: {all_layers_percentage:.2f}% of baseline speed")
    print(f"Middle layers model: {middle_layers_percentage:.2f}% of baseline speed")
    
    # Prepare results
    results = {
        "test_name": test_prompt["name"],
        "instruction": test_prompt["instruction"],
        "query": test_prompt["query"],
        "original_tokens": original_tokens,
        "original_time": original_time,
        "original_tps": original_tps,
        "all_layers_tokens": all_layers_tokens,
        "all_layers_time": all_layers_time,
        "all_layers_tps": all_layers_tps,
        "middle_layers_tokens": middle_layers_tokens,
        "middle_layers_time": middle_layers_time,
        "middle_layers_tps": middle_layers_tps,
        "all_layers_percentage": all_layers_percentage,
        "middle_layers_percentage": middle_layers_percentage
    }
    
    return results


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: The parsed arguments
    """
    parser = argparse.ArgumentParser(description="Run INSTABOOST tokens per second test")
    
    # Add arguments with default values
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
    return args

def run_tokens_per_second_tests(args) -> List[Dict[str, Any]]:
    """
    Run tokens per second tests with all three models.
    
    Args:
        args: Command line arguments
        
    Returns:
        List of dictionaries with test results
    """
    # Load configuration
    config = load_config()
    
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
    
    # Initialize models
    original_model, all_layers_model, middle_layers_model = initialize_models(model_params=test_params)
    
    # Run the test prompts
    results = []
    for test_prompt in TOKENS_PER_SECOND_TEST_PROMPTS:
        result = run_tokens_per_second_test(
            original_model=original_model,
            all_layers_model=all_layers_model,
            middle_layers_model=middle_layers_model,
            test_prompt=test_prompt,
            model_params=test_params
        )
        results.append(result)
    
    return results

def calculate_average_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate average results across all test prompts.
    
    Args:
        results: List of dictionaries with test results
        
    Returns:
        Dictionary with average results
    """
    if not results:
        return {}
    
    # Initialize sums
    sum_original_tps = 0
    sum_all_layers_tps = 0
    sum_middle_layers_tps = 0
    sum_all_layers_percentage = 0
    sum_middle_layers_percentage = 0
    
    # Calculate sums
    for result in results:
        sum_original_tps += result["original_tps"]
        sum_all_layers_tps += result["all_layers_tps"]
        sum_middle_layers_tps += result["middle_layers_tps"]
        sum_all_layers_percentage += result["all_layers_percentage"]
        sum_middle_layers_percentage += result["middle_layers_percentage"]
    
    # Calculate averages
    count = len(results)
    avg_original_tps = sum_original_tps / count
    avg_all_layers_tps = sum_all_layers_tps / count
    avg_middle_layers_tps = sum_middle_layers_tps / count
    avg_all_layers_percentage = sum_all_layers_percentage / count
    avg_middle_layers_percentage = sum_middle_layers_percentage / count
    
    # Create average results dictionary
    avg_results = {
        "test_name": "AVERAGE",
        "original_tps": avg_original_tps,
        "all_layers_tps": avg_all_layers_tps,
        "middle_layers_tps": avg_middle_layers_tps,
        "all_layers_percentage": avg_all_layers_percentage,
        "middle_layers_percentage": avg_middle_layers_percentage
    }
    
    return avg_results

if __name__ == "__main__":
    print("Running INSTABOOST tokens per second test...")
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Record start time
    start_time = time.time()
    
    # Run the tests
    results = run_tokens_per_second_tests(args)
    
    # Calculate average results
    avg_results = calculate_average_results(results)
    results.append(avg_results)
    
    # Record end time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTests completed in {elapsed_time:.2f} seconds")
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Original model: {avg_results['original_tps']:.2f} tokens/sec (100%)")
    print(f"All layers model: {avg_results['all_layers_tps']:.2f} tokens/sec ({avg_results['all_layers_percentage']:.2f}%)")
    print(f"Middle layers model: {avg_results['middle_layers_tps']:.2f} tokens/sec ({avg_results['middle_layers_percentage']:.2f}%)")
    
    print("\nINSTABOOST tokens per second test complete!")
