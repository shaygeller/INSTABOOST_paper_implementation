"""
INSTABOOST Instruction Precision Test Cases

This module provides test cases for evaluating the effectiveness of INSTABOOST
in maintaining attention on very specific, detailed requirements.
"""

# ============================================================================
# TEST CASE 1: Writing with Precise Constraints
# ============================================================================

WRITING_CONSTRAINTS_TEST = {
    "name": "Writing with Precise Constraints",
    "instruction": """
You are an AI assistant that creates writing samples according to very specific constraints. For this task, you must write a short story that precisely follows these requirements:

1. Word count: The story must be exactly 200-250 words (no more, no less)
2. Structure: The story must have exactly 5 paragraphs
   - Paragraph 1: Introduction (40-50 words)
   - Paragraph 2: Rising action (50-60 words)
   - Paragraph 3: Climax (30-40 words)
   - Paragraph 4: Falling action (50-60 words)
   - Paragraph 5: Resolution (30-40 words)
3. Characters: The story must include exactly 3 characters:
   - A main character named Alex (gender not specified)
   - A supporting character who is elderly
   - A non-human character (animal or object)
4. Setting: The story must take place in exactly two distinct locations
5. Time: The entire story must occur within a 24-hour period
6. Literary devices: The story must include:
   - At least one simile
   - At least one instance of alliteration
   - Exactly one flashback (no more than 2 sentences)
7. Vocabulary: The story must:
   - Not use any word more than 3 times (except articles and prepositions)
   - Include at least 5 words that are 10+ letters long
   - Avoid all adverbs ending in "-ly"

8. Theme: The story must involve a transformation or change
9. Title: The title must be exactly 4 words long

These constraints are mandatory and must be followed precisely.
""",
    "query": """
Write a short story about an unexpected discovery. Make sure to follow all the constraints exactly as specified.
""",
    "description": "A test case where the model must create a short story following extremely precise constraints regarding word count, structure, characters, setting, time, literary devices, vocabulary, theme, and title. This tests if INSTABOOST helps maintain attention on multiple detailed requirements throughout a creative writing task."
}

# ============================================================================
# TEST CASE 2: Code Generation with Specific Requirements
# ============================================================================

CODE_REQUIREMENTS_TEST = {
    "name": "Code Generation with Specific Requirements",
    "instruction": """
You are an AI assistant that generates code according to very specific requirements. For this task, you must write a Python function that precisely follows these specifications:

1. Function name: Must be named 'process_data' (exactly this spelling and case)
2. Parameters: Must accept exactly 3 parameters:
   - 'data' (required): A list of dictionaries
   - 'filter_key' (required): A string
   - 'transform' (optional): A function, with default value None
3. Return value: Must return a dictionary with exactly these keys:
   - 'filtered_items': A list of items that passed the filter
   - 'stats': A dictionary with statistics
   - 'status': A string status message
4. Functionality: The function must:
   - Filter the input data to only include items where filter_key exists and its value is not None
   - If transform is provided, apply it to each filtered item's filter_key value
   - Calculate these exact statistics:
     * 'count': Number of items after filtering
     * 'avg_value': Average numerical value of filter_key (if applicable)
     * 'keys_found': List of all unique keys found across all items
   - Set status to "Success" if any items passed the filter, otherwise "No matching items"
5. Error handling: Must handle these specific cases:
   - If data is not a list: Raise TypeError with message "Data must be a list"
   - If filter_key is not a string: Raise TypeError with message "Filter key must be a string"
   - If transform is provided but is not callable: Raise TypeError with message "Transform must be callable"
6. Code style:
   - Must include a docstring in Google style format
   - Must use list comprehensions for filtering operations
   - Must use type hints for all parameters and return value
   - Must include exactly 2 inline comments explaining non-obvious parts
   - Variable names must use snake_case
7. Performance:
   - Must only iterate through the data list at most twice
   - Must use dictionary comprehension for creating the stats dictionary

These requirements are mandatory and must be followed precisely.
""",
    "query": """
Write a Python function that processes a list of dictionaries according to the specified requirements. Make sure to follow all the constraints exactly as specified.
""",
    "description": "A test case where the model must generate a Python function following extremely precise requirements regarding function name, parameters, return value, functionality, error handling, code style, and performance considerations. This tests if INSTABOOST helps maintain attention on multiple detailed technical requirements throughout a code generation task."
}

# ============================================================================
# TEST CASE 3: Data Analysis with Methodological Constraints
# ============================================================================

DATA_ANALYSIS_TEST = {
    "name": "Data Analysis with Methodological Constraints",
    "instruction": """
You are an AI assistant that performs data analysis according to very specific methodological constraints. For this task, you must analyze a dataset and present your findings following these exact requirements:

1. Analysis structure: Your analysis must include exactly these sections in this order:
   - Data Overview
   - Descriptive Statistics
   - Trend Analysis
   - Comparative Analysis
   - Limitations
   - Conclusions
2. Data Overview section must:
   - Describe exactly 5 key characteristics of the dataset
   - Identify exactly 2 potential data quality issues
   - Include exactly 1 statement about data collection methodology
3. Descriptive Statistics section must:
   - Report exactly 6 statistical measures: mean, median, mode, range, standard deviation, and skewness
   - Present statistics for exactly 3 different variables
   - Include exactly 1 statement about the distribution shape for each variable
4. Trend Analysis section must:
   - Identify exactly 3 trends in the data
   - Quantify each trend with a specific percentage or numerical value
   - Specify the time period for each trend using MM/YYYY format
   - Include exactly 1 statement about seasonality for each trend
5. Comparative Analysis section must:
   - Make exactly 4 comparisons between different segments or categories
   - Use exactly 2 different comparison metrics
   - Include exactly 1 statement about statistical significance for each comparison
   - Present exactly 1 alternative explanation for each observed difference
6. Limitations section must:
   - Identify exactly 3 limitations of the analysis
   - For each limitation, provide exactly 1 specific example of its potential impact
   - Suggest exactly 1 mitigation strategy for each limitation
7. Conclusions section must:
   - Present exactly 3 key findings
   - For each finding, provide exactly 1 business implication
   - Include exactly 2 recommendations for further analysis
   - End with exactly 1 statement about overall confidence in the results

8. Throughout the analysis, you must:
   - Use exactly 2 different data visualization types (describe them textually)
   - Cite exactly 3 statistical methods used
   - Maintain consistent precision of 1 decimal place for all percentages
   - Use exactly 2 industry benchmarks for context

These methodological constraints are mandatory and must be followed precisely.
""",
    "query": """
Analyze the following e-commerce sales dataset and present your findings according to the specified methodological requirements:

The dataset contains 12 months of sales data (Jan 2024 - Dec 2024) for an online retailer selling electronics, clothing, and home goods. It includes information on daily sales, customer demographics, product categories, marketing channels, and customer satisfaction ratings. The data shows seasonal patterns with peaks during holiday periods. There are some missing values in the customer demographic fields and a few outliers in the sales figures. The average order value is $67.50, with electronics having the highest average ($120.30) and clothing the lowest ($42.80). Customer satisfaction averages 4.2/5 overall, with variation across product categories. The conversion rate is 3.2% overall but varies by marketing channel, with email showing 5.7% and social media 2.8%. Repeat customers (30% of the total) spend on average 40% more per order than new customers.
""",
    "description": "A test case where the model must perform a data analysis following extremely precise methodological constraints regarding analysis structure, section content, statistical measures, and reporting format. This tests if INSTABOOST helps maintain attention on multiple detailed analytical requirements throughout a data analysis task."
}

# ============================================================================
# TEST CASE 4: Recipe Creation with Specific Parameters
# ============================================================================

RECIPE_PARAMETERS_TEST = {
    "name": "Recipe Creation with Specific Parameters",
    "instruction": """
You are an AI assistant that creates recipes according to very specific parameters. For this task, you must develop a recipe that precisely follows these requirements:

1. Recipe structure: Your recipe must include exactly these sections in this order:
   - Title
   - Description (30-50 words)
   - Yield (number of servings)
   - Preparation time (in minutes)
   - Cooking time (in minutes)
   - Total time (in minutes)
   - Ingredients list
   - Equipment list
   - Instructions
   - Nutritional information
   - Storage instructions
   - Serving suggestions
2. Title must:
   - Contain exactly 3-5 words
   - Include the main protein or primary ingredient
   - Not include cooking method in the title
3. Ingredients list must:
   - Include exactly 8-12 ingredients total
   - List ingredients in order of use in the recipe
   - Specify exact measurements using metric units (g, ml, etc.)
   - Include exactly 1 herb, 1 spice, and 1 acidic ingredient
   - Include exactly 1 ingredient that can be substituted (with the alternative noted in parentheses)
4. Equipment list must:
   - Include exactly 4-6 items
   - List items in order of use in the recipe
   - Include exactly 1 specialized tool that might not be in every kitchen
5. Instructions must:
   - Contain exactly 6-8 steps
   - Begin each step with an action verb
   - Include exactly 2 precise temperature specifications (in both Celsius and Fahrenheit)
   - Include exactly 3 precise timing indications
   - Include exactly 1 technique tip
   - Include exactly 1 safety precaution
6. Nutritional information must include exact values (per serving) for:
   - Calories
   - Protein (g)
   - Carbohydrates (g)
   - Fat (g)
   - Fiber (g)
   - Sodium (mg)
7. Storage instructions must:
   - Specify exact refrigeration time (in days)
   - Include exactly 1 freezing option with precise freezing time
   - Include exactly 1 reheating instruction
8. Serving suggestions must:
   - Include exactly 2 garnish options
   - Suggest exactly 1 complementary side dish
   - Include exactly 1 beverage pairing

9. Throughout the recipe, you must:
   - Use exactly 2 cooking techniques
   - Ensure the total recipe time (prep + cooking) is between 30-60 minutes
   - Include exactly 1 make-ahead component
   - Ensure the recipe yields exactly 4 servings

These parameters are mandatory and must be followed precisely.
""",
    "query": """
Create a chicken recipe that would be suitable for a weeknight dinner. Make sure to follow all the specified parameters exactly.
""",
    "description": "A test case where the model must create a recipe following extremely precise parameters regarding structure, ingredients, equipment, instructions, nutritional information, and more. This tests if INSTABOOST helps maintain attention on multiple detailed culinary requirements throughout a recipe creation task."
}

# ============================================================================
# TEST CASE 5: Survey Design with Methodological Specifications
# ============================================================================

SURVEY_DESIGN_TEST = {
    "name": "Survey Design with Methodological Specifications",
    "instruction": """
You are an AI assistant that designs surveys according to very specific methodological specifications. For this task, you must create a survey that precisely follows these requirements:

1. Survey structure: Your survey must include exactly these sections in this order:
   - Title
   - Introduction (40-60 words)
   - Screening questions
   - Demographic questions
   - Core questions
   - Follow-up questions
   - Closing statement (20-30 words)
2. Title must:
   - Contain exactly 6-10 words
   - Not include the word "survey" or "questionnaire"
   - Include the primary research topic
3. Introduction must:
   - State the exact purpose of the survey
   - Specify the exact time commitment (8-10 minutes)
   - Include exactly 1 statement about confidentiality
   - Include exactly 1 statement about voluntary participation
4. Screening questions must:
   - Include exactly 2 questions
   - Use exactly 1 yes/no question
   - Use exactly 1 multiple-choice question with 4 options
   - Include skip logic instructions for disqualification
5. Demographic questions must:
   - Include exactly 4 questions covering: age, gender, location, and occupation
   - Use age ranges in 10-year increments
   - Include exactly 5 gender options
   - Use exactly 4 geographic regions
   - Use exactly 6 occupation categories
   - Make all demographic questions optional (explicitly stated)
6. Core questions must:
   - Include exactly 10 questions total
   - Use exactly 3 different question types:
     * 4 Likert scale questions (5-point scale with labels for each point)
     * 4 multiple-choice questions (each with exactly 5 options)
     * 2 open-ended questions (with 50-word response limit noted)
   - Include exactly 2 matrix questions
   - Include exactly 1 conditional question (based on a previous response)
7. Follow-up questions must:
   - Include exactly 3 questions
   - All must be optional (explicitly stated)
   - Include exactly 1 question about willingness for future research
   - Include exactly 1 question requesting feedback on the survey itself
8. Closing statement must:
   - Thank respondents
   - Specify exactly when and how results will be shared
   - Include exactly 1 contact method for questions

9. Throughout the survey, you must:
   - Use exactly 2 attention check questions (disguised within core questions)
   - Include exactly 3 questions with "Select all that apply" format
   - Ensure all rating scales are consistently ordered (negative to positive)
   - Include exactly 1 progress indicator instruction
   - Use neutral, non-leading language throughout

These methodological specifications are mandatory and must be followed precisely.
""",
    "query": """
Design a customer satisfaction survey for a software as a service (SaaS) company that provides project management tools. Make sure to follow all the specified methodological requirements exactly.
""",
    "description": "A test case where the model must design a survey following extremely precise methodological specifications regarding structure, question types, response options, and survey design best practices. This tests if INSTABOOST helps maintain attention on multiple detailed research methodology requirements throughout a survey design task."
}

# List of all instruction precision test cases
INSTRUCTION_PRECISION_TEST_CASES = [
    WRITING_CONSTRAINTS_TEST,
    CODE_REQUIREMENTS_TEST,
    DATA_ANALYSIS_TEST,
    RECIPE_PARAMETERS_TEST,
    SURVEY_DESIGN_TEST,
]
