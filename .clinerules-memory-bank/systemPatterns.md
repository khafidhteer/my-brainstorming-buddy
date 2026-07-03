# System Patterns

## Architecture Overview

```
User Question
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Framework Selector (src/framework_selector.py) │
│  - Auto-detect via LLM classification          │
│  - Manual override by framework key             │
│  - Falls back to Fishbone on error              │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│  Orchestrator (src/orchestrator.py)             │
│  - Iterates through framework steps             │
│  - Passes previous outputs as context           │
│  - Supports early termination                   │
└──────┬──────────┬──────────┬────────────────────┘
       │          │          │
       ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Step 1   │ │ Step 2   │ │ Step N   │
│ LLM Call │→│ LLM Call │→│ LLM Call │
└──────────┘ └──────────┘ └──────────┘
       │          │          │
       └──────────┴──────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│  Formatter (src/formatter.py)                   │
│  - ChainResult (Markdown, JSON, plain text)     │
│  - StepOutput per step                          │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        Streamlit UI        CLI
        (app.py)          (main.py)
```

## Design Patterns

### 1. Template Method Pattern (BaseFramework)
All frameworks inherit from `BaseFramework` which defines the interface:
- `name`, `description`, `steps` - metadata properties
- `generate_prompt()` - abstract method each framework implements
- `should_terminate()` - optional early termination hook
- `get_step()`, `total_steps` - utility methods

### 2. Strategy Pattern (Framework Selection)
The `select_framework()` function acts as a strategy selector:
- Uses LLM to classify the question
- Returns the appropriate framework instance
- Supports manual override via `preferred` parameter
- Registry pattern via `FRAMEWORK_REGISTRY` dict

### 3. Chain-of-Responsibility (Orchestrator)
The orchestrator executes steps sequentially:
- Each step receives all previous outputs as context
- Output from step N becomes input context for step N+1
- Early termination possible via `should_terminate()`

### 4. Adapter Pattern (LLMAdapter)
Wraps the OpenAI-compatible API:
- `chat_completion()` for free-form text
- `structured_completion()` for JSON responses
- Configurable via constructor or `.env`

## Data Flow

```
Question (str)
    → Framework Selection (framework instance + key)
    → For each step:
        → generate_prompt(step_index, question, previous_outputs)
            → (system_prompt, user_prompt)
        → LLM.chat_completion(system_prompt, user_prompt)
            → output (str)
        → StepOutput(step_index, name, description, prompt, output)
    → ChainResult(question, framework, steps)
        → to_markdown() / to_json() / to_text()
```

## Key Design Decisions

1. **Async LLM calls** - All API calls use `async/await` for non-blocking I/O
2. **No Pydantic models in frameworks** - Using simple dataclasses (`StepDefinition`) to keep it lightweight
3. **Framework state is stateless** - Each call to `generate_prompt()` receives full context; no internal state
4. **Separation of concerns** - LLM adapter, framework logic, orchestration, and formatting are all separate modules
5. **Streamlit + CLI dual interface** - Same backend engine supports both UIs