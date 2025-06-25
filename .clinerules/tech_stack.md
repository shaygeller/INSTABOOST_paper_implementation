# Tech Stack and Project Standards

## Tech Stack

This project implements the INSTABOOST technique described in the paper "Instruction Following by Boosting Attention of Large Language Models" using the following technologies:

- **Python**: Primary programming language
- **PyTorch**: Deep learning framework for tensor operations and model manipulation
- **TransformerLens**: Library for interpreting and modifying transformer models
- **Hugging Face**: For model loading, tokenization, and hub access

## Dependencies

### Core Dependencies
- `torch`: PyTorch library for deep learning
- `transformer_lens`: Library for interpreting transformer models
- `numpy`: Numerical computing library
- `python-dotenv`: For loading environment variables
- `huggingface_hub`: For accessing Hugging Face models

### Standard Library Dependencies
- `os`, `ssl`: For system and SSL configuration
- `csv`, `time`, `datetime`: For data handling and timing
- `typing`: For type annotations
- `random`: For random number generation

## Project Structure

- `transformerlens_instaboost.py`: Main implementation of the INSTABOOST technique
- `transformerlens_original.py`: Original implementation for comparison
- `run_instaboost_tests.py`: Script to run the tests
- `tests/`: Directory containing test-related files
  - `tests/instaboost_test_cases.py`: Test cases for evaluating the INSTABOOST implementation
  - `tests/__init__.py`: Package initialization file

## Compatibility Rules

1. **PyTorch Version Compatibility**:
   - Maintain compatibility with PyTorch 2.0+
   - Avoid using deprecated PyTorch features

2. **TransformerLens Compatibility**:
   - Use TransformerLens features compatible with the models being tested
   - Avoid modifications that would break TransformerLens hook system

3. **Hugging Face Integration**:
   - Ensure compatibility with Hugging Face Transformers library
   - Follow Hugging Face model loading best practices

4. **Hardware Compatibility**:
   - Code should be able to run on CPU, CUDA (NVIDIA GPUs), and MPS (Apple Silicon)
   - Include device detection and appropriate fallbacks

## Coding Standards

### Python Standards
- Use Python 3.8+ features
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values

### Documentation
- Use Google-style docstrings for all classes and functions
- Include parameter descriptions, return types, and examples where appropriate
- Document complex algorithms with clear explanations

### Code Organization
- Organize code into logical classes and functions
- Use clear, descriptive variable and function names
- Separate model implementation from testing code
- Create modular and reusable components that encapsulate specific functionality, while avoiding over-engineering that might complicate the codebase unnecessarily
- Limit code files to a maximum of 500 lines, with the following exceptions:
  - Test case files in the tests/ directory are exempt from this limit
- Request specific permission before exceeding the 500-line limit, and only when:
  1. The file contains a single logical component that should not be split
  2. Splitting would significantly reduce readability or maintainability
  3. The necessity is clearly documented at the top of the file

### Error Handling
- Use appropriate exception handling
- Provide informative error messages
- Include fallback mechanisms where appropriate

### Security Practices
- Use environment variables for sensitive information (API keys, tokens)
- Follow the security guidelines in security.md
- Never hardcode credentials in source code

### Configuration Management
- Reject hard-coded seeds outside config: seeds must come from config.yaml or env var, not inline numbers
- This allows toggling between determinism and randomization from the CLI
- Aids in distributed parameter sweeps and experiments

### Testing
- Include comprehensive test cases
- Test both normal and edge cases
- Ensure reproducibility by setting random seeds

## Development Workflow

1. **Environment Setup**:
   - Use virtual environments for isolation
   - Install dependencies from requirements (if available)
   - Set up environment variables as needed

2. **Implementation**:
   - Follow the existing code structure and patterns
   - Maintain compatibility with the core libraries
   - Document changes thoroughly

3. **Testing**:
   - Run tests using the existing test framework
   - Compare results with baseline models
   - Ensure reproducibility across runs

4. **Version Control**:
   - Make atomic, focused commits
   - Use descriptive commit messages
   - Create branches for significant changes

## Performance Considerations

- Be mindful of memory usage when working with large models
- Consider computational efficiency, especially for attention manipulation
- Use appropriate batch sizes for the available hardware
- Implement proper cleanup of GPU memory when applicable
