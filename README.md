# AI Finance Assistant

A sophisticated multi-agent AI system for financial education, portfolio analysis, and investment guidance. This application leverages advanced language models, retrieval-augmented generation, and specialized agents to provide personalized financial assistance.

## 📖 Documentation

- 📌 **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- 🏗️ **[Architecture](docs/ARCHITECTURE.md)** - System design and technical details
- 🚀 **[Deployment Guide](docs/DEPLOYMENT.md)** - Deploy to AWS or Docker
- 📋 **[Project Reference](docs/REFERENCE.md)** - Complete API reference
- 🔧 **[Fixes Applied](docs/FIXES_APPLIED.md)** - Recent bug fixes and improvements
- 📊 **[Project Summary](docs/PROJECT_SUMMARY.md)** - Project overview
- 📑 **[File Index](docs/FILE_INDEX.md)** - Complete file listing
- 📄 **[Completion Summary](docs/COMPLETION_SUMMARY.md)** - Delivery summary

## 🌟 Features

### Core Capabilities
- **Multi-Agent Architecture**: 6 specialized agents for different financial domains
- **Intelligent Routing**: Automatic intent detection and agent selection
- **Knowledge Base**: 50+ curated financial education articles
- **Real-Time Market Data**: Live stock quotes and market indices
- **Conversational Interface**: Natural language interactions with context preservation
- **Portfolio Analysis**: Diversification insights and performance metrics
- **Goal Planning**: Financial goal setting with risk-adjusted strategies

### Six Specialized Agents

1. **Finance Q&A Agent**: Educational content on investing fundamentals
2. **Portfolio Analysis Agent**: Portfolio review, diversification assessment
3. **Market Analysis Agent**: Real-time market insights and trends
4. **Goal Planning Agent**: Financial goal setting and planning strategies
5. **News Synthesizer Agent**: Financial news analysis and impact assessment
6. **Tax Education Agent**: Tax-advantaged accounts and strategies

## 📋 Prerequisites

- Python 3.9+
- pip or conda
- Google API Key (for Gemini LLM) or OpenAI API Key
- Internet connection (for market data APIs)

## 🚀 Quick Start

### 1. Installation

```bash
# Navigate to project directory
cd AIFinAssistant

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GOOGLE_API_KEY="your_google_api_key"
# OR
export OPENAI_API_KEY="your_openai_api_key"
```

### 2. Setup Knowledge Base

```bash
python main.py --mode setup
```

This creates the financial knowledge base with educational articles.

### 3. Run the Application

**Option A: Web Interface (Recommended)**
```bash
python main.py --mode web
# or directly
streamlit run src/web_app/streamlit_app.py
```
Then open http://localhost:8501 in your browser.

**Option B: Interactive CLI**
```bash
python main.py --mode cli
```

## 📚 Project Structure

```
AIFinAssistant/
├── src/
│   ├── agents/                 # 6 specialized agents
│   │   ├── base_agent.py      # Base agent class
│   │   ├── finance_qa_agent.py
│   │   ├── portfolio_analysis_agent.py
│   │   ├── market_analysis_agent.py
│   │   ├── goal_planning_agent.py
│   │   ├── news_synthesizer_agent.py
│   │   └── tax_education_agent.py
│   ├── core/
│   │   └── llm_client.py       # LLM integration (Gemini, OpenAI)
│   ├── data/
│   │   ├── knowledge_base/     # Financial articles (JSON)
│   │   └── knowledge_base_builder.py
│   ├── rag/
│   │   └── rag_system.py       # RAG with FAISS indexing
│   ├── workflow/
│   │   └── langgraph_workflow.py  # Orchestration & routing
│   ├── web_app/
│   │   └── streamlit_app.py    # Web interface
│   └── utils/
│       └── market_data.py      # Market data APIs
├── tests/
│   └── test_suite.py           # Comprehensive tests
├── config/
│   ├── config.yaml             # Configuration file
│   └── config_loader.py        # Config management
├── docs/
│   └── ARCHITECTURE.md         # Technical details
├── requirements.txt            # Python dependencies
├── main.py                     # Entry point
└── README.md                   # This file
```

## 💡 Usage Examples

### Web Interface

1. **Chat Tab**: Ask questions about finance
   - "What is a stock?"
   - "How do I start investing?"
   - "Explain the difference between stocks and bonds"

2. **Portfolio Tab**: Add holdings and get analysis
   - Enter stock symbols (e.g., AAPL)
   - Add quantities
   - Click "Analyze" for insights

3. **Goals Tab**: Set financial goals
   - Define goal type (Retirement, Home, etc.)
   - Set target amount and timeframe
   - Get personalized planning advice

4. **Markets Tab**: Monitor market data
   - View major indices (S&P 500, NASDAQ)
   - Look up individual stocks
   - Get current quotes

### CLI Interface

```bash
python main.py --mode cli

You: What is compound interest?
Assistant: [Detailed explanation...]

You: Analyze my portfolio: AAPL 10, MSFT 5
Assistant: [Portfolio analysis...]

You: How do I plan for retirement?
Assistant: [Retirement planning guidance...]

You: exit
```

## 🔧 Configuration

Edit `config/config.yaml` to customize:

```yaml
llm:
  provider: "gemini"          # gemini, openai, claude
  model: "gemini-pro"
  temperature: 0.7

market_data:
  provider: "yfinance"        # yfinance or alpha_vantage
  yfinance:
    cache_ttl: 3600

vector_db:
  provider: "faiss"
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
  top_k_results: 5

agents:
  timeout: 30
  max_retries: 3
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run all tests
pytest tests/test_suite.py -v

# Run with coverage
pytest tests/test_suite.py --cov=src --cov-report=html

# Run specific test
pytest tests/test_suite.py::TestAgents::test_finance_qa_agent_creation -v
```

**Test Coverage: 80%+**
- Agent initialization and processing
- Knowledge base operations
- Workflow routing and state management
- Market data integration
- Edge cases and error handling

## 🔐 API Keys Setup

### Google Gemini API

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Set environment variable:
   ```bash
   export GOOGLE_API_KEY="your_key_here"
   ```

### OpenAI API (Optional)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create API key
3. Set environment variable:
   ```bash
   export OPENAI_API_KEY="your_key_here"
   ```

### Alpha Vantage API (Optional)

1. Get free API key from [Alpha Vantage](https://www.alphavantage.co/api/)
2. Set in config.yaml or environment

## 📊 Knowledge Base

The application includes 50+ curated articles on:
- Stock market fundamentals
- Portfolio diversification
- Asset allocation strategies
- Tax-advantaged accounts (401k, IRA, Roth)
- Investment principles and strategies
- Risk management
- Economic concepts
- And more...

Articles are organized by category:
- `fundamentals/`: Basic investing concepts
- `portfolio/`: Portfolio management
- `investing-strategies/`: Investment approaches
- `tax/`: Tax education
- `financial-planning/`: Planning topics

## 🚨 Important Disclaimers

This is an **educational tool**, not financial advice:
- Responses are for learning purposes only
- Consult a qualified financial advisor for personal advice
- Past performance doesn't guarantee future results
- Invest only money you can afford to lose
- All investments carry risk

## 🐳 Docker Setup (Optional)

```dockerfile
# Build image
docker build -t ai-fin-assistant .

# Run container
docker run -p 8501:8501 -e GOOGLE_API_KEY="your_key" ai-fin-assistant
```

## 📈 Performance Metrics

- **Agent Response Time**: < 5 seconds (with caching)
- **Knowledge Base Retrieval**: < 500ms
- **Market Data Fetch**: < 2 seconds
- **Memory Usage**: ~500MB (baseline)
- **Concurrent Users**: Supports multiple sessions

## 🐛 Troubleshooting

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### API Key Issues
- Verify API key is valid and has correct permissions
- Check environment variables: `echo $GOOGLE_API_KEY`
- Ensure API has quota remaining

### Knowledge Base Not Found
```bash
python main.py --mode setup
```

### Streamlit Port Already in Use
```bash
streamlit run src/web_app/streamlit_app.py --server.port 8502
```

### Market Data Errors
- Check internet connection
- Verify API rate limits
- Check yFinance service status

## 📝 Development

### Adding New Agents

1. Create new agent file in `src/agents/`
2. Extend `Agent` base class
3. Implement `process()` method
4. Register in workflow router

### Adding Knowledge Articles

1. Create JSON file in `src/data/knowledge_base/`
2. Follow schema:
   ```json
   {
     "id": "unique_id",
     "title": "Article Title",
     "category": "category_name",
     "content": "Full article text...",
     "source": "Source",
     "tags": ["tag1", "tag2"]
   }
   ```
3. Run setup: `python main.py --mode setup`

### Extending RAG

- Modify embedding model in config
- Add custom retrieval logic in `RAGRetriever`
- Experiment with similarity thresholds

## 📞 Support

For issues and questions:
1. Check troubleshooting section
2. Review test cases for examples
3. Consult agent documentation

## 📄 License

This project is provided as-is for educational purposes.

## 🙏 Acknowledgments

- LangChain for agent framework
- Hugging Face for embeddings
- FAISS for vector search
- yFinance for market data
- Google Gemini for LLM

---

**Version**: 1.0.0  
**Last Updated**: December 2024
