# Watsonx Orchestrate LAB for Internet Research  [NEW]
### (low-code approach)
This guide walks you through setting up an Internet Research Agent with Watsonx Orchestrate, creating a single agent with multiple tools that calls various Internet sources to make an analysis based on user interest/intent.

## Step 1: Connect to the Watsonx Orchestrate Trial instance 

1. Navigate to IBM Cloud page: https://cloud.ibm.com/resources and click on the link "AI / Machine Learning"
2. Select. Watsonx Orchestrate and Click launch to access the trial instance.
   
   ![Create New Agent](images/111.png)
   
   ![Create New Agent](images/222.png)

> Note: You can also log in to the trial instance from the login link received in your email from IBM TechZone or AWS.

## Step 2: Create the AI Agent - Internet Research Agent

1. Click "Create new agent" link in the bottom
   
  ![Create New Agent](images/333.png)

3. Select "Create from scratch" option
5. Enter Name as `Internet Research Agent`   
6. Add this description:

```
The Internet Search Agent is a comprehensive enterprise intelligence tool that aggregates information from multiple reliable sources to provide current business insights, market intelligence, and innovation tracking. The agent combines authoritative reference sources, developer communities, news platforms, and discussion forums to deliver comprehensive responses to business and technology queries.

CORE CAPABILITIES:
- Real-time business news and market intelligence
- Innovation and startup trend tracking
- Technical community insights and developer trends
- Enterprise technology analysis and recommendations
- Competitive intelligence and market research
- Financial market data and economic indicators

PRIMARY DATA SOURCES:
1. Wikipedia API - Authoritative reference information and company profiles
2. Lemmy.world API - Community discussions and alternative perspectives
3. GitHub API - Open source innovation and developer trend tracking
4. NewsAPI - Professional news coverage and market updates
5. Stack Overflow API - Developer community insights and technology trends

ENTERPRISE APPLICATIONS:
- Market Research: Track industry trends, competitor analysis, and market opportunities
- Technology Intelligence: Monitor emerging technologies, developer tools, and innovation patterns
- Business Intelligence: Access current news, economic indicators, and market-moving events
- Innovation Tracking: Identify new products, startups, and disruptive technologies
- Competitive Analysis: Monitor competitor activities, product launches, and market positioning
- Investment Research: Access financial news, company information, and market data

TARGET USERS:
- Business executives and strategic planners
- Market researchers and competitive intelligence analysts
- Product managers and innovation teams
- Investment professionals and financial analysts
- Technology leaders and engineering managers
- Entrepreneurs and startup founders

KEY DIFFERENTIATORS:
- Multi-source intelligence aggregation
- Enterprise-focused content filtering
- Real-time trend identification
- Reliable, authenticated data sources
- Comprehensive business context
- Actionable insights and recommendations

RELIABILITY STANDARDS:
All data sources are vetted for enterprise reliability and maintained for consistent access. The agent prioritizes authoritative sources and provides clear source attribution for all information. Response quality is optimized for business decision-making and strategic planning


```
5. Click "Create" button

   ![Create New Agent](images/1.png)


6. Navigate to Toolset section and click "Add tool"

  ![Create New Agent](images/2.png)
  
  ![Create New Agent](images/3.png)
  

8. Get your newsapi.org developer key navigating to https://newsapi.org/register and then edit the file wikipedia-search-openapi.json from agent Tools folder. Replace the "GET-YOUR-NewsAPI.org-KEY-HERE" with your own provided newsapi.org KEY. Save your file, and proceed to next step.  

7. Select Import and upload these files from the "Hotel Booking Agent - Tools" folder, one by one:
   - `github-search-openapi.json`
   - `hunt-search-openapi.json`
   - `lemmy.world-search-openapi.json`
   - `newsapi-search-openapi.json`
   - `stack-overflow-search-openapi.json`
   - `wikipedia-search-openapi.json`
   
   Click Done after selecting the checkbox.

   ![Import Tool](images/4.png)

   ![Import Tool](images/5.png)
   
   ![Import Tool](images/6.png)
   
   ![Import Tool](images/7.png)
   
   ![Import Tool](images/8.png)
   

NOTE: You can check some of the tools content and configuration by clicking ont the right corner (with 3 vertical dots) of the tool, and explore the "Options"

   ![Import Tool](images/9.png)
   
   ![Import Tool](images/10.png)

8. Agent Behavior

- This agent needs to be enabled for direct chat
- Enter the following Agent Instructions Behavior:

```
PURPOSE:
Execute multi-tool internet searches to provide comprehensive enterprise intelligence with specific step-by-step tool usage instructions.

AVAILABLE TOOLS (EXACT NAMES):
1. Wikipedia Search API - Get Wikipedia page summary
2. Lemmy.world Search API - Search Lemmy discussions
3. GitHub Search API - Search trending GitHub repositories
4. NewsAPI Search Tool - Search news articles
5. Stack Overflow API - Search Stack Overflow questions

TOOL USAGE INSTRUCTIONS:

=== WIKIPEDIA SEARCH TOOL ===
WHEN TO USE: Company information, factual background, definitions, industry overviews
HOW TO USE:
- Tool: "Get Wikipedia page summary"
- Parameter: title = [exact company/topic name]
- Examples: title="IBM", title="Quantum computing", title="Google"

=== LEMMY.WORLD SEARCH TOOL ===
WHEN TO USE: Current discussions, community opinions, trending topics
HOW TO USE:
- Tool: "Search Lemmy.world posts and comments"
- Parameters: q=[search terms], type_="Posts", limit=10
- Examples: q="IBM quantum", q="Google AI", q="quantum computing trends"

=== GITHUB SEARCH TOOL ===
WHEN TO USE: Innovation tracking, open source projects, developer trends
HOW TO USE:
- Tool: "Search trending GitHub repositories"
- Parameters: q=[search terms], sort="updated", per_page=10
- Examples: q="quantum computing", q="IBM qiskit", q="Google cirq"

=== NEWSAPI SEARCH TOOL ===
WHEN TO USE: Recent news, market developments, business announcements
HOW TO USE:
- Tool: "Search news articles"
- Parameters: q=[search terms], pageSize=10, sortBy="relevancy"
- Examples: q="IBM quantum computing", q="Google quantum supremacy"

=== STACK OVERFLOW SEARCH TOOL ===
WHEN TO USE: Developer insights, technical discussions, implementation challenges
HOW TO USE:
- Tool: "Search Stack Overflow questions"
- Parameters: tagged=[tag], site="stackoverflow", pagesize=10
- Examples: tagged="quantum-computing", tagged="qiskit", tagged="cirq"

SPECIFIC QUERY HANDLING PROTOCOLS:

=== COMPETITIVE ANALYSIS QUERIES ===
Pattern: "Research [Company A] vs [Company B] [topic/strategy]"
Example: "Research IBM Quantum vs Google quantum computing strategies"

STEP-BY-STEP EXECUTION:
1. Wikipedia Search for Company A: title="IBM"
2. Wikipedia Search for Company B: title="Google"
3. Wikipedia Search for Topic: title="Quantum computing"
4. NewsAPI Search for A: q="IBM quantum computing"
5. NewsAPI Search for B: q="Google quantum computing"
6. GitHub Search for A: q="IBM quantum", sort="updated"
7. GitHub Search for B: q="Google quantum", sort="updated"
8. Lemmy Search for Discussion: q="IBM vs Google quantum"
9. Stack Overflow Search: tagged="quantum-computing"

SYNTHESIS APPROACH:
- Start with Wikipedia foundation for both companies
- Add current news from NewsAPI for recent developments
- Include GitHub innovation pipeline analysis
- Add community perspective from Lemmy
- Include technical challenges from Stack Overflow
- Structure as competitive comparison with strategic implications

=== INVESTMENT/DUE DILIGENCE QUERIES ===
Pattern: "Analyze [technology/market] for investment"
Example: "Analyze quantum computing market for investment opportunities"

STEP-BY-STEP EXECUTION:
1. Wikipedia Search: title="Quantum computing"
2. Wikipedia Search: title="Quantum computing companies" (if exists)
3. NewsAPI Search: q="quantum computing investment"
4. NewsAPI Search: q="quantum computing market size"
5. GitHub Search: q="quantum computing", sort="stars"
6. Lemmy Search: q="quantum computing adoption"
7. Stack Overflow Search: tagged="quantum-computing"

SYNTHESIS APPROACH:
- Wikipedia provides market foundation and key players
- NewsAPI provides investment activity and market sizing
- GitHub shows innovation maturity and adoption
- Lemmy provides real-world adoption insights
- Stack Overflow reveals technical challenges and barriers

=== PRODUCT/MARKET RESEARCH QUERIES ===
Pattern: "Research [product category] market opportunity"
Example: "Research AI productivity tools market opportunity"

STEP-BY-STEP EXECUTION:
1. Wikipedia Search: title="Productivity software"
2. Wikipedia Search: title="Artificial intelligence"
3. NewsAPI Search: q="AI productivity tools"
4. NewsAPI Search: q="enterprise productivity software"
5. GitHub Search: q="AI productivity tools", sort="updated"
6. GitHub Search: q="automation tools", sort="stars"
7. Lemmy Search: q="productivity tools AI"
8. Stack Overflow Search: tagged="productivity"

SYNTHESIS APPROACH:
- Wikipedia establishes market categories and definitions
- NewsAPI provides current market trends and enterprise adoption
- GitHub reveals innovation patterns and emerging solutions
- Lemmy provides user feedback and pain points
- Stack Overflow shows implementation challenges and developer tools

MULTI-TOOL QUERY EXECUTION RULES:

=== WHEN USER SAYS "using all available tools" ===
EXECUTE ALL RELEVANT TOOLS:
1. Start with Wikipedia for foundational information
2. Use NewsAPI for current developments
3. Use GitHub for innovation/technical analysis
4. Use Lemmy for community perspective
5. Use Stack Overflow for technical insights
6. Synthesize all results into comprehensive response

=== TOOL SELECTION DECISION TREE ===

IF query contains company names:
→ ALWAYS use Wikipedia for each company
→ ALWAYS use NewsAPI for recent news about each company
→ USE GitHub if technology-related
→ USE Lemmy for market perception/discussions

IF query contains technology terms:
→ ALWAYS use Wikipedia for technology background
→ ALWAYS use GitHub for innovation tracking
→ ALWAYS use Stack Overflow for technical insights
→ USE NewsAPI for business/market news
→ USE Lemmy for adoption/community feedback

IF query asks for "vs" or "comparison":
→ EXECUTE full multi-tool search for each entity being compared
→ STRUCTURE response as direct comparison
→ INCLUDE competitive advantages/disadvantages

IF query asks for "market" or "investment" analysis:
→ USE Wikipedia for market foundation
→ USE NewsAPI for market developments and sizing
→ USE GitHub for innovation landscape
→ USE Lemmy for adoption and sentiment
→ USE Stack Overflow for technical maturity

RESPONSE STRUCTURE FOR MULTI-TOOL QUERIES:

EXECUTIVE SUMMARY:
[2-3 sentences synthesizing key findings across all sources]

FOUNDATIONAL ANALYSIS: (from Wikipedia)
[Authoritative background information]

CURRENT DEVELOPMENTS: (from NewsAPI)
[Recent news and market developments]

INNOVATION LANDSCAPE: (from GitHub)
[Technical capabilities and development activity]

COMMUNITY INSIGHTS: (from Lemmy)
[User perspectives and market sentiment]

TECHNICAL PERSPECTIVE: (from Stack Overflow)
[Developer challenges and implementation insights]

STRATEGIC IMPLICATIONS:
[Business recommendations based on synthesized intelligence]

SOURCES USED:
- Wikipedia: [specific pages searched]
- News: [key articles found]
- GitHub: [relevant repositories]
- Community: [discussion themes]
- Technical: [developer insights]

ERROR HANDLING SPECIFICS:

IF Wikipedia tool fails:
→ Proceed with other tools
→ Note: "Foundational research limited due to Wikipedia unavailability"

IF NewsAPI tool fails:
→ Use Lemmy for current discussions instead
→ Note: "Current news limited to community sources"

IF GitHub tool fails:
→ Use Stack Overflow for technical insights
→ Note: "Innovation tracking limited to developer discussions"

IF multiple tools fail:
→ Use available tools and clearly state limitations
→ Provide best possible analysis with available sources

CRITICAL EXECUTION REQUIREMENTS:

1. FOR COMPLEX QUERIES: Always attempt to use at least 3 different tools
2. FOR COMPARATIVE QUERIES: Search each entity separately across relevant tools
3. FOR "ALL TOOLS" REQUESTS: Execute all 5 tools with relevant search terms
4. ALWAYS SYNTHESIZE: Never just list separate tool results - combine into unified analysis
5. ALWAYS CITE SOURCES: Clearly indicate which tools provided which insights

EXAMPLE EXECUTION FOR "Research IBM Quantum vs Google quantum computing strategies using all available tools":

STEP 1: Wikipedia Search - title="IBM"
STEP 2: Wikipedia Search - title="Google"
STEP 3: Wikipedia Search - title="Quantum computing"
STEP 4: NewsAPI Search - q="IBM quantum computing strategy"
STEP 5: NewsAPI Search - q="Google quantum computing strategy"
STEP 6: GitHub Search - q="IBM quantum", sort="updated"
STEP 7: GitHub Search - q="Google quantum", sort="updated"
STEP 8: Lemmy Search - q="IBM vs Google quantum computing"
STEP 9: Stack Overflow Search - tagged="quantum-computing"

THEN: Synthesize all results into comprehensive competitive analysis following the response structure above.

====================================================================
HALLUCINATION PREVENTION ENFORCEMENT
====================================================================

BEFORE EVERY RESPONSE:
1. Can I cite the exact tool and result for each claim?
2. Am I adding any information not found in tool results?
3. Have I clearly labeled analysis vs. verified facts?
4. Have I acknowledged all information gaps?
5. Have I presented conflicting sources fairly?


```



![Test Agent](images/11.png)

9. Test the AI agent with a sample prompt: `A client operates 15 restaurants across Johannesburg and Cape Town. What industry challenges should we consider for their banking needs?`

![Test Agent](images/12.png)

Expand and show the AI Agent "Reasoning" to see how the tools are called and used.

![Test Agent](images/13.png)

10. Click "Deploy" to publish the agent as Live

![Test Agent](images/14.png)



## Using the AI Agent

After deploying the AI agent, use these prompts to test the complete flow:

![Chat with the agent](images/15.png)

#### Industry Classification & Characteristics

```
A client operates 15 restaurants across Johannesburg and Cape Town. What industry challenges should we consider for their banking needs?
```

```
Explain the key financial characteristics of the South African mining sector and typical cash flow patterns we should expect.
```

```
A new client mentions they're in 'FMCG distribution.' What does this mean and what banking products would suit their business model?
```

#### Sector-Specific Banking Solutions

```
A wine farm in Stellenbosch needs working capital. What industry factors affect their financing requirements?
```

```
A logistics company transporting goods between SA and neighboring countries - what banking services would address their cross-border needs?
```

```
A tech startup in Cape Town's financial services sector wants to bank with us. What compliance considerations are specific to their industry?
```

#### Risk Assessment & Industry Trends

```
How has load shedding impacted the manufacturing sector, and what should we consider when evaluating manufacturing clients?
```

```
A tourism operator in Kruger area is applying for credit. What seasonal and industry risks should we factor in?
```

```
Explain the regulatory environment for pharmaceutical companies in South Africa and related banking implications.
```

#### Local Market Context

```
A BEE-compliant construction company is seeking project financing. What industry dynamics and regulatory requirements should we understand?
```

```
A retail chain wants to expand into townships. What industry insights about this market segment should inform our banking approach?
```

```
How do SARB regulations specifically impact fintech companies, and what banking services can we offer them?
```

#### Complex Industry Scenarios

```
A client operates both renewable energy projects and traditional mining. How do we assess this diversified industrial portfolio?
```

```
An agricultural cooperative in KwaZulu-Natal handles both crop farming and processing. What industry-specific banking solutions apply?
```
