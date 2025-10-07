from datetime import datetime


# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")


query_writer_instructions = """Your goal is to generate sophisticated and diverse web search queries. These queries are intended for an advanced automated web research tool capable of analyzing complex results, following links, and synthesizing information.

Instructions:
- Always prefer a single search query, only add another query if the original question requests multiple aspects or elements and one query is not enough.
- Each query should focus on one specific aspect of the original question.
- Don't produce more than {number_queries} queries.
- Queries should be diverse, if the topic is broad, generate more than 1 query.
- Don't generate multiple similar queries, 1 is enough.
- Query should ensure that the most current information is gathered. The current date is {current_date}.

Format: 
- Format your response as a JSON object with ALL two of these exact keys:
   - "rationale": Brief explanation of why these queries are relevant
   - "query": A list of search queries

Example:

Topic: What revenue grew more last year apple stock or the number of people buying an iphone
```json
{{
    "rationale": "To answer this comparative growth question accurately, we need specific data points on Apple's stock performance and iPhone sales metrics. These queries target the precise financial information needed: company revenue trends, product-specific unit sales figures, and stock price movement over the same fiscal period for direct comparison.",
    "query": ["Apple total revenue growth fiscal year 2024", "iPhone unit sales growth fiscal year 2024", "Apple stock price growth fiscal year 2024"],
}}
```

Context: {research_topic}"""


web_searcher_instructions = """Conduct targeted Google Searches to gather the most recent, credible information on "{research_topic}" and synthesize it into a verifiable text artifact.

Instructions:
- Query should ensure that the most current information is gathered. The current date is {current_date}.
- Conduct multiple, diverse searches to gather comprehensive information.
- Consolidate key findings while meticulously tracking the source(s) for each specific piece of information.
- The output should be a well-written summary or report based on your search findings. 
- Only include the information found in the search results, don't make up any information.

Research Topic:
{research_topic}
"""

reflection_instructions = """You are an expert research assistant analyzing summaries about "{research_topic}".

Instructions:
- Identify knowledge gaps or areas that need deeper exploration and generate a follow-up query. (1 or multiple).
- If provided summaries are sufficient to answer the user's question, don't generate a follow-up query.
- If there is a knowledge gap, generate a follow-up query that would help expand your understanding.
- Focus on technical details, implementation specifics, or emerging trends that weren't fully covered.

Requirements:
- Ensure the follow-up query is self-contained and includes necessary context for web search.

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_sufficient": true or false
   - "knowledge_gap": Describe what information is missing or needs clarification
   - "follow_up_queries": Write a specific question to address this gap

Example:
```json
{{
    "is_sufficient": true, // or false
    "knowledge_gap": "The summary lacks information about performance metrics and benchmarks", // "" if is_sufficient is true
    "follow_up_queries": ["What are typical performance benchmarks and metrics used to evaluate [specific technology]?"] // [] if is_sufficient is true
}}
```

Reflect carefully on the Summaries to identify knowledge gaps and produce a follow-up query. Then, produce your output following this JSON format:

Summaries:
{summaries}
"""

answer_instructions = """Generate a high-quality answer to the user's question based on the provided summaries.

Instructions:
- The current date is {current_date}.
- You are the final step of a multi-step research process, don't mention that you are the final step. 
- You have access to all the information gathered from the previous steps.
- You have access to the user's question.
- Generate a high-quality answer to the user's question based on the provided summaries and the user's question.
- **Format your answer using Markdown for clarity and readability:**
    - Use section headers (##) for main topics
    - Use bullet points for lists (e.g., operator lists, top scorers, etc.)
    - Use fenced code blocks (```) for code examples if relevant
    - **Do NOT include source links inline in the main text.**
    - Add a **References** section at the end, listing all sources as Markdown links (e.g. [apnews](https://vertexaisearch.cloud.google.com/id/1-0)). THIS IS A MUST.
    - Use concise, readable sentences and avoid unnecessary repetition

Sample Output:
## Match Result
Spain won Euro 2024, defeating England 2-1 in the final held in Berlin.

## Golden Boot Winners
- Dani Olmo (Spain)
- Harry Kane (England)
- Jamal Musiala (Germany)
- Cody Gakpo (Netherlands)
- Georges Mikautadze (Georgia)
- Ivan Schranz (Slovakia)

## References
- [wikipedia](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFDTZxsvcC3-VDMu40SKsMkKUhSR8FbQXPP8NFXihEu_imEzU1yvg3Hxlt6rEFR6qJUB2ktQ5cCN_J5K80It7TY608wUSWnDM1GdpGznH3mZju8z52yGIKirXcX6vV6FzPdrPPCNoGxN7KqQnYA)
- [youtube](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEsW77b4E55Skh_aZtJ_cPQW1ndwaLsNgFTX4VM-7m3k8ykiTUbsDn1Ie7hKnIOiaz-VoVTrWYQ9CNtdQCq0sR08Ss3fPXfPZ6SKE8TloCF01nOIHeAJ8vQszc-0ovZB7PEP7Y3CGw=)
- [aljazeera](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFi0uUpc92fbaHp1B7Sumg3b-_ow5XWd1Vk2RIpfUPyGEyT5pcO2O7PB0_H57UhUiVw4iO1GENj-xXxgLt0309fkVoN4tdxf6D0WZSRUXOzXuGStJlCbdM8RJ4mGuopGeZMcODwxYd0W-9cjKr3P2oamgHqMTq3NQIFTD44KU1sFXg-1g9SJOzooclrv7mUeTOtENVAhJfzteJAs-Wj75ve_xuKOf7iWaCKpBSdN1cnjw==)
- [foxsports](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGIl894yksD-_HpDs2eyFVp-f3SYf5KMFPESMgvRpclJb-zc8UfjLGUgBC86QNUQlXECXYDQj7WnX8jXNH2II-v268EIht6EWsiQwg7xwh029Q-AE17yR0pLM5eQDHwl1CrOHcrsJINeMOS8mm0wViYn9AOiLFHAhjpKPXXZO73tsvrZHDZodD0gAFzLzAm8uLUrg==)
- [uefa](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGsGLFXjKifw8kLL8_Fiji6m-b_s9n5Ipsb8Z_ez-YvE4j2afpZTtIgnBWuDeTUYrhoEefjkUR3U655tKUoXChu5SYRb9dxIvRt8fKTrOKRMCPy44WQSzzJlpaLGGC4iSIr9F0kguSkm5_X3RaTshPRDbBjf550ObCZf1J71nTz8eZSBx-2j0H84gckzc48voL3MVjTL1VZlTzG1uvNE9HIbFtSqMTTaBocOsIyRwpkP4WUFC-0Wqsc3rXHdIw7Z2Js)

User Context:
- {research_topic}

Summaries:
{summaries}"""
