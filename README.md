# INSTABOOST

Implementation of the paper: "Instruction Following by Boosting Attention of Large Language Models" by Vitoria Guardieiro, Adam Stein, Avishree Khare, Eric Wong (2025).

## Overview

INSTABOOST is a technique that improves instruction following in large language models by selectively boosting attention to instruction tokens during inference. This implementation:

- Modifies attention patterns during inference without requiring model retraining
- Supports different boosting strategies (all layers or middle layers only)
- Works with models supported by TransformerLens and Hugging Face
- Provides a testing framework to compare different boosting strategies

## Installation

```bash
# Clone the repository
git clone https://github.com/shaygeller/INSTABOOST_paper_implementation.git
cd INSTABOOST_paper_implementation

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install torch numpy transformer_lens python-dotenv pyyaml huggingface_hub
```

For accessing gated models like Llama, create a `.env` file with your Hugging Face token:
```
HUGGINGFACE_TOKEN=your_token_here
```

## Usage

### Configuration

Edit `config.yaml` to customize parameters:

```yaml
# Random seed settings
random_seed: 42  # Set to null for random behavior

# INSTABOOST parameters
instaboost:
  multiplier: 10.0  # Attention multiplier
  boost_middle_layers_only: true
  num_middle_layers: 5
  start_layer: 8
  head_boost_percentage: 0.2
```

### Running the Model

#### Option 1: Direct Usage

```python
from transformerlens_instaboost import InstaBoostTransformerLens

# Initialize the model
model = InstaBoostTransformerLens(
    model_name="meta-llama/Llama-3.2-1B-Instruct",
    boost_middle_layers_only=True,
    num_middle_layers=5
)

# Generate text with INSTABOOST
output = model.generate(
    instruction="You are a helpful assistant.",
    query="What is the capital of France?",
    multiplier=10.0
)
print(output)
```

#### Option 2: Running Tests

```bash
# Run all test cases
python run_instaboost_tests.py
```

This will:
1. Run test cases defined in `tests/instaboost_test_cases.py`
2. Compare outputs from the original model and INSTABOOST variants
3. Save results to a CSV file in the `results` directory

## Project Structure

- `transformerlens_instaboost.py`: Main implementation of INSTABOOST
- `transformerlens_original.py`: Original model implementation for comparison
- `run_instaboost_tests.py`: Script to run tests and compare results
- `utils.py`: Utility functions for configuration and device management
- `config.yaml`: Configuration file for model and INSTABOOST parameters
- `tests/instaboost_test_cases.py`: Test cases for evaluating INSTABOOST

## Citation

```
@misc{guardieiro2025instruction,
      title={Instruction Following by Boosting Attention of Large Language Models}, 
      author={Vitoria Guardieiro and Adam Stein and Avishree Khare and Eric Wong},
      year={2025},
      eprint={2506.13734},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

arXiv:2506.13734 [cs.CL] - https://doi.org/10.48550/arXiv.2506.13734
