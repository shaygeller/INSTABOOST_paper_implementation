# INSTABOOST Project Brief

## Project Overview

INSTABOOST is an implementation of the technique described in the paper "Instruction Following by Boosting Attention of Large Language Models" by Vitoria Guardieiro, Adam Stein, Avishree Khare, and Eric Wong (2025). The technique aims to improve instruction following capabilities in large language models by selectively boosting attention to instruction tokens during inference.

## Core Requirements

1. **Implement the INSTABOOST technique** as described in the paper, which involves:
   - Modifying attention patterns during inference to boost attention to instruction tokens
   - Applying a multiplier to attention scores for instruction tokens
   - Implementing the technique in a way that can be applied to various transformer models

2. **Create a comparison framework** to evaluate the effectiveness of INSTABOOST:
   - Compare original model outputs with INSTABOOST-enhanced outputs
   - Test on various instruction following scenarios, especially challenging ones
   - Measure and quantify improvements in instruction following

3. **Support different boosting strategies**:
   - Boost attention in all layers
   - Boost attention in specific middle layers only
   - Allow configuration of which layers and attention heads to boost

4. **Ensure compatibility** with:
   - TransformerLens library
   - Hugging Face models
   - Various hardware configurations (CPU, CUDA, MPS)

5. **Maintain clean, modular code** that:
   - Follows Python best practices
   - Is well-documented
   - Uses configuration files instead of hard-coded values
   - Has a clear separation of concerns

## Project Goals

1. **Primary Goal**: Demonstrate that INSTABOOST can improve instruction following in large language models, especially in challenging scenarios where models might otherwise ignore or misinterpret instructions.

2. **Secondary Goals**:
   - Provide a flexible implementation that can be applied to different models
   - Create a framework for testing and evaluating instruction following capabilities
   - Contribute to the understanding of attention mechanisms in transformer models
   - Explore the impact of boosting attention in different layers and heads

## Success Criteria

1. INSTABOOST successfully improves instruction following in challenging test cases
2. The implementation is compatible with different models and hardware configurations
3. The code is well-organized, documented, and follows best practices
4. The project includes comprehensive test cases and evaluation metrics
5. Configuration is flexible and does not rely on hard-coded values
