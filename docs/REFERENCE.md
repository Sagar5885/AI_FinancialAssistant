# AI Finance Assistant - Reference Guide

## Quick Reference

### Installation (3 steps)
```bash
pip install -r requirements.txt
export GOOGLE_API_KEY="your_key"
python3 main.py --mode web
```

### Project Structure
```
src/agents/              → 6 specialized agents
src/core/              → LLM clients
src/rag/               → Knowledge base & RAG
src/workflow/          → Intent routing
src/utils/             → Market data APIs
src/web_app/           → Streamlit UI
tests/                 → Test suite
config/                → Configuration
docs/                  → Documentation
```

### Running the App

**Web Interface** (Recommended)
```bash
python3 main.py --mode web
# Open http://localhost:8501
```

**CLI Interface**
```bash
python3 main.py --mode cli
# Interactive prompt
```

**Docker**
```bash
docker-compose up -d
# Access at http://localhost:8501
```

### Testing

**Run Test Suite**
```bash
python3 test_suite.py
```

**Validate Project**
```bash
python3 validate_project.py
```

**Run Specific Tests**
```bash
pytest tests/test_suite.py::TestAgents -v
```

## Supported Queries

### Finance Education
- "What is a stock?"
- "Explain bonds"
- "How do I start investing?"
- "What's diversification?"

### Portfolio Analysis
- "Analyze my portfolio: AAPL 10, MSFT 5"
- "Is my portfolio diversified?"
- "What's my total portfolio value?"

### Market Analysis
- "What's the current market doing?"
- "What's the S&P 500 today?"
- "Look up TESLA stock"

### Goal Planning
- "Help me plan for retirement"
- "How much should I save for a home?"
- "Plan $1M goal in 20 years"

### Tax Education
- "Explain 401k vs IRA"
- "What's a Roth account?"
- "Tax loss harvesting explained"

### News & Analysis
- "What's the impact of this news?"
- "Explain recent market events"
- "Contextualize this financial news"

## Configuration

### Environment Variables
```bash
GOOGLE_API_KEY=your_key          # Required for Gemini
OPENAI_API_KEY=your_key          # For OpenAI (optional)
ALPHA_VANTAGE_API_KEY=your_key   # For Alpha Vantage (optional)
LOG_LEVEL=INFO                   # INFO, DEBUG, WARNING, ERROR
STREAMLIT_SERVER_PORT=8501       # Default port
```

### Config File (config/config.yaml)
```yaml
llm:
  provider: "gemini"             # gemini, openai, claude
  temperature: 0.7               # 0-1, higher = more creative

market_data:
  provider: "yfinance"           # yfinance, alpha_vantage
  cache_ttl: 3600                # Cache duration in seconds

vector_db:
  top_k_results: 5               # Top results from knowledge base
```

## Knowledge Base

### Categories
- `fundamentals/` - Basic concepts
- `portfolio/` - Portfolio management
- `tax/` - Tax education
- `investing-strategies/` - Investment approaches
- `economic-concepts/` - Economic theory
- `investing-products/` - ETFs, index funds
- `financial-planning/` - Planning topics
- `investing-principles/` - Core principles

### Adding Articles
1. Create JSON in `src/data/knowledge_base/`
2. Format: `{"id": "...", "title": "...", "content": "...", "category": "...", "source": "...", "tags": [...]}`
3. Run: `python3 main.py --mode setup`

## API Keys

### Google Gemini (Free Tier)
1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Export: `export GOOGLE_API_KEY="key"`

### OpenAI (Paid)
1. Visit https://platform.openai.com/api-keys
2. Create new key
3. Export: `export OPENAI_API_KEY="key"`

### Alpha Vantage (Free/Paid)
1. Visit https://www.alphavantage.co/api/
2. Get free key
3. Add to `config/config.yaml`

## Agents Overview

| Agent | Purpose | Use Case |
|-------|---------|----------|
| Finance Q&A | General education | Learning financial concepts |
| Portfolio | Holdings analysis | Understanding your portfolio |
| Market | Real-time insights | Market conditions |
| Goals | Financial planning | Setting targets |
| News | Contextualize news | Understanding impact |
| Tax | Account education | Tax strategies |

## Common Issues

| Issue | Solution |
|-------|----------|
| Port 8501 in use | `streamlit run ... --server.port 8502` |
| API key error | Check `echo $GOOGLE_API_KEY` |
| No market data | Check internet, wait for cache |
| Slow responses | Check API quota, increase timeout |
| Import errors | `pip install -r requirements.txt` |

## Performance Tips

- Use **caching** - Responses cache for speed
- **Batch queries** - Ask related questions together
- **Specific queries** - More specific = better results
- **Check markets tab** - Real-time data there
- **Use portfolio tab** - Easier than typing symbols

## File Locations

| File | Purpose |
|------|---------|
| `main.py` | Entry point |
| `test_suite.py` | Test runner |
| `validate_project.py` | Project validator |
| `config/config.yaml` | Configuration |
| `src/agents/` | Agent implementations |
| `src/data/knowledge_base/` | Articles |
| `logs/app.log` | Application logs |
| `Dockerfile` | Container config |
| `docker-compose.yml` | Docker orchestration |

## Documentation Files

- `README.md` - Complete guide
- `QUICK_START.md` - 5-minute setup
- `ARCHITECTURE.md` - System design
- `DEPLOYMENT.md` - Deployment guide
- `PROJECT_SUMMARY.md` - Project overview
- `.env.example` - Environment template

## Development Commands

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run application
python3 main.py --mode web
python3 main.py --mode cli
python3 main.py --mode setup

# Testing
python3 test_suite.py
python3 validate_project.py

# Generate knowledge base
python3 src/data/knowledge_base_builder.py

# Docker
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## Code Organization

### Adding a New Agent
1. Create `src/agents/my_agent.py`
2. Extend `Agent` class
3. Implement `process()` method
4. Add to `AgentType` enum
5. Register in router

### Adding Knowledge Article
1. Create JSON in `src/data/knowledge_base/`
2. Follow schema
3. Run: `python3 main.py --mode setup`

### Extending LLM Support
1. Create class in `src/core/llm_client.py`
2. Implement `LLMProvider` interface
3. Add to `LLMClient.provider` logic
4. Update config.yaml

## Troubleshooting Guide

### Can't Import Modules?
```bash
pip install -r requirements.txt
python3 test_suite.py
```

### API Not Working?
```bash
echo $GOOGLE_API_KEY
# Should show your key, if not:
export GOOGLE_API_KEY="your_key"
```

### No Market Data?
```bash
# Check internet connection
ping google.com

# Verify yfinance works
python3 -c "import yfinance; yfinance.Ticker('AAPL')"
```

### Memory Issues?
```bash
# Reduce cache TTL in config.yaml
# Or restart application
# Or limit knowledge base size
```

## Success Indicators

✅ **All Systems Working When:**
- `python3 test_suite.py` shows 7/7 passed
- `python3 validate_project.py` shows all green
- Web interface loads on http://localhost:8501
- Knowledge base shows 8+ categories
- Can ask financial questions and get responses

## Next Steps

1. **Get Started**
   ```bash
   pip install -r requirements.txt
   export GOOGLE_API_KEY="your_key"
   python3 main.py --mode web
   ```

2. **Explore Features**
   - Try different agents
   - Add portfolio holdings
   - Set financial goals
   - Check market data

3. **Learn & Customize**
   - Read architecture docs
   - Explore agent code
   - Add custom knowledge
   - Integrate more APIs

4. **Deploy**
   - Follow deployment guide
   - Set up monitoring
   - Configure backups
   - Optimize performance

## Resources

- **LangChain**: https://python.langchain.com/
- **Streamlit**: https://streamlit.io/
- **FAISS**: https://faiss.ai/
- **yFinance**: https://github.com/ranaroussi/yfinance
- **Google Gemini**: https://ai.google.dev/

## Support

For help:
1. Check README.md
2. Review ARCHITECTURE.md
3. Look at test examples
4. Check inline code comments
5. Review error logs in `logs/app.log`

---

**Quick Help**: See QUICK_START.md for fastest setup!
