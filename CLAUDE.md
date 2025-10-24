# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered coffee shop chatbot application with market basket analysis and RAG-based product recommendations. The system uses a multi-agent architecture where specialized agents handle different aspects of customer interactions.

**Core Technologies:**
- LLM: Meta Llama 3.1 8B Instruct (hosted on RunPod)
- Vector Database: Pinecone (for RAG-based product details)
- Recommendation Engine: Apriori algorithm + popularity-based filtering
- Deployment: RunPod serverless platform
- Python dependencies: OpenAI SDK, pandas, numpy, pinecone, runpod

## Architecture

### Multi-Agent System

The application uses an **agent controller** pattern (`agent_controller.py`) that routes user messages through a pipeline:

1. **GuardAgent**: Validates that user queries are coffee shop-related and within allowed scope
2. **ClassificationAgent**: Routes the request to the appropriate specialized agent based on intent
3. **Specialized Agents**:
   - `DetailsAgent`: Answers questions about the shop (hours, location, menu items) using RAG with Pinecone
   - `OrderTakingAgent`: Manages the order conversation flow with state tracking
   - `RecommendationAgent`: Provides product recommendations using Apriori or popularity algorithms

**Key Pattern**: All agents implement the `AgentProtocol` interface requiring a `get_response(messages)` method that returns a standardized dict with `role`, `content`, and `memory` fields.

### Message Flow

Messages follow OpenAI chat format with an additional `memory` field for agent-specific state:
```python
{
    "role": "assistant",
    "content": "response text",
    "memory": {
        "agent": "agent_name",
        # agent-specific state (order, step number, decisions, etc.)
    }
}
```

### Agent Communication

- **GuardAgent** and **ClassificationAgent** use JSON mode (`use_json_mode=True`) for structured outputs
- All agent LLM calls go through `utils.get_chatbot_respnse()` with a fallback `double_check_json_output()` for validation
- State is maintained in message history, not in agent instances (agents are stateless except for initialization data)

## Development Commands

### Local Development
```bash
# Run the interactive CLI version for testing
cd python_code/api
python development.py

# Test with custom JSON input
python main.py  # expects RunPod serverless format
```

### Docker Build & Run
```bash
# Build Docker image
cd python_code/api
docker build -t coffee-chatbot .

# Run locally (requires .env file)
docker run --env-file .env coffee-chatbot
```

### Environment Setup

Create `.env` files in both `python_code/` and `python_code/api/` with:
- `RUNPOD_TOKEN`: RunPod API key
- `RUNPOD_CHATBOT_URL`: LLM endpoint URL
- `RUNPOD_EMBEDDING_URL`: Embedding model endpoint
- `MODEL_NAME`: LLM model identifier
- `PINECONE_API_KEY`: Pinecone API key
- `PINECONE_INDEX_NAME`: Vector database index name
- Firebase credentials (for potential future features)

## Data Files

- `recommendation_objects/apriori_recommendations.json`: Pre-computed market basket associations
- `recommendation_objects/popularity_recommendation.csv`: Product popularity rankings with categories
- Pinecone index stores vectorized product/shop information for RAG queries

## Important Implementation Details

### Recommendation Logic

The `RecommendationAgent` has three modes:
1. **Apriori**: Market basket analysis - "customers who bought X also bought Y"
2. **Popular**: Overall most popular items
3. **Popular by Category**: Most popular within a specific category (e.g., "coffee", "pastries")

Apriori recommendations are diversified by limiting max 2 items per category (`recommendations_per_category`).

### Order Taking Flow

`OrderTakingAgent` maintains state through `memory`:
- `step number`: Current stage in order process
- `order`: List of `{"item": str, "quantity": int, "price": float}`
- `asked_recommendation_before`: Boolean to avoid duplicate recommendations

After first order items are added, it automatically calls `RecommendationAgent.get_recommendation_from_order()` once.

### JSON Output Handling

All structured agent outputs use a two-step validation:
1. LLM generates JSON (with `use_json_mode=True` when available)
2. `double_check_json_output()` validates and uses regex extraction + LLM repair if needed

This pattern is critical because the Llama model sometimes adds text outside JSON braces.

### RAG Implementation

`DetailsAgent` uses semantic search:
1. Embed user query with OpenAI-compatible embedding endpoint
2. Query Pinecone with top_k=2 for relevant context
3. Inject context into LLM prompt for grounded responses

## Testing Notes

- `development.py`: Interactive CLI that clears screen between messages, useful for conversation testing
- `test_input.json`: Sample RunPod serverless format payload
- The system expects conversation history in the `messages` list - always include prior context for multi-turn conversations

## Code Organization

```
python_code/api/
├── agents/
│   ├── __init__.py          # Exports all agents
│   ├── agent_protocol.py    # Protocol interface
│   ├── guard_agent.py
│   ├── classification_agent.py
│   ├── details_agent.py
│   ├── order_taking_agent.py
│   ├── recommendation_agent.py
│   └── utils.py             # Shared LLM/embedding helpers
├── recommendation_objects/   # Pre-computed recommendation data
├── agent_controller.py      # Main routing logic
├── main.py                  # RunPod serverless entry point
├── development.py           # Local testing CLI
└── Dockerfile
```

Jupyter notebooks in `python_code/` contain the data preparation pipelines (recommendation engine training, vector DB population, Firebase uploading).
