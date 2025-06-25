# INSTABOOST System Patterns

## System Architecture

The INSTABOOST implementation follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Configuration  │     │  Model Wrappers │     │  Test Framework │
│  Management     │◄────┤  & Hooks        │────►│  & Evaluation   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         ▲                      ▲                       ▲
         │                      │                       │
         └──────────────────────┼───────────────────────┘
                               │
                      ┌─────────────────┐
                      │  Utility        │
                      │  Functions      │
                      └─────────────────┘
```

### Core Components

1. **Configuration Management**
   - Centralized configuration via `config.yaml`
   - Environment variable overrides
   - Utility functions for loading and accessing configuration

2. **Model Wrappers & Hooks**
   - `OriginalTransformerLens`: Wrapper for the original model without boosting
   - `InstaBoostTransformerLens`: Implementation of the INSTABOOST technique
   - Hook functions for modifying attention patterns during inference

3. **Test Framework & Evaluation**
   - Test cases for evaluating instruction following
   - Comparison framework for different boosting strategies
   - Results logging and analysis

4. **Utility Functions**
   - Common functionality shared across components
   - Device detection and management
   - Random seed handling

## Key Technical Decisions

### 1. TransformerLens as the Base Framework

The implementation uses TransformerLens as the base framework for working with transformer models. This decision was made because:

- TransformerLens provides a clean hook system for modifying model internals
- It offers compatibility with Hugging Face models
- It provides access to attention patterns and other internal model states
- It has a simple and consistent API for model loading and generation

### 2. Hook-Based Attention Modification

INSTABOOST modifies attention patterns using TransformerLens hooks rather than modifying the model architecture:

```python
def instaboost_hook(attn_scores, hook):
    # Modify attention scores for selected heads
    modified_scores = attn_scores.clone()
    for head_idx in heads_to_boost:
        modified_scores[:, head_idx, :, :instruction_len] *= multiplier
    
    # Re-normalize to ensure each row sums to 1
    normalized_scores = torch.nn.functional.normalize(modified_scores, p=1, dim=-1)
    
    return normalized_scores
```

This approach:
- Requires no model parameter updates
- Can be applied at inference time
- Is compatible with various model architectures
- Can be easily enabled or disabled

### 3. Selective Boosting Strategies

The implementation supports different boosting strategies:

1. **All Layers Boosting**: Boost attention in all transformer layers
2. **Middle Layers Boosting**: Boost attention only in specific middle layers
3. **Random Head Selection**: Randomly select a percentage of attention heads to boost in each layer

This flexibility allows for experimentation with different boosting approaches and optimization for specific models and tasks.

### 4. Configuration-Driven Approach

All parameters are configurable through `config.yaml` or environment variables:

```yaml
# Random seed settings
random_seed: 42  # Set to null for random behavior

# INSTABOOST parameters
instaboost:
  multiplier: 10.0
  boost_middle_layers_only: true
  num_middle_layers: 5
  start_layer: 8
  head_boost_percentage: 0.2
```

This approach:
- Eliminates hard-coded values
- Allows for easy experimentation with different parameters
- Supports reproducibility through seed control
- Enables configuration through environment variables in different environments

## Design Patterns

### 1. Wrapper Pattern

The implementation uses the Wrapper pattern to encapsulate the original model and add INSTABOOST functionality:

```python
class InstaBoostTransformerLens:
    def __init__(self, model_name, ...):
        self.model = HookedTransformer.from_pretrained(model_name, ...)
        self.tokenizer = self.model.tokenizer
        # Additional INSTABOOST configuration
```

This pattern:
- Maintains the original model's interface
- Adds new functionality without modifying the original code
- Allows for easy comparison between original and modified behavior

### 2. Hook Pattern

The implementation uses the Hook pattern (provided by TransformerLens) to modify model behavior during inference:

```python
with self.model.hooks(instaboost_hooks):
    output = self.model.generate(...)
```

This pattern:
- Allows for temporary modification of model behavior
- Provides access to internal model states
- Enables clean separation between the model and the modification logic

### 3. Strategy Pattern

The implementation uses the Strategy pattern for different boosting strategies:

```python
if boost_middle_layers_only:
    self.layers_to_boost = self._get_specific_layer_indices()
else:
    self.layers_to_boost = list(range(self.model.cfg.n_layers))
```

This pattern:
- Allows for different boosting strategies to be selected at runtime
- Encapsulates each strategy in its own method
- Makes it easy to add new strategies in the future

### 4. Factory Method Pattern

The implementation uses the Factory Method pattern for model initialization:

```python
def initialize_models(model_params):
    original_model = OriginalTransformerLens(...)
    all_layers_model = InstaBoostTransformerLens(..., boost_middle_layers_only=False)
    middle_layers_model = InstaBoostTransformerLens(..., boost_middle_layers_only=True)
    
    return original_model, all_layers_model, middle_layers_model
```

This pattern:
- Centralizes model creation logic
- Ensures consistent initialization across different model types
- Makes it easy to add new model variants in the future

## Critical Implementation Paths

### 1. Attention Score Modification

The core of INSTABOOST is the modification of attention scores:

```
Input → Tokenization → Forward Pass → Hook Intercepts Attention → 
Modify Scores → Normalize → Continue Forward Pass → Generate Output
```

This path is critical for the functioning of INSTABOOST and is implemented in the `_create_instaboost_hook` method.

### 2. Layer and Head Selection

The selection of which layers and heads to boost is another critical path:

```
Configuration → Determine Layers to Boost → 
Select Random Heads for Each Layer → Create Hooks for Selected Layers
```

This path is implemented in the `_get_specific_layer_indices` and `_select_random_heads` methods.

### 3. Test Case Evaluation

The evaluation of test cases is a critical path for assessing INSTABOOST's effectiveness:

```
Test Case → Generate with Original Model → Generate with All Layers INSTABOOST → 
Generate with Middle Layers INSTABOOST → Compare Outputs → Log Results
```

This path is implemented in the `run_test_case` and `compare_outputs` functions.
