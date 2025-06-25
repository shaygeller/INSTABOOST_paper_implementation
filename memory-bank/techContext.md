# INSTABOOST Technical Context

## Technologies Used

### Core Technologies

1. **Python**: The primary programming language used for the implementation.
   - Version: 3.8+
   - Used for all components of the project

2. **PyTorch**: The deep learning framework used for tensor operations and model manipulation.
   - Version: 2.0+
   - Used for tensor operations, device management, and model manipulation

3. **TransformerLens**: The library used for interpreting and modifying transformer models.
   - Used for accessing and modifying attention patterns
   - Provides the hook system for implementing INSTABOOST
   - Offers compatibility with Hugging Face models

4. **Hugging Face Transformers**: Used for model loading, tokenization, and hub access.
   - Provides access to pre-trained models
   - Handles tokenization and generation

### Supporting Libraries

1. **NumPy**: Used for numerical computing and array operations.
   - Primarily used for random seed setting and array manipulations

2. **YAML**: Used for configuration file parsing.
   - Handles loading and parsing of the `config.yaml` file

3. **Python-dotenv**: Used for loading environment variables.
   - Enables configuration through environment variables
   - Helps with managing sensitive information like API tokens

4. **CSV**: Used for results logging and analysis.
   - Stores test results in a structured format for later analysis

### Development Tools

1. **Git**: Used for version control.
   - Tracks changes to the codebase
   - Facilitates collaboration

2. **VSCode**: Recommended IDE for development.
   - Provides Python language support
   - Offers debugging capabilities
   - Integrates with Git

## Development Setup

### Environment Setup

1. **Python Environment**:
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install torch numpy transformer_lens python-dotenv pyyaml huggingface_hub
   ```

2. **Hugging Face Authentication**:
   - Create a `.env` file with your Hugging Face token:
     ```
     HUGGINGFACE_TOKEN=your_token_here
     ```
   - This is required for accessing gated models like Llama

3. **Configuration**:
   - Create a `config.yaml` file with your desired configuration
   - Alternatively, set environment variables to override configuration values

### Running the Code

1. **Running Tests**:
   ```bash
   python run_instaboost_tests.py
   ```
   - This will run all test cases with the configuration specified in `config.yaml`
   - Results will be saved to a CSV file in the `results` directory

2. **Using INSTABOOST in Your Code**:
   ```python
   from transformerlens_instaboost import InstaBoostTransformerLens
   
   # Initialize the model
   model = InstaBoostTransformerLens(
       model_name="meta-llama/Llama-3.2-1B-Instruct",
       boost_middle_layers_only=True
   )
   
   # Generate text with INSTABOOST
   output = model.generate(
       instruction="You are a helpful assistant.",
       query="What is the capital of France?",
       multiplier=10.0
   )
   ```

## Technical Constraints

### Hardware Constraints

1. **Memory Requirements**:
   - The implementation requires enough memory to load the transformer model
   - For large models (e.g., Llama-3.2-70B), significant GPU memory is needed
   - Smaller models can run on CPU or consumer GPUs

2. **Compute Requirements**:
   - Inference with INSTABOOST has a small overhead compared to regular inference
   - The overhead is primarily in the attention modification step
   - The implementation is optimized to minimize this overhead

3. **Device Compatibility**:
   - The implementation supports CPU, CUDA (NVIDIA GPUs), and MPS (Apple Silicon)
   - Device detection is automatic, but can be overridden through configuration

### Software Constraints

1. **TransformerLens Compatibility**:
   - The implementation relies on TransformerLens's hook system
   - Changes to TransformerLens's API may require updates to the implementation
   - Currently compatible with the latest version of TransformerLens

2. **Model Compatibility**:
   - The implementation is designed to work with transformer models supported by TransformerLens
   - It has been tested with Llama models but should work with other transformer architectures
   - Some model-specific adjustments may be needed for optimal performance

3. **Python Version Compatibility**:
   - The implementation requires Python 3.8 or higher
   - It uses type hints and other features not available in earlier versions

### Performance Considerations

1. **Inference Speed**:
   - INSTABOOST adds a small overhead to inference time
   - The overhead is proportional to the number of layers and heads being boosted
   - Boosting only middle layers can reduce this overhead

2. **Memory Usage**:
   - The implementation creates a copy of attention scores for modification
   - This increases memory usage slightly during inference
   - The increase is temporary and only during the forward pass

3. **Scaling Considerations**:
   - The implementation scales with the size of the model
   - For very large models, memory constraints may become significant
   - Selective boosting (middle layers only) can help mitigate these constraints

## Tool Usage Patterns

### Configuration Management

```python
# Load configuration from config.yaml
config = load_config()

# Get a value with environment variable override and default
value = os.getenv("ENV_VAR_NAME", config.get("section", {}).get("key", default_value))
```

### Device Management

```python
# Get device from config or auto-detect
device = get_device()

# Use device in model initialization
model = HookedTransformer.from_pretrained(model_name, device=device)
```

### Random Seed Management

```python
# Set up random seed from config or environment variable
random_seed = setup_random_seed()

# Use random seed in layer selection
if random_seed is not None:
    layer_seed = random_seed + layer_idx
    random.seed(layer_seed)
```

### Hook Creation and Usage

```python
# Create a hook function
def instaboost_hook(attn_scores, hook):
    # Modify attention scores
    return modified_scores

# Create hooks for multiple layers
hooks = [(f"blocks.{layer_idx}.attn.hook_pattern", instaboost_hook) for layer_idx in layers_to_boost]

# Use hooks during generation
with model.hooks(hooks):
    output = model.generate(input_tokens)
```

### Test Case Execution

```python
# Run a test case with multiple models
results = run_test_case(
    original_model=original_model,
    all_layers_model=all_layers_model,
    middle_layers_model=middle_layers_model,
    test_case=test_case,
    run_index=run_idx,
    model_params=model_params
)

# Save results to CSV
save_results_to_csv(all_results, filename)
