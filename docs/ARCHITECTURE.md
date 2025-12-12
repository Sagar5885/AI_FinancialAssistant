# AI Finance Assistant - Architecture Documentation

## System Overview

The AI Finance Assistant is a sophisticated multi-agent system designed to provide personalized financial education and guidance through an intelligent conversational interface.

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                          │
│  (Streamlit Web App / CLI Interface)                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│              CONVERSATION MANAGEMENT LAYER                       │
│  (Intent Detection, State Management, Routing)                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼────────┐  ┌─────▼───────────┐
│  AGENT LAYER │  │  RAG LAYER      │  │  MARKET DATA    │
│              │  │                 │  │                 │
│ • Finance QA │  │ • Knowledge Base│  │ • yFinance API  │
│ • Portfolio  │  │ • FAISS Index   │  │ • Alpha Vantage │
│ • Market     │  │ • Embeddings    │  │ • Caching       │
│ • Goals      │  │ • Retrieval     │  │                 │
│ • News       │  │                 │  │                 │
│ • Tax        │  │                 │  │                 │
└────────┬─────┘  └────────┬────────┘  └─────┬───────────┘
         │                 │                  │
         └─────────────────┼──────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
┌───────▼──────────────┐          ┌──────────▼──────┐
│   LLM CLIENT         │          │  DATA LAYER     │
│                      │          │                 │
│ • Google Gemini      │          │ • Articles JSON │
│ • OpenAI GPT         │          │ • Vector Index  │
│ • Retries/Fallback   │          │ • Cache         │
└──────────────────────┘          └─────────────────┘
```

## Component Architecture

### 1. User Interface Layer

#### Streamlit Web App (`src/web_app/streamlit_app.py`)
- **Chat Interface**: Natural language conversation
- **Portfolio Tab**: Manage and analyze holdings
- **Goals Tab**: Set and track financial goals
- **Markets Tab**: Real-time market data
- **Home Tab**: Overview and quick stats

**Key Features:**
- Multi-tab interface
- Session state management
- Real-time market updates
- Responsive design

### 2. Conversation Management

#### Intent Detector (`src/workflow/langgraph_workflow.py`)
- Analyzes user queries to detect intent
- Routes to appropriate agent
- Extracts context parameters
- Keyword-based detection with fallbacks

**Supported Intents:**
- Finance Q&A (education)
- Portfolio analysis
- Market insights
- Goal planning
- News synthesis
- Tax education

#### Workflow State
- Maintains conversation history
- Tracks user portfolio
- Stores goals and preferences
- Preserves context across interactions

#### Conversation Manager
- Session management (per user)
- Message routing and processing
- Portfolio updates
- Goal tracking
- Session persistence

### 3. Agent Layer

#### Base Agent Class (`src/agents/base_agent.py`)
```python
class Agent:
    - process(query, context) → response
    - retrieve_context(query) → knowledge base content
    - generate_response(prompt, context) → LLM output
    - add_to_memory(message) → store in agent memory
    - get_memory() → conversation history
```

#### Six Specialized Agents

1. **Finance Q&A Agent** (`finance_qa_agent.py`)
   - Purpose: General financial education
   - Knowledge Base: All articles
   - Specialization: Clear, jargon-free explanations
   - Example: "What is a stock?"

2. **Portfolio Analysis Agent** (`portfolio_analysis_agent.py`)
   - Purpose: Analyze investment portfolios
   - Features: Diversification assessment, risk analysis
   - Data Input: Stock symbols and quantities
   - Example: "Analyze my portfolio: AAPL 10, MSFT 5"

3. **Market Analysis Agent** (`market_analysis_agent.py`)
   - Purpose: Provide real-time market insights
   - Data Source: Real-time stock quotes
   - Analysis: Market trends, indices, sentiment
   - Example: "What's happening in the market?"

4. **Goal Planning Agent** (`goal_planning_agent.py`)
   - Purpose: Financial goal setting and planning
   - Parameters: Goal type, amount, timeframe, risk tolerance
   - Output: Personalized strategies
   - Example: "Help me plan for retirement"

5. **News Synthesizer Agent** (`news_synthesizer_agent.py`)
   - Purpose: Contextualize financial news
   - Input: News articles/topics
   - Analysis: Impact assessment, implications
   - Example: "What's the impact of this market news?"

6. **Tax Education Agent** (`tax_education_agent.py`)
   - Purpose: Tax and account education
   - Topics: 401k, IRA, Roth, HSA, tax strategies
   - Output: Educational, not tax advice
   - Example: "Explain the difference between Roth and Traditional IRA"

### 4. RAG (Retrieval-Augmented Generation) Layer

#### Knowledge Base (`src/rag/rag_system.py`)
- **Storage**: JSON files organized by category
- **Articles**: 50+ curated financial articles
- **Categories**:
  - Fundamentals (stocks, bonds, investing)
  - Portfolio management
  - Investing strategies
  - Tax education
  - Financial planning
  - Economic concepts

#### RAG Retriever
- **Embedding Model**: Sentence Transformers
- **Vector DB**: FAISS (local) / Chroma (optional)
- **Retrieval**: Semantic similarity search
- **Context Building**: Aggregates top-k relevant documents

**Process:**
```
Query → Embedding → Vector Search → Ranked Results → Context
```

#### RAG Context Builder
- Formats retrieved documents
- Adds source citations
- Respects token limits
- Preserves document structure

### 5. LLM Client Layer

#### LLM Abstraction (`src/core/llm_client.py`)

**Supported Providers:**
- Google Gemini (default)
- OpenAI GPT
- Claude (ready to integrate)

**Features:**
- Unified interface
- Automatic retries with exponential backoff
- Error handling and fallbacks
- Temperature control
- Token limits

**Process:**
```
Prompt → Provider → LLM Call → Retry Logic → Response
```

### 6. Market Data Layer

#### Market Data Integration (`src/utils/market_data.py`)

**Providers:**
- yFinance (default)
- Alpha Vantage (backup)

**Features:**
- Real-time stock quotes
- Market indices (S&P 500, NASDAQ, Dow)
- Portfolio performance metrics
- Caching with TTL
- Rate limit handling

**Data Classes:**
- `StockQuote`: Symbol, price, change, 52-week stats
- `MarketTrend`: Index value and change
- `MarketDataCache`: TTL-based caching

### 7. Workflow Orchestration

#### Router
- Receives user query
- Detects intent
- Routes to appropriate agent(s)
- Merges context
- Returns response

#### Conversation Manager
- Creates/manages user sessions
- Maintains state
- Processes messages through router
- Handles portfolio/goal updates
- Provides session summaries

## Data Flow

### Typical Conversation Flow

```
1. User Input (UI)
   ↓
2. Intent Detection
   - Keywords analysis
   - Context extraction
   ↓
3. Agent Selection
   - Route to appropriate agent
   ↓
4. Context Retrieval
   - Query knowledge base
   - Fetch market data if needed
   ↓
5. LLM Processing
   - Format prompt with context
   - Generate response
   - Handle errors/retries
   ↓
6. Response Formatting
   - Add source citations
   - Apply disclaimers
   ↓
7. State Update
   - Store in conversation history
   - Update user profile
   ↓
8. Response to User
```

## State Management

### Workflow State
```python
{
    "user_id": str,
    "messages": List[Message],
    "current_agent": AgentType,
    "context": Dict,           # Shared context
    "portfolio": Dict,         # Holdings
    "goals": List[Goal],       # Financial goals
    "preferences": Dict        # User preferences
}
```

### Message Format
```python
{
    "role": "user|assistant",
    "content": str,
    "timestamp": datetime,
    "metadata": Dict           # Optional metadata
}
```

## Error Handling & Resilience

### Multi-Level Fallbacks
1. **LLM Level**: Retry with exponential backoff
2. **Agent Level**: Graceful error messages
3. **Market Data**: Cached values or static fallbacks
4. **RAG**: Keyword matching if semantic search fails
5. **UI Level**: User-friendly error display

### Rate Limiting
- API call caching with TTL
- Batch processing where possible
- Graceful degradation on limits
- User feedback on timeouts

## Security & Privacy

### API Key Management
- Environment variables
- Config file encryption (future)
- No logs of sensitive data
- Rate limiting per user

### Data Handling
- No persistent user data storage
- Session-based storage
- Clear data on logout
- GDPR-compliant design

## Performance Characteristics

### Benchmarks
- **Agent Response**: 2-5 seconds (cached)
- **Knowledge Retrieval**: <500ms
- **Market Data Fetch**: 1-3 seconds
- **Memory Per Session**: ~50MB
- **Concurrent Sessions**: Supports 100+

### Optimization Techniques
- FAISS vector indexing
- Response caching
- Lazy loading
- Batch processing
- Connection pooling

## Extensibility

### Adding New Agents
1. Extend `Agent` base class
2. Implement `process()` method
3. Register in `AgentType` enum
4. Add to router configuration

### Adding Knowledge Articles
1. Create JSON in `knowledge_base/`
2. Follow schema:
   ```json
   {
     "id": "unique_id",
     "title": "Article Title",
     "category": "category",
     "content": "Full text",
     "source": "Source",
     "tags": ["tag1", "tag2"]
   }
   ```
3. Run setup to rebuild index

### Integrating New LLMs
1. Create provider class in `llm_client.py`
2. Implement required methods
3. Update config
4. No code changes needed elsewhere (abstraction)

## Deployment Considerations

### Docker Deployment
```bash
docker-compose up -d
```

### Scaling
- Stateless agent design (easy horizontal scaling)
- Separate vector DB for production
- Session store (Redis for multi-instance)
- Load balancer for requests

### Monitoring
- Logging to `logs/app.log`
- Performance metrics
- Error tracking
- API usage stats

## Testing Strategy

### Test Coverage
- Unit tests: Agent logic
- Integration tests: Agent + RAG + LLM
- End-to-end tests: Full conversation flows
- Edge case tests: Error conditions

### Test Levels
- `test_suite.py`: 30+ tests covering:
  - Agent creation and processing
  - Knowledge base operations
  - Intent detection
  - Market data handling
  - Workflow state management
  - Error conditions

## Configuration Management

### Config Hierarchy
1. `config/config.yaml` - Defaults
2. Environment variables - Overrides
3. Runtime parameters - Session-specific

### Key Configuration Areas
- LLM provider and settings
- Market data source
- Vector DB configuration
- Agent timeouts
- Logging levels

---

**Version**: 1.0.0  
**Last Updated**: December 2024
