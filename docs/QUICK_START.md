# 🚀 Quick Start Guide - AI Finance Assistant

Get up and running in 5 minutes!

## Step 1: Clone and Setup (1 min)

```bash
cd AIFinAssistant
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

## Step 2: Install Dependencies (2 min)

```bash
pip install -r requirements.txt
```

## Step 3: Get API Key (1 min)

**Option A: Google Gemini (Recommended)**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

**Option B: OpenAI**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy the key

## Step 4: Set Environment Variable

```bash
# macOS/Linux
export GOOGLE_API_KEY="paste_your_key_here"

# Windows (PowerShell)
$env:GOOGLE_API_KEY="paste_your_key_here"
```

## Step 5: Run Application

```bash
# Web interface (Recommended)
python main.py --mode web

# Opens at http://localhost:8501
```

## ✨ First Interaction

Try these questions:
- "What are stocks and how do they work?"
- "How do I start investing?"
- "Explain the S&P 500"
- "What's the difference between stocks and bonds?"

## 📱 Web Interface Features

### Chat Tab
- Ask any financial question
- Get educational responses
- View conversation history

### Portfolio Tab
- Add stock symbols (AAPL, MSFT, etc.)
- Get portfolio analysis
- See diversification insights

### Goals Tab
- Set financial goals
- Specify target amount and timeline
- Get personalized planning

### Markets Tab
- View S&P 500, NASDAQ, Dow Jones
- Look up individual stocks
- Get real-time quotes

## 🆘 Troubleshooting

**"No module named 'streamlit'"**
```bash
pip install -r requirements.txt
```

**"API Key Error"**
- Check GOOGLE_API_KEY is set correctly
- Verify key has API enabled
- Try a fresh API key

**"Port 8501 already in use"**
```bash
streamlit run src/web_app/streamlit_app.py --server.port 8502
```

## 📚 Try CLI Mode

```bash
python main.py --mode cli

# Interactive prompt - ask questions directly!
```

## 🐳 Docker Mode

```bash
docker-compose up -d
# Access at http://localhost:8501
```

## 📖 Next Steps

1. Read the [full README.md](README.md)
2. Explore [Architecture](docs/ARCHITECTURE.md)
3. Run the [test suite](tests/test_suite.py)
4. Check [API docs](docs/API.md)

## 💡 Tips

- The app works better with longer context
- Be specific with portfolio symbols
- Ask follow-up questions for deeper learning
- Check the Markets tab for current data

## 🎯 Example Scenarios

**Scenario 1: Learning**
```
You: What is diversification?
Assistant: [Educational explanation]
You: Why is it important?
Assistant: [Context and examples]
```

**Scenario 2: Portfolio Analysis**
```
Portfolio Tab → Add: AAPL 10, MSFT 5
Click: Analyze My Portfolio
Get: Detailed analysis and recommendations
```

**Scenario 3: Goal Planning**
```
Goals Tab → Set: Retirement, $1M, 20 years, Moderate
Get: Personalized planning advice
```

---

**Ready to learn about finance? Let's go! 💰**
