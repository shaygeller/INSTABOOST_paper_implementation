"""
INSTABOOST Distraction Resistance Test Cases

This module provides test cases for evaluating the effectiveness of INSTABOOST
in maintaining focus on core instructions despite deliberate distractions.
"""

# ============================================================================
# TEST CASE 1: Instructions with Tangential Information
# ============================================================================

TANGENTIAL_INFORMATION_TEST = {
    "name": "Instructions with Tangential Information",
    "instruction": """
You are an AI assistant that summarizes academic articles. Your task is to create a concise summary of the provided article, focusing on the main research question, methodology, findings, and implications.

Did you know that the first academic journals were published in the 17th century? The "Journal des sçavans" (later spelled "Journal des savants"), which first appeared in January 1665, is considered the earliest academic journal published in Europe. It was followed by "Philosophical Transactions of the Royal Society" in March 1665. These early journals primarily contained book reviews and general descriptions of the research being conducted across Europe. The modern peer review process didn't become standardized until the mid-20th century, though some forms of editorial review existed earlier.

YOUR SUMMARY MUST FOLLOW THIS EXACT FORMAT:
1. Title: [Title of the article]
2. Authors: [Authors of the article]
3. Research Question: [1-2 sentences describing the main research question]
4. Methodology: [2-3 sentences describing the research methods]
5. Key Findings: [3-4 bullet points highlighting the main results]
6. Implications: [1-2 sentences on the significance of the findings]
7. Limitations: [1-2 sentences on the limitations of the study]

The history of academic publishing is fascinating. By the 19th century, there were approximately 100 academic journals. Today, there are over 30,000 peer-reviewed journals publishing millions of articles annually. The growth has been exponential, with a particularly sharp increase after World War II when research funding expanded significantly. The digital revolution has further transformed academic publishing, with online journals, preprint servers, and open access models challenging traditional publishing paradigms.

When writing your summary, avoid including your own opinions or evaluations of the research. Focus solely on objectively reporting what is contained in the article. Do not use phrases like "I think" or "In my opinion." The summary should be written in the third person and maintain a formal academic tone throughout.

The economics of academic publishing has been a controversial topic in recent years. Many journals operate on a subscription model, with annual subscriptions for institutions often costing thousands of dollars. Meanwhile, authors typically receive no compensation for their articles and often must pay "article processing charges" to publish, especially in open access journals. This has led to debates about the sustainability and equity of the current academic publishing system.

Remember to keep your summary concise. The entire summary should be no more than 300-400 words. Focus on the most important information and avoid tangential details. Your goal is to provide a clear, accurate, and efficient overview of the article that would help a researcher quickly determine if the full article is relevant to their work.
""",
    "query": """
Please summarize the following research article:

Title: "The Impact of Artificial Intelligence on Labor Markets: Evidence from Online Job Postings"
Authors: Zhang, M., Johnson, K., & Patel, S. (2024)

Abstract: This study examines how the increasing adoption of artificial intelligence (AI) technologies is affecting labor market demands and skill requirements across different industries. Using a dataset of over 200 million online job postings from 2010-2023, we analyze changes in job descriptions, required skills, and compensation offers. Our findings indicate that AI-related skills are increasingly demanded across all sectors, not just in technology. Jobs requiring AI skills command a 14.5% wage premium on average. However, this premium varies significantly by industry and job role. We also find evidence of job polarization, with growth in both high-skilled technical positions and lower-skilled service roles, while middle-skill routine jobs show declining demand. The results suggest that while AI is creating new opportunities, it is also accelerating labor market inequality. Policy implications for education and workforce development are discussed.

Methodology: We collected job posting data from five major online employment platforms between January 2010 and December 2023. Text mining and natural language processing techniques were used to identify AI-related skills and requirements. We employed difference-in-differences and event study approaches to analyze how the introduction of major AI technologies affected job postings in various sectors. Control variables included regional economic indicators, industry growth rates, and seasonal factors.

Results: The demand for AI skills has grown by 35.8% annually since 2018, compared to 5.2% for other technical skills. Industries showing the highest growth in AI skill requirements include healthcare (41.2%), financial services (38.7%), and manufacturing (33.5%). Job roles are increasingly hybridized, with traditional positions incorporating technical requirements. For example, marketing positions mentioning AI skills increased from 2.3% in 2015 to 26.7% in 2023. We estimate that approximately 18.7% of tasks described in 2015 job postings have been automated or significantly transformed by 2023. The wage premium for AI skills is highest in industries with lower overall technology adoption, suggesting a scarcity effect.

Limitations: Our analysis is limited to online job postings, which may not represent the entire labor market, particularly for small businesses or certain sectors. Additionally, job postings reflect employer demands but do not necessarily translate to actual hiring or job creation. Finally, our methodology cannot fully separate the effects of AI from other technological and economic factors influencing labor markets.

Implications: Our findings suggest that education and training systems need significant adaptation to prepare workers for an AI-influenced labor market. The growing wage premium for AI skills indicates potential for increasing inequality if access to AI education remains limited. Policy interventions may be necessary to ensure equitable access to opportunities in the evolving labor market.
""",
    "description": "A test case where the instruction contains substantial tangential information about the history and economics of academic publishing, which is irrelevant to the core task of summarizing the provided article. This tests if INSTABOOST helps maintain focus on the actual instructions (the required summary format) despite these distractions."
}

# ============================================================================
# TEST CASE 2: Task Embedded in Narrative
# ============================================================================

NARRATIVE_EMBEDDED_TEST = {
    "name": "Task Embedded in Narrative",
    "instruction": """
You are an AI assistant that helps with various tasks. Let me tell you a story about my friend Alex who works as a data analyst.

Alex has been working at a tech company for about three years now. The company develops software for healthcare providers, and Alex's job is to analyze user data to improve the product. Last week, Alex was given a challenging project: to create a dashboard that would help hospital administrators track key performance indicators.

YOUR TASK IS TO CREATE A LIST OF 5 ESSENTIAL KPIs FOR A HOSPITAL DASHBOARD. FOR EACH KPI, INCLUDE:
1. The name of the KPI
2. A brief description (1-2 sentences)
3. Why it's important to track
4. How it should be visualized (chart type)

Alex has always been detail-oriented and methodical in approaching problems. In college, Alex majored in statistics with a minor in computer science. The combination has proved valuable in the current role, allowing for both rigorous analysis and efficient coding of data pipelines. Alex's colleagues often come to them for help with particularly tricky data problems or for advice on how to present findings to non-technical stakeholders.

The dashboard project is particularly important because the company is trying to expand its market share in larger hospital systems. Currently, most of their clients are small to medium-sized clinics, but the CEO believes their software could provide even more value to larger institutions with more complex needs. Alex's dashboard could be a key selling point in upcoming pitches to these larger potential clients.

Outside of work, Alex enjoys hiking and has been trying to visit all the national parks in the country. So far, 12 parks have been checked off the list, with Yellowstone being the most recent visit last summer. Alex also volunteers at a local coding bootcamp, teaching introductory data analysis to career-changers. It's a way of giving back, as Alex also transitioned into tech from a previous career in environmental science.

The deadline for the dashboard project is next Friday, which is putting some pressure on Alex. But with careful planning and prioritization, it should be manageable. Alex has already started researching hospital metrics and speaking with the company's healthcare consultants to understand what would be most valuable to include.
""",
    "query": """
I'm working on a similar project to Alex's and could use your help with identifying the most important KPIs for hospital administrators. What would you recommend?
""",
    "description": "A test case where the actual task (creating a list of hospital KPIs) is embedded within a lengthy narrative about a fictional character named Alex. This tests if INSTABOOST helps identify and focus on the actual instructions buried within an irrelevant story."
}

# ============================================================================
# TEST CASE 3: Instructions with Misleading Examples
# ============================================================================

MISLEADING_EXAMPLES_TEST = {
    "name": "Instructions with Misleading Examples",
    "instruction": """
You are an AI assistant that helps create professional email templates. Your task is to write a formal business email based on the provided scenario.

Here's an example of a casual, friendly email that would NOT be appropriate for a formal business context:

Subject: Hey there! Quick question about the project
Hi [Name],
Just wanted to check in about that thing we discussed last week. I was thinking maybe we could grab coffee sometime and chat more about it? Let me know what works for you! BTW, loved that funny cat video you shared on social media yesterday. 😂
Catch you later,
[Your name]

YOUR EMAIL MUST FOLLOW THESE GUIDELINES:
1. Use a clear, specific subject line
2. Begin with a formal salutation (Dear Mr./Ms./Dr. [Last Name])
3. Use professional language throughout (no slang, emoticons, or abbreviations)
4. Clearly state the purpose in the first paragraph
5. Provide necessary details in the second paragraph
6. Include a specific request or next step in the third paragraph
7. End with a formal closing (Sincerely, Regards, etc.)
8. Include a professional signature block

Here's another example of an overly casual message that would NOT meet the professional standards required:

Subject: Update
Hello,
Hope ur doing well! Just wanted to give u a quick update on the project... things are moving along nicely! We're a bit behind schedule but no worries, we'll catch up. 
Let's touch base next week? Maybe Tuesday?
Thx,
J

Remember, your email should be concise but complete, providing all necessary information while respecting the recipient's time. Aim for a tone that is professional, courteous, and clear. Avoid unnecessary jargon or overly complex sentences. The email should be straightforward and easy to understand, with a clear purpose and action item.

Here's a third example of what NOT to do in a professional email:

Subject: URGENT!!! Please respond ASAP!!!
Hello [FIRST NAME],
I'm following up on my previous 5 emails that you haven't responded to!!! This is EXTREMELY important and I need your input RIGHT AWAY. Can't move forward without your approval.
Please get back to me TODAY.
Thanks,
[Name]
Sent from my iPhone

Your email should maintain a professional tone even when communicating urgent matters. Avoid using all caps, multiple exclamation points, or pushy language that might come across as demanding or unprofessional.
""",
    "query": """
Please write a formal business email from a marketing manager to a potential client, following up after an initial meeting and proposing a schedule for the marketing campaign discussed. The email should include specific dates for deliverables and request confirmation of the proposed timeline.
""",
    "description": "A test case where the instruction contains multiple misleading examples of what NOT to do, which could potentially distract from the actual guidelines for creating a professional email. This tests if INSTABOOST helps maintain focus on the actual requirements despite the presence of counterexamples that might confuse the model."
}

# ============================================================================
# TEST CASE 4: Instructions with Irrelevant Technical Details
# ============================================================================

IRRELEVANT_TECHNICAL_TEST = {
    "name": "Instructions with Irrelevant Technical Details",
    "instruction": """
You are an AI assistant that helps create simple HTML webpages. Your task is to write HTML code for a basic webpage based on the provided description.

The HTML5 specification was finalized by the World Wide Web Consortium (W3C) in 2014, though it had been in use for several years prior. The development of HTML5 began in 2004 when the Web Hypertext Application Technology Working Group (WHATWG) started work on the specification. One of the major goals was to improve the language with support for the latest multimedia while keeping it easily readable by humans and consistently understood by computers and devices.

YOUR HTML CODE MUST INCLUDE THE FOLLOWING ELEMENTS:
1. A proper DOCTYPE declaration
2. HTML, head, and body tags
3. A title element in the head section
4. At least one heading (h1-h6) element
5. At least one paragraph (p) element
6. At least one image (img) element with alt text
7. At least one hyperlink (a) element
8. A simple navigation menu using an unordered list (ul/li)
9. Basic CSS styling (either internal or inline)

The HTTP protocol, which is used to transmit webpages, was developed by Tim Berners-Lee at CERN in 1989. HTTP/1.1 became the dominant version in the late 1990s and remained so until HTTP/2 was standardized in 2015. HTTP/2 introduced several performance improvements, including multiplexing, header compression, and server push. More recently, HTTP/3 has been developed, which uses QUIC, a transport layer network protocol designed by Google, instead of TCP.

When writing your HTML code, ensure it is well-structured and properly indented for readability. Use semantic HTML elements where appropriate (such as header, nav, main, section, article, footer) to improve accessibility and SEO. Avoid deprecated elements and attributes that are no longer supported in HTML5.

The CSS box model is a fundamental concept in web design that describes how elements are rendered on a webpage. It consists of content, padding, border, and margin. The standard box model calculates an element's total width as content width + padding + border + margin. However, the alternative box-sizing: border-box makes the width include content, padding, and border, which many developers find more intuitive.

Remember to make your webpage responsive by using appropriate meta tags and CSS media queries. This ensures that the webpage displays properly on different devices and screen sizes. Mobile-friendly design has become increasingly important, especially since Google's mobile-first indexing approach for search rankings.
""",
    "query": """
Please create a simple HTML webpage for a small bakery called "Sweet Delights." The page should include a heading, a brief description of the bakery, an image of a cake (you can use a placeholder), a list of three popular items they sell, and a link to a contact page. Add some basic styling to make it visually appealing.
""",
    "description": "A test case where the instruction contains irrelevant technical details about HTML5 history, HTTP protocols, and CSS concepts that aren't directly related to the task of creating a simple webpage. This tests if INSTABOOST helps maintain focus on the actual requirements despite the presence of technical distractions."
}

# ============================================================================
# TEST CASE 5: Instructions with Emotional Narrative
# ============================================================================

EMOTIONAL_NARRATIVE_TEST = {
    "name": "Instructions with Emotional Narrative",
    "instruction": """
You are an AI assistant that helps create professional résumés. Your task is to write a résumé based on the provided career information.

I've been feeling so frustrated with my job search lately. It's been three months since I was laid off from my previous position, and despite applying to dozens of jobs, I've only had two interviews. It's really taking a toll on my confidence and mental health. I wake up every morning with a sense of dread, wondering if today will be another day of rejection emails or, worse, silence. My savings are starting to dwindle, and I'm worried about making next month's rent payment. My partner has been supportive, but I can tell they're concerned too. Sometimes I wonder if I'll ever find another job in my field.

YOUR RÉSUMÉ MUST INCLUDE THE FOLLOWING SECTIONS:
1. Header with name and contact information
2. Professional summary (3-4 sentences highlighting key qualifications)
3. Skills section (organized in categories if applicable)
4. Work experience (for each position: company name, job title, dates, and 3-5 bullet points of accomplishments)
5. Education
6. Optional sections (certifications, volunteer work, etc. if relevant)

Last night, I had a breakdown after receiving another rejection email. This was for a position I was really excited about and thought I was perfectly qualified for. The email was the standard "we've decided to move forward with other candidates" template. I couldn't help but cry, wondering what's wrong with me and why no one wants to hire me. My self-esteem has never been lower. I used to be confident in my abilities and proud of my career accomplishments, but now I question everything about my professional worth.

When writing the résumé, use strong action verbs to begin each bullet point under work experience. Quantify achievements whenever possible (e.g., "Increased sales by 20%" rather than "Increased sales"). Tailor the content to highlight experiences and skills most relevant to the target position. Keep the design clean and professional, with consistent formatting throughout.

My friend suggested that maybe my résumé is the problem. She said it might not be effectively showcasing my skills and experience. That's why I'm reaching out for help. I really need this résumé to stand out and help me land interviews. I'm starting to feel desperate, and I know that desperation isn't attractive to employers. I'm trying to stay positive, but it gets harder with each passing day. I just need a chance to prove myself. Is that too much to ask?

Remember to keep the résumé concise, ideally 1-2 pages depending on experience level. Use a clean, professional font and maintain adequate white space for readability. Avoid using personal pronouns (I, me, my) and focus on direct, achievement-oriented statements. Proofread carefully to ensure there are no spelling or grammatical errors.
""",
    "query": """
Please create a professional résumé for a marketing professional with 5 years of experience. The person has worked as a Marketing Coordinator at TechStart Inc. (2018-2020) and as a Marketing Manager at GrowthMedia (2020-present). They have a Bachelor's degree in Marketing from State University (2018) and are skilled in social media management, content creation, SEO, email marketing, and analytics tools. They've led campaigns that increased web traffic by 45% and generated a 30% increase in qualified leads.
""",
    "description": "A test case where the instruction contains an emotional narrative about job search frustrations and personal struggles, which is irrelevant to the task of creating a professional résumé. This tests if INSTABOOST helps maintain focus on the actual requirements despite the presence of emotionally distracting content."
}

# List of all distraction resistance test cases
DISTRACTION_RESISTANCE_TEST_CASES = [
    TANGENTIAL_INFORMATION_TEST,
    NARRATIVE_EMBEDDED_TEST,
    MISLEADING_EXAMPLES_TEST,
    IRRELEVANT_TECHNICAL_TEST,
    EMOTIONAL_NARRATIVE_TEST,
]
