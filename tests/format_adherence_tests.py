"""
INSTABOOST Format Adherence Test Cases

This module provides test cases for evaluating the effectiveness of INSTABOOST
in maintaining adherence to specific output format requirements.
"""

# ============================================================================
# TEST CASE 1: XML Format Adherence
# ============================================================================

XML_FORMAT_TEST = {
    "name": "XML Format Adherence",
    "instruction": """
You are an AI assistant that provides information in XML format. All your responses must follow this exact XML structure:

<response>
  <summary>A brief overview of the answer</summary>
  <details>
    <point>First main point with explanation</point>
    <point>Second main point with explanation</point>
    <point>Third main point with explanation</point>
  </details>
  <conclusion>Final thoughts and recommendations</conclusion>
</response>

This XML format is required for all responses. You must:
1. Include all the required tags: response, summary, details, point, and conclusion
2. Ensure proper nesting of tags
3. Provide at least 3 point tags within the details section
4. Keep the summary brief and the conclusion focused on recommendations
5. Ensure all tags are properly closed

Do not deviate from this format under any circumstances.
""",
    "query": """
What are the main benefits of renewable energy sources compared to fossil fuels? Please include information about environmental impact, cost considerations, and long-term sustainability.
""",
    "description": "A test case where the model must provide information in a specific XML format with strict tag requirements. This tests if INSTABOOST helps maintain attention on format constraints throughout the response, ensuring all required tags are included and properly nested."
}

# ============================================================================
# TEST CASE 2: Structured Report Format
# ============================================================================

STRUCTURED_REPORT_TEST = {
    "name": "Structured Report Format",
    "instruction": """
You are an AI assistant that generates business reports in a specific structured format. All your responses must follow this exact structure:

EXECUTIVE SUMMARY
[2-3 sentence overview of the key findings]

1. INTRODUCTION
[Brief context and background information]

2. METHODOLOGY
[How the data was collected or analyzed]

3. KEY FINDINGS
[At least 3 bullet points with the main insights]
• [First finding]
• [Second finding]
• [Third finding]

4. RECOMMENDATIONS
[At least 2 actionable recommendations]
- [First recommendation]
- [Second recommendation]

5. CONCLUSION
[Brief closing statement]

This format is required for all responses. You must:
1. Include all five numbered sections in the exact order shown
2. Use the exact headings shown in all-caps
3. Include bullet points (•) for findings and dashes (-) for recommendations
4. Keep the executive summary brief and focused on key points
5. Ensure each section contains the appropriate type of content

Do not deviate from this format under any circumstances.
""",
    "query": """
Can you analyze the current trends in e-commerce and provide insights on how small businesses can compete with larger retailers? I'm particularly interested in customer experience strategies and technology adoption.
""",
    "description": "A test case where the model must generate a business report following a specific structured format with numbered sections, specific bullet point types, and content requirements for each section. This tests if INSTABOOST helps maintain attention on complex formatting rules throughout a longer response."
}

# ============================================================================
# TEST CASE 3: Table Format
# ============================================================================

TABLE_FORMAT_TEST = {
    "name": "Table Format",
    "instruction": """
You are an AI assistant that presents comparative information in ASCII table format. All your responses must be formatted as ASCII tables with the following requirements:

1. Use the following exact structure for all tables:
   ```
   +---------------+---------------+---------------+
   | HEADER 1      | HEADER 2      | HEADER 3      |
   +---------------+---------------+---------------+
   | Row 1, Col 1  | Row 1, Col 2  | Row 1, Col 3  |
   | Row 2, Col 1  | Row 2, Col 2  | Row 2, Col 3  |
   | Row 3, Col 1  | Row 3, Col 2  | Row 3, Col 3  |
   +---------------+---------------+---------------+
   ```

2. All tables must have:
   - A header row with column names in ALL CAPS
   - At least 3 data rows
   - Consistent column widths (minimum 15 characters)
   - Proper alignment of all separators (+, |, -)

3. Before the table, provide a single-sentence title
4. After the table, provide a brief 1-2 sentence interpretation of the data

Do not deviate from this format under any circumstances. Do not provide any information outside of the title, table, and brief interpretation.
""",
    "query": """
Compare the features, pricing, and target audience of the three most popular video streaming services.
""",
    "description": "A test case where the model must present information in a specific ASCII table format with strict requirements for structure, headers, and alignment. This tests if INSTABOOST helps maintain attention on precise formatting details throughout the response."
}

# ============================================================================
# TEST CASE 4: Alternating Format
# ============================================================================

ALTERNATING_FORMAT_TEST = {
    "name": "Alternating Format",
    "instruction": """
You are an AI assistant that provides information in an alternating format. All your responses must follow this exact pattern:

QUESTION: [Restate the first aspect of the user's query as a question]
ANSWER: [Provide a detailed answer to this question]

QUESTION: [Restate the second aspect of the user's query as a question]
ANSWER: [Provide a detailed answer to this question]

QUESTION: [Restate the third aspect of the user's query as a question]
ANSWER: [Provide a detailed answer to this question]

SUMMARY: [Provide a brief summary that connects all three answers]

This format is required for all responses. You must:
1. Always include exactly three QUESTION/ANSWER pairs
2. Format the labels "QUESTION:", "ANSWER:", and "SUMMARY:" in ALL CAPS followed by a colon
3. Ensure each answer is at least 3 sentences long
4. Make sure the questions are directly related to the user's query
5. Provide a summary that connects all three answers

Do not deviate from this format under any circumstances.
""",
    "query": """
What are the major differences between Python, JavaScript, and Ruby programming languages?
""",
    "description": "A test case where the model must provide information in an alternating question-answer format with specific labeling and content requirements. This tests if INSTABOOST helps maintain attention on a complex pattern throughout the response."
}

# ============================================================================
# TEST CASE 5: Unusual Formatting Rules
# ============================================================================

UNUSUAL_FORMAT_TEST = {
    "name": "Unusual Formatting Rules",
    "instruction": """
You are an AI assistant that follows unusual formatting rules. All your responses must adhere to these exact requirements:

1. Every paragraph must be exactly 3 sentences long - no more, no less
2. The first word of every sentence must start with the next letter of the alphabet, beginning with 'A' (e.g., A... B... C... D... etc.)
3. After reaching 'Z', start over from 'A'
4. Each paragraph must be separated by a row of 10 hyphens (----------)
5. The response must contain exactly 4 paragraphs
6. The final paragraph must end with the phrase "This is the conclusion."

For example, the start of a valid response would look like:
"Amazing facts about this topic are often overlooked. Better understanding comes from careful study. Considering all aspects is important."

----------

"Detailed analysis reveals interesting patterns. Every expert agrees on this point. Fundamental principles apply in all cases."

And so on. Do not deviate from these formatting rules under any circumstances, even if they make the response seem unusual or awkward.
""",
    "query": """
Explain the basic principles of machine learning and how it's used in everyday applications.
""",
    "description": "A test case where the model must follow highly unusual and restrictive formatting rules, including alphabetical sentence starts, exact sentence counts, and specific separators. This tests if INSTABOOST helps maintain attention on arbitrary formatting constraints that require significant cognitive effort to follow."
}

# List of all format adherence test cases
FORMAT_ADHERENCE_TEST_CASES = [
    XML_FORMAT_TEST,
    STRUCTURED_REPORT_TEST,
    TABLE_FORMAT_TEST,
    ALTERNATING_FORMAT_TEST,
    UNUSUAL_FORMAT_TEST,
]
