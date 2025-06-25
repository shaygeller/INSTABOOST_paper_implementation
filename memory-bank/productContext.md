# INSTABOOST Product Context

## Why This Project Exists

Large Language Models (LLMs) have shown remarkable capabilities in generating text, but they sometimes struggle with following instructions precisely, especially when those instructions conflict with their pre-training or when the instructions are complex. The INSTABOOST project exists to address this limitation by implementing a technique that can improve instruction following without requiring model retraining or fine-tuning.

The paper "Instruction Following by Boosting Attention of Large Language Models" introduces a simple yet effective approach to enhance instruction following by modifying attention patterns during inference. This project implements that technique to make it accessible and usable with various models.

## Problems It Solves

1. **Instruction Neglect**: LLMs sometimes ignore or partially follow instructions, especially when those instructions conflict with their pre-training. INSTABOOST helps models pay more attention to the instruction part of the prompt.

2. **Jailbreaking Vulnerability**: Models can be vulnerable to jailbreaking attempts where carefully crafted prompts cause them to ignore safety guidelines. By boosting attention to instruction tokens, INSTABOOST can help models maintain adherence to their safety instructions.

3. **Inconsistent Instruction Following**: Models may follow instructions inconsistently across different contexts or queries. INSTABOOST aims to make instruction following more consistent.

4. **Need for Retraining**: Traditional approaches to improving instruction following often require expensive retraining or fine-tuning. INSTABOOST is an inference-time technique that requires no model parameter updates.

## How It Should Work

INSTABOOST works by modifying the attention patterns in transformer models during inference:

1. **Input Processing**:
   - The input is divided into two parts: the instruction and the query
   - The length of the instruction is determined to identify which tokens to boost

2. **Attention Modification**:
   - During the forward pass, attention scores directed toward instruction tokens are multiplied by a configurable factor (the "boost multiplier")
   - This increases the relative importance of instruction tokens in the attention mechanism
   - The modified attention scores are then normalized to ensure they still sum to 1

3. **Selective Boosting**:
   - Boosting can be applied to all layers or only to specific middle layers
   - A configurable percentage of attention heads in each layer can be selected for boosting
   - This selective approach allows for fine-tuning the boosting strategy for different models and tasks

4. **Comparison Framework**:
   - The implementation includes a testing framework that compares outputs from:
     - The original model without boosting
     - The model with boosting applied to all layers
     - The model with boosting applied only to middle layers
   - This allows for evaluation of the effectiveness of different boosting strategies

## User Experience Goals

1. **Ease of Use**: The implementation should be easy to use with minimal setup, leveraging configuration files for customization.

2. **Flexibility**: Users should be able to apply INSTABOOST to different models and customize the boosting strategy according to their needs.

3. **Transparency**: The implementation should provide clear information about what is being boosted and how, allowing users to understand the impact of the technique.

4. **Compatibility**: The implementation should work with popular libraries like TransformerLens and Hugging Face, and support various hardware configurations.

5. **Reproducibility**: Results should be reproducible, with options for setting random seeds and controlling other factors that might affect generation.

## Target Users

1. **Researchers** studying instruction following, attention mechanisms, or model behavior

2. **Developers** working with language models who need better instruction following without retraining

3. **AI Safety Practitioners** interested in techniques to improve model alignment and reduce vulnerabilities

4. **Educators** teaching about transformer models and attention mechanisms
