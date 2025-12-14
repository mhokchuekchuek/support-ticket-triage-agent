# TriageAgent

Agent that triages support tickets using LLM with tools.

## Location

`src/modules/agents/triage.py`

## Class

### `TriageAgent(BaseAgent)`

Analyzes tickets using LLM with KB search and customer lookup tools.

**Constructor Parameters** (all injected):

| Parameter | Type | Description |
|-----------|------|-------------|
| `llm` | BaseLLM | LLM client for text generation |
| `kb_tool` | KBRetrievalTool | Knowledge base retrieval tool |
| `customer_tool` | CustomerLookupTool | Customer lookup tool |
| `prompt_manager` | BasePromptManager | Prompt manager for loading prompts |
| `name` | str | Agent name (default: "triage_agent") |

## Methods

### `execute(state) -> AgentState`

Execute triage on current state.

**Flow**:
1. Look up customer info
2. Search knowledge base
3. Get system prompt from Langfuse
4. Build user prompt with context
5. Get LLM response
6. Parse response into TriageResult

## Usage

```python
from src.modules.agents.triage import TriageAgent
from libs.llm.client.selector import LLMClientSelector
from libs.llm.prompt_manager.selector import PromptManagerSelector
from libs.database.vector.selector import VectorStoreSelector
from src.modules.agents.tools.kb_retrieval import KBRetrievalTool
from src.modules.agents.tools.customer_lookup import CustomerLookupTool

# Create dependencies
llm = LLMClientSelector.create(provider="litellm", model="gpt-4o-mini")
vector_store = VectorStoreSelector.create(provider="qdrant", collection_name="kb")
prompt_manager = PromptManagerSelector.create(provider="langfuse")

kb_tool = KBRetrievalTool(vector_store=vector_store)
customer_tool = CustomerLookupTool(data_path="data/customers.json")

# Create agent
agent = TriageAgent(
    llm=llm,
    kb_tool=kb_tool,
    customer_tool=customer_tool,
    prompt_manager=prompt_manager,
)

# Use with workflow
from src.modules.graph.workflow import TriageWorkflow

workflow = TriageWorkflow(triage_agent=agent)
result = workflow.invoke(ticket)
```
