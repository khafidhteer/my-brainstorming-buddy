# Product Context

## Why This Project Exists
Users often ask complex analytical questions that require structured reasoning rather than a single answer. Standard LLM chat gives one-shot responses without the rigor of formal analytical frameworks. This system forces the LLM to think step-by-step through established methodologies, producing more thorough, auditable, and actionable results.

## Problem Being Solved
- **Single answers lack depth** - LLMs give one response without showing their reasoning chain
- **Framework selection is expertise-dependent** - Most people don't know which analytical framework to apply
- **Context is lost** - Without chained reasoning, each answer is independent of previous analysis
- **No structured output** - Raw LLM responses are unstructured and hard to compare across analyses

## User Personas

### Business Analyst
- Asks "why" questions about processes, metrics, and outcomes
- Needs structured root cause analysis for presentations
- Benefits from Fishbone, DMAIC, Apollo RCA

### Safety/Reliability Engineer
- Investigates incidents, failures, and accidents
- Needs formal failure analysis methodologies
- Benefits from Fault Tree, STAMP, Swiss Cheese

### Strategist/Decision-Maker
- Faces complex, ambiguous situations
- Needs to classify problems before acting
- Benefits from Cynefin, Iceberg Model, Three Horizons of Growth

### Quality Manager
- Runs process improvement initiatives
- Needs data-driven improvement methodology
- Benefits from DMAIC, Fishbone

### Product Manager / Innovator
- Designs products and features for specific customer needs
- Needs to understand what customers are truly trying to accomplish
- Benefits from JTBD, Value Proposition Canvas, Blue Ocean Strategy

### Marketing Strategist
- Plans go-to-market campaigns and brand positioning
- Needs to segment markets and position offerings effectively
- Benefits from STP, Ideal Customer Profile, Technology Adoption Life Cycle

### Startup Founder / Entrepreneur
- Decides which market to enter and how to scale
- Needs to identify beachhead markets and plan expansion
- Benefits from Beachhead Market Strategy, Blue Ocean Strategy, Three Horizons of Growth

### Sales Leader
- Defines target accounts and optimizes lead scoring
- Needs to focus the sales team on high-value prospects
- Benefits from Ideal Customer Profile, STP

## How It Should Work
1. User asks a question in natural language
2. System auto-detects the best framework from 16 available (or user overrides)
3. System executes the framework step-by-step, each step building on previous outputs
4. User sees the complete reasoning chain with intermediate results
5. User can export the analysis as Markdown or JSON

## Core Value Proposition
"Get not just an answer, but the **reasoning path** that led to it, validated through a formal analytical framework."

## Framework Categories
The 16 frameworks fall into two broad categories:

### Analytical / Root Cause (8 frameworks)
For investigating problems, failures, and incidents:
Fishbone, Fault Tree, Iceberg, Apollo RCA, STAMP, Swiss Cheese, Cynefin, DMAIC

### Business / Strategy (8 frameworks)
For market decisions, customer understanding, and growth planning:
JTBD, Value Proposition Canvas, Beachhead Market, Technology Adoption Life Cycle, Blue Ocean, Ideal Customer Profile, STP, Three Horizons of Growth