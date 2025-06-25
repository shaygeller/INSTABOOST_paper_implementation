"""
Original TransformerLens Model Implementation

This module provides a wrapper for the original TransformerLens model without any
attention boosting. It serves as a baseline for comparison with the INSTABOOST
implementation.
"""

import os
os.environ['CURL_CA_BUNDLE'] = ''
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
    
import torch
from typing import Optional
from transformer_lens import HookedTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OriginalTransformerLens:
    """
    Wrapper for the original TransformerLens model without any attention boosting.
    """
    
    def __init__(
        self,
        model_name: str = "llama-2-7b",
        model_path: Optional[str] = None,
        device: Optional[str] = None,
    ):
        """
        Initialize the original model instance with a TransformerLens model.
        
        Args:
            model_name: The model name to load with TransformerLens
            model_path: Path to local model files (if None, will try to load from cache)
            device: Device to load the model on ('cuda', 'mps', or 'cpu')
        """
        # Determine device if not specified
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else \
                         "mps" if torch.backends.mps.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model from local cache if possible
        print(f"Loading model: {model_name}")
        try:
            # Try to load from local path if provided
            if model_path:
                print(f"Attempting to load from local path: {model_path}")
                self.model = HookedTransformer.from_pretrained(
                    model_name,
                    device=self.device,
                    hf_path=model_path
                )
            else:
                # Try to load from cache
                print(f"Attempting to load from cache")
                self.model = HookedTransformer.from_pretrained(
                    model_name,
                    device=self.device,
                    use_cache=True
                )
            print(f"Successfully loaded model from local files")
        except Exception as e:
            print(f"Error loading model from local files: {e}")
            print("Falling back to downloading from Hugging Face Hub...")
            self.model = HookedTransformer.from_pretrained(
                model_name,
                device=self.device
            )
            print(f"Successfully loaded model from Hugging Face Hub")
        
        # Get the tokenizer
        self.tokenizer = self.model.tokenizer
        
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
        output = self.model.generate(
            input_tokens,  # TransformerLens uses positional args, not input_ids
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
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
    
    # Load the Llama model from local files
    model_name = "meta-llama/Llama-3.2-1B-Instruct"
    model_path = "./Llama-3.2-1B-Instruct"
    
    # Initialize the original model
    original_model = OriginalTransformerLens(
        model_name=model_name,
        model_path=model_path,
        device="cpu"  # Use CPU for testing
    )
    
    # Example generation
    instruction = "You are a helpful, harmless, and honest assistant."
    query = "What is the capital of France?"
    
    # Get parameters from environment variables
    temperature = float(os.getenv("TEMPERATURE", 0.1))
    max_new_tokens = int(os.getenv("MAX_NEW_TOKENS", 100))
    
    # Generate text
    generated_text = original_model.generate(
        instruction=instruction,
        query=query,
        temperature=temperature,
        do_sample=temperature > 0,
        max_new_tokens=max_new_tokens
    )
    
    print("\n=== Generated Text ===")
    print(generated_text)
