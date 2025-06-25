"""
INSTABOOST TransformerLens Model Implementation

This module provides a wrapper for the TransformerLens model with INSTABOOST
attention boosting. INSTABOOST works by amplifying the attention given to
instruction prompts within the Transformer layers during inference.
"""

import os
os.environ['CURL_CA_BUNDLE'] = ''
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
    
import torch
import numpy as np
import random
from typing import List, Tuple, Union, Dict, Optional, Set
from transformer_lens import HookedTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)

class InstaBoostTransformerLens:
    """
    INSTABOOST implementation using TransformerLens.
    
    This implementation follows the paper's description of modifying attention scores
    to increase focus on instruction tokens during generation.
    """
    
    def __init__(
        self,
        model_name: str = "llama-2-7b",
        model_path: Optional[str] = None,
        device: Optional[str] = None,
        boost_middle_layers_only: bool = False,
        num_middle_layers: int = 5,
        start_layer: int = 8,  # Start boosting from this layer index
        head_boost_percentage: float = 0.2,  # Percentage of heads to boost in each layer
    ):
        """
        Initialize the INSTABOOST instance with a TransformerLens model.
        
        Args:
            model_name: The model name to load with TransformerLens
            model_path: Path to local model files (if None, will try to load from cache)
            device: Device to load the model on ('cuda', 'mps', or 'cpu')
            boost_middle_layers_only: Whether to boost only specific layers
            num_middle_layers: Number of layers to boost if boost_middle_layers_only is True
            start_layer: The starting layer index for boosting (default: 8)
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
        
        # Store attention weights for analysis
        self.attention_weights = {}
        
        # Set up layer boosting configuration
        self.boost_middle_layers_only = boost_middle_layers_only
        self.num_middle_layers = num_middle_layers
        self.start_layer = start_layer
        self.head_boost_percentage = head_boost_percentage
        
        if boost_middle_layers_only:
            self.layers_to_boost = self._get_specific_layer_indices()
            print(f"Will boost {num_middle_layers} layers starting from layer {start_layer}: {self.layers_to_boost}")
        else:
            self.layers_to_boost = list(range(self.model.cfg.n_layers))
            print(f"Will boost all {len(self.layers_to_boost)} layers")
            
        # Select random heads to boost for each layer
        self.heads_to_boost = self._select_random_heads()
        print(f"Will boost {self.head_boost_percentage*100:.1f}% of attention heads in each layer")
    
    def _get_specific_layer_indices(self) -> List[int]:
        """
        Get the indices of the specific layers to boost, starting from start_layer.
        
        Returns:
            List of layer indices to boost
        """
        total_layers = self.model.cfg.n_layers
        end_idx = min(self.start_layer + self.num_middle_layers, total_layers)
        specific_layers = list(range(self.start_layer, end_idx))
        
        # Print detailed information about the layers being boosted
        print("\n=== INSTABOOST Layer Configuration ===")
        print(f"Total model layers: {total_layers}")
        print(f"Number of layers to boost: {len(specific_layers)}")
        print(f"Starting at layer index: {self.start_layer} (0-indexed)")
        print(f"Ending at layer index: {end_idx-1} (0-indexed)")
        print(f"Percentage of model being boosted: {(len(specific_layers)/total_layers)*100:.1f}%")
        
        # Print a visual representation of which layers are being boosted
        layer_diagram = ["[ ]" for _ in range(total_layers)]
        for idx in specific_layers:
            layer_diagram[idx] = "[X]"
        
        print("\nLayer boosting diagram (X = boosted, empty = not boosted):")
        print("First layer [0] → Last layer [{}]".format(total_layers-1))
        print(" ".join(layer_diagram))
        print("\n")
        
        return specific_layers
        
    def _select_random_heads(self) -> Dict[int, Set[int]]:
        """
        Randomly select a percentage of attention heads to boost in each layer.
        
        Returns:
            Dictionary mapping layer indices to sets of head indices to boost
        """
        heads_to_boost = {}
        
        # Get the number of attention heads in the model
        num_heads = self.model.cfg.n_heads
        
        # Calculate how many heads to boost per layer (self.head_boost_percentage of total heads)
        heads_per_layer = max(1, int(num_heads * self.head_boost_percentage))
        
        # For each layer to boost, randomly select heads
        for layer_idx in self.layers_to_boost:
            # Use a fixed seed based on the layer index to ensure consistency
            # but different heads for different layers
            layer_seed = RANDOM_SEED + layer_idx
            random.seed(layer_seed)
            
            # Randomly select heads_per_layer heads from range(num_heads)
            selected_heads = set(random.sample(range(num_heads), heads_per_layer))
            heads_to_boost[layer_idx] = selected_heads
        
        # Print detailed information about the heads being boosted
        print("\n=== INSTABOOST Head Configuration ===")
        print(f"Total attention heads per layer: {num_heads}")
        print(f"Number of heads to boost per layer: {heads_per_layer} ({self.head_boost_percentage*100:.1f}%)")
        
        # Print a visual representation of which heads are being boosted for each layer
        print("\nHead boosting diagram (X = boosted, empty = not boosted):")
        for layer_idx in sorted(heads_to_boost.keys()):
            head_diagram = ["[ ]" for _ in range(num_heads)]
            for head_idx in heads_to_boost[layer_idx]:
                head_diagram[head_idx] = "[X]"
            print(f"Layer {layer_idx}: " + " ".join(head_diagram))
        print("\n")
        
        return heads_to_boost
    
    def _create_instaboost_hook(self, instruction_len: int, multiplier: float):
        """
        Create a hook function that applies INSTABOOST to attention patterns.
        
        Args:
            instruction_len: Length of the instruction prompt in tokens
            multiplier: The attention multiplier to apply (M in the paper)
            
        Returns:
            Hook function that modifies attention scores
        """
        def instaboost_hook(attn_scores, hook):
            """
            Hook function that boosts attention to instruction tokens.
            
            Args:
                attn_scores: The attention scores tensor
                hook: The hook object
                
            Returns:
                Modified attention scores
            """
            # Store original scores for analysis
            self.attention_weights[hook.name] = attn_scores.detach().clone()
            
            # Extract layer index from hook name (format: "blocks.{layer_idx}.attn.hook_pattern")
            layer_idx = int(hook.name.split('.')[1])
            
            # Get the set of head indices to boost for this layer
            heads_to_boost = self.heads_to_boost.get(layer_idx, set())
            
            # Create a copy of the attention scores to modify
            modified_scores = attn_scores.clone()
            
            # Only boost the selected heads for this layer
            for head_idx in heads_to_boost:
                # Boost attention to instruction tokens for this head only
                # This is the core of INSTABOOST as described in the paper:
                # βij = αij · M if j corresponds to a prompt token (0 ≤ j < K)
                # βij = αij if j corresponds to an input query token (K ≤ j < N)
                modified_scores[:, head_idx, :, :instruction_len] *= multiplier
            
            # Re-normalize to ensure each row sums to 1
            # This is equivalent to the normalization step in the paper:
            # β'ij = βij / Zi where Zi = ∑j βij
            normalized_scores = torch.nn.functional.normalize(modified_scores, p=1, dim=-1)
            
            return normalized_scores
        
        return instaboost_hook
    
    def generate(
        self,
        instruction: str,
        query: str,
        multiplier: float = 5.0,
        max_new_tokens: int = 100,
        temperature: float = 0.0,
        top_p: float = 1.0,
        do_sample: bool = False,
    ) -> str:
        """
        Generate text with INSTABOOST.
        
        Args:
            instruction: The instruction to boost attention to
            query: The query to generate from
            multiplier: The attention multiplier (M in the paper)
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
        
        # Calculate instruction length
        instruction_tokens = self.tokenizer.encode(instruction, return_tensors="pt")
        instruction_len = instruction_tokens.shape[1]
        
        # Print information about the instruction boosting
        print(f"\n=== INSTABOOST Generation Parameters ===")
        print(f"Instruction length: {instruction_len} tokens")
        print(f"Attention multiplier: {multiplier}")
        print(f"Boosting layers: {self.layers_to_boost}")
        print(f"Boosting {self.head_boost_percentage*100:.1f}% of attention heads per layer")
        if self.boost_middle_layers_only:
            print(f"Boosting mode: Specific layers ({len(self.layers_to_boost)} layers starting from layer {self.start_layer})")
        else:
            print(f"Boosting mode: All layers ({len(self.layers_to_boost)} layers)")
        
        # Create INSTABOOST hooks for the specified layers
        instaboost_hooks = []
        for layer_idx in self.layers_to_boost:
            hook_name = f"blocks.{layer_idx}.attn.hook_pattern"
            instaboost_hooks.append((hook_name, self._create_instaboost_hook(instruction_len, multiplier)))
        
        # Generate with INSTABOOST
        with self.model.hooks(instaboost_hooks):
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
    
    # Get parameters from environment variables
    multiplier = 10
    temperature = 0.1
    max_new_tokens = 100
    
    # Initialize the INSTABOOST model
    instaboost_model = InstaBoostTransformerLens(
        model_name=model_name,
        device="cpu",  # Use CPU for testing
        boost_middle_layers_only=True,  # Only boost specific layers
        num_middle_layers=5,  # Boost 5 layers
        start_layer=8  # Start boosting from layer 8
    )
    
    # Example generation
    instruction = "You are a helpful, harmless, and honest assistant."
    query = "What is the capital of France?"
    
    # Generate text with INSTABOOST
    generated_text = instaboost_model.generate(
        instruction=instruction,
        query=query,
        multiplier=multiplier,
        temperature=temperature,
        do_sample=temperature > 0,
        max_new_tokens=max_new_tokens
    )
    
    print("\n=== Generated Text with INSTABOOST ===")
    print(generated_text)
