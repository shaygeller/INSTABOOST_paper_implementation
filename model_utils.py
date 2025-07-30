"""
Model Utility Functions for INSTABOOST

This module provides utility functions for initializing models used in the INSTABOOST project.
"""

import os
from dotenv import load_dotenv
from huggingface_hub import login
from typing import Dict, Any, Tuple

# Import the model implementations
from hf_model import HFModel
from transformerlens_instaboost import InstaBoostTransformerLens

def initialize_models(model_params: Dict[str, Any]) -> Tuple[HFModel, InstaBoostTransformerLens, InstaBoostTransformerLens]:
    """
    Initialize all three models.
    
    Args:
        model_params: Dictionary with model parameters including:
            - model_name: The name of the model to load
            - device: The device to load the model on
            - num_middle_layers: Number of middle layers to boost
        
    Returns:
        Tuple of (original_model, all_layers_model, middle_layers_model)
    """
    print(f"Initializing models using model:{model_params['model_name']}, device: {model_params['device']}")
    
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
