"""
Utility Functions for INSTABOOST

This module provides utility functions used across the INSTABOOST project.
"""

import os
import yaml
import torch
import random
import numpy as np
from typing import Dict, Any, Optional

def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.yaml or use default values.
    
    Returns:
        Dictionary containing configuration values
    """
    config_path = os.getenv("CONFIG_PATH", "config.yaml")
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            print(f"Loaded configuration from {config_path}")
            return config
    except Exception as e:
        print(f"Error loading config from {config_path}: {e}")
        print("Using default configuration")
        return {}

def setup_random_seed() -> Optional[int]:
    """
    Set up random seed from configuration or environment variable.
    
    Returns:
        The random seed used, or None if no seed was set
    """
    # Load configuration
    config = load_config()
    
    # Get random seed from config or environment variable
    random_seed = os.getenv("RANDOM_SEED", config.get("random_seed"))
    
    # Convert to integer if it's a string (from env var)
    if isinstance(random_seed, str) and random_seed.isdigit():
        random_seed = int(random_seed)
    
    # Set random seed for reproducibility if specified
    if random_seed is not None:
        print(f"Using random seed: {random_seed}")
        random.seed(random_seed)
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)
        # Set CUDA seed if available
        if torch.cuda.is_available():
            torch.cuda.manual_seed(random_seed)
            torch.cuda.manual_seed_all(random_seed)
    else:
        print("Using random behavior (no seed specified)")
    
    return random_seed

def get_device(device_config: Optional[str] = None) -> str:
    """
    Determine the device to use for computation.
    
    Args:
        device_config: Device configuration string ('auto', 'cuda', 'mps', 'cpu')
                      or None to use config.yaml or auto-detect
    
    Returns:
        Device string ('cuda', 'mps', or 'cpu')
    """
    # Load configuration if device_config is None
    if device_config is None:
        config = load_config()
        model_config = config.get("model", {})
        device_config = os.getenv("DEVICE", model_config.get("device", "auto"))
    
    # Auto-detect device if set to 'auto'
    if device_config == "auto":
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"
    else:
        device = device_config
    
    print(f"Using device: {device}")
    return device
