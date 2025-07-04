"""
Original Model Implementation Using Hugging Face Transformers

This module provides a wrapper for the original model using Hugging Face's transformers
library directly without TransformerLens. It serves as a baseline for comparison with
the INSTABOOST implementation.
"""

import os
os.environ['CURL_CA_BUNDLE'] = ''
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
    
import torch
from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
from utils import load_config, get_device

# Load environment variables
load_dotenv()

# Load configuration
config = load_config()

class HFModel:
    """
    Hugging Face's transformers library directly.
    This class provides a baseline implementation without any attention boosting.
    """
    
    def __init__(
        self,
        model_name: str = "llama-2-7b",
        model_path: Optional[str] = None,
        device: Optional[str] = None,
    ):
        """
        Initialize the original model instance with a Hugging Face model.
        
        Args:
            model_name: The model name to load from Hugging Face
            model_path: Path to local model files (if None, will try to load from cache)
            device: Device to load the model on ('cuda', 'mps', or 'cpu')
        """
        # Determine device if not specified
        if device is None:
            self.device = get_device()
        else:
            self.device = device
        
        # Load tokenizer and model from local cache if possible
        print(f"Loading model: {model_name}")
        try:
            # Try to load from local path if provided
            if model_path:
                print(f"Attempting to load from local path: {model_path}")
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path if model_path else model_name,
                    device_map=self.device,
                    torch_dtype=torch.float16 if self.device != "cpu" else torch.float32,
                    trust_remote_code=True
                )
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_path if model_path else model_name,
                    trust_remote_code=True
                )
            else:
                # Try to load from cache
                print(f"Attempting to load from cache")
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    device_map=self.device,
                    torch_dtype=torch.float16 if self.device != "cpu" else torch.float32,
                    trust_remote_code=True
                )
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_name,
                    trust_remote_code=True
                )
            print(f"Successfully loaded model from local files")
        except Exception as e:
            print(f"Error loading model from local files: {e}")
            print("Falling back to downloading from Hugging Face Hub...")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map=self.device,
                torch_dtype=torch.float16 if self.device != "cpu" else torch.float32,
                trust_remote_code=True
            )
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )
            print(f"Successfully loaded model from Hugging Face Hub")
        
        print(f"Successfully loaded model and tokenizer")
    
    def generate(
        self,
        instruction: str,
        query: str,
        max_new_tokens: int = 100,
        temperature: float = 0.0,
        top_p: float = 1.0,
        do_sample: bool = False,
    ) -> str:
        """
        Generate text with the original model.
        
        Args:
            instruction: The instruction prompt
            query: The query to generate from
            max_new_tokens: Maximum number of new tokens to generate
            temperature: Sampling temperature (0 for deterministic output)
            top_p: Top-p sampling parameter
            do_sample: Whether to use sampling (vs greedy decoding)
            
        Returns:
            The generated text
        """
        # Format the input
        full_prompt = f"{instruction}\n\n{query}"
        
        # Tokenize the input
        input_tokens = self.tokenizer.encode(full_prompt, return_tensors="pt").to(self.device)
        
        # Generate with the model
        with torch.no_grad():
            # Create attention mask (all 1s for input tokens)
            attention_mask = torch.ones_like(input_tokens)
            
            # Set up generation parameters
            generation_config = {
                "max_new_tokens": max_new_tokens,
                "top_p": top_p,
                "pad_token_id": self.tokenizer.eos_token_id,
                "attention_mask": attention_mask
            }
            
            # Add temperature only if sampling is enabled
            if do_sample:
                generation_config["do_sample"] = True
                generation_config["temperature"] = temperature
            
            output = self.model.generate(
                input_tokens,
                **generation_config
            )
        
        # Decode the output
        output_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Extract only the generated part (after the input)
        generated_text = output_text[len(full_prompt):]
        
        return generated_text


if __name__ == "__main__":
    
    # Login to Hugging Face (if needed)
    from huggingface_hub import login
    huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
    if huggingface_token:
        login(token=huggingface_token, add_to_git_credential=False)
    
    # Get model parameters from config
    model_config = config.get("model", {})
    generation_config = config.get("generation", {})
    
    # Get model name from config or environment variable
    model_name = os.getenv("MODEL_NAME", model_config.get("name", "meta-llama/Llama-3.2-1B-Instruct"))
    
    # Get device from config or auto-detect
    device = get_device()
    
    # Get model path from environment variable
    model_path = os.getenv("MODEL_PATH", None)
    
    print("\n=== Configuration ===")
    print(f"Model: {model_name}")
    print(f"Device: {device}")
    print(f"Model path: {model_path}")
    
    # Initialize the original model
    original_model = HFModel(
        model_name=model_name,
        model_path=model_path,
        device=device
    )
    
    # Example generation
    instruction = "You are a helpful, harmless, and honest assistant."
    query = "What is the capital of France?"
    
    # Get generation parameters from config or environment variables
    temperature = float(os.getenv("TEMPERATURE", generation_config.get("temperature", 0.0)))
    max_new_tokens = int(os.getenv("MAX_NEW_TOKENS", generation_config.get("max_new_tokens", 100)))
    top_p = float(os.getenv("TOP_P", generation_config.get("top_p", 1.0)))
    
    print(f"Temperature: {temperature}")
    print(f"Max new tokens: {max_new_tokens}")
    print(f"Top p: {top_p}")
    
    # Generate text
    generated_text = original_model.generate(
        instruction=instruction,
        query=query,
        temperature=temperature,
        top_p=top_p,
        do_sample=temperature > 0,
        max_new_tokens=max_new_tokens
    )
    
    print("\n=== Generated Text ===")
    print(generated_text)
