"""
Financial knowledge base - Educational articles on investing and personal finance
"""
import json
from pathlib import Path

# Create comprehensive financial education articles
KNOWLEDGE_BASE_ARTICLES = [
    {
        "id": "stocks_101",
        "title": "Understanding Stocks: A Beginner's Guide",
        "category": "fundamentals",
        "content": """Stocks represent ownership shares in a company. When you buy stock, you become a partial owner.

Key Concepts:
- Share Price: The current market price of one share
- Market Cap: Total value of all shares (Share Price × Shares Outstanding)
- Dividend: Regular payments to shareholders
- Trading: Buying and selling through stock exchanges

Benefits of Investing in Stocks:
- Potential for long-term growth
- Dividend income
- Low cost of entry
- Easy to buy and sell

Risks:
- Price volatility
- Company-specific risks
- Market downturns
- No guaranteed returns

Beginner Tips:
- Start with index funds for diversification
- Don't try to time the market
- Invest for the long term
- Dollar-cost average (invest regularly)""",
        "source": "Financial Education Guide",
        "tags": ["stocks", "investing", "beginner"]
    },
    {
        "id": "bonds_explained",
        "title": "Bonds: Fixed Income Investing",
        "category": "fundamentals",
        "content": """Bonds are loans you make to companies or governments that pay interest.

How Bonds Work:
- You lend money to a borrower (issuer)
- Issuer pays fixed interest (coupon) over time
- You get principal back at maturity
- Bonds are less volatile than stocks

Types of Bonds:
- Government Bonds: Issued by governments
- Corporate Bonds: Issued by companies
- Municipal Bonds: Issued by local governments
- Treasury Securities: U.S. government backed

Bond Basics:
- Yield: Annual interest rate
- Duration: Sensitivity to interest rates
- Credit Rating: Risk of default
- Par Value: Face value of bond

Pros and Cons:
✓ More stable than stocks
✓ Regular income
✗ Lower growth potential
✗ Inflation risk
✗ Interest rate risk""",
        "source": "Financial Education Guide",
        "tags": ["bonds", "fixed-income", "investing"]
    },
    {
        "id": "diversification",
        "title": "Portfolio Diversification: Don't Put All Eggs in One Basket",
        "category": "portfolio",
        "content": """Diversification is a strategy to reduce risk by spreading investments across different assets.

Why Diversify:
- Reduces concentration risk
- Smooths returns over time
- Protects against company/sector downturns
- Helps achieve financial goals

Diversification Methods:
1. Asset Class Diversification:
   - Stocks, bonds, cash, real estate
   
2. Sector Diversification:
   - Technology, Healthcare, Finance, Energy, Consumer, etc.
   
3. Geographic Diversification:
   - Domestic and international investments
   
4. Size Diversification:
   - Large-cap, mid-cap, small-cap companies

Diversification Strategies:
- Index Funds: Own many companies at once
- ETFs: Low-cost, diversified portfolios
- Asset Allocation: Balance stocks/bonds by age
- Rebalancing: Maintain target allocation

Common Mistakes:
✗ Diversifying too much (over-diversification)
✗ Not rebalancing regularly
✗ Trying to time the market
✗ Following fads or tips""",
        "source": "Portfolio Management Guide",
        "tags": ["diversification", "portfolio", "risk-management"]
    },
    {
        "id": "asset_allocation",
        "title": "Asset Allocation by Age and Risk Tolerance",
        "category": "portfolio",
        "content": """Asset allocation is how you divide investments among stocks, bonds, and cash based on your situation.

Age-Based Guidelines:
Age 20-30: 80-90% stocks, 10-20% bonds (high growth tolerance)
Age 30-40: 70-80% stocks, 20-30% bonds
Age 40-50: 60-70% stocks, 30-40% bonds
Age 50-60: 50-60% stocks, 40-50% bonds
Age 60+: 40-50% stocks, 50-60% bonds (income focus)

Risk Tolerance Considerations:
Conservative: 30-40% stocks, 60-70% bonds
Moderate: 50-60% stocks, 40-50% bonds
Aggressive: 80-90% stocks, 10-20% bonds

Factors Affecting Allocation:
- Time horizon
- Risk tolerance
- Income needs
- Health and longevity
- Major expenses (home, education)
- Income stability
- Existing assets

Rebalancing:
- Review allocation annually
- Rebalance when allocation drifts 5-10%
- Sell winners, buy underperformers
- Tax-efficient rebalancing""",
        "source": "Investment Strategy Guide",
        "tags": ["asset-allocation", "portfolio", "retirement"]
    },
    {
        "id": "401k_ira_guide",
        "title": "Tax-Advantaged Accounts: 401(k) and IRA",
        "category": "tax",
        "content": """Tax-advantaged accounts help you save for retirement with tax benefits.

401(k) Plans:
- Employer-sponsored retirement plan
- 2024 contribution limit: $23,500 ($31,000 if 50+)
- Pretax or Roth options
- Employer may match contributions
- Required distributions at 73

Traditional IRA:
- Individual retirement account
- 2024 contribution limit: $7,000 ($8,000 if 50+)
- Contributions may be tax-deductible
- Growth is tax-deferred
- Distributions taxed as income
- Required distributions at 73

Roth IRA:
- Contributions not tax-deductible
- Growth is tax-free
- Qualified distributions are tax-free
- No required distributions
- Can withdraw contributions anytime
- Income limits apply

Comparison:
401(k): Employer plan, higher limits, forced distributions
Traditional IRA: Individual, tax-deferred, income-limited deduction
Roth IRA: Individual, tax-free growth, no forced distributions

Key Advantages:
✓ Tax savings now or later
✓ Employer matching (401k)
✓ Lower taxes on distributions
✓ Long-term wealth building""",
        "source": "Tax Planning Guide",
        "tags": ["retirement", "tax-advantaged", "401k", "ira"]
    },
    {
        "id": "dollar_cost_averaging",
        "title": "Dollar-Cost Averaging: Invest Regularly",
        "category": "investing-strategies",
        "content": """Dollar-cost averaging (DCA) means investing a fixed amount regularly regardless of market conditions.

How It Works:
- Invest same amount every month/quarter
- Buy more shares when prices are low
- Buy fewer shares when prices are high
- Reduces impact of market timing
- Removes emotion from investing

Benefits:
✓ Reduces timing risk
✓ Builds discipline
✓ Lower average cost per share
✓ Works with any budget
✓ Simple to implement

Example:
Market Down: Invest $500, buy more shares
Market Up: Invest $500, buy fewer shares
Result: Lower average cost than lump sum

When to Use DCA:
- Regular investment from paychecks
- Contributing to retirement accounts
- Building wealth over time
- Uncertain market conditions

DCA vs. Lump Sum:
DCA: Safer, steadier approach
Lump Sum: May perform better in rising markets
Best: DCA for most investors""",
        "source": "Investment Strategies",
        "tags": ["investing", "strategy", "discipline"]
    },
    {
        "id": "index_funds",
        "title": "Index Funds: Low-Cost Diversified Investing",
        "category": "investing-products",
        "content": """Index funds track a market index like the S&P 500, providing instant diversification.

What is an Index Fund:
- Owns all or representative sample of index
- Passive management (no active trading)
- Low fees (typically 0.03-0.20% annually)
- Predictable, transparent holdings

Popular Indices:
- S&P 500: 500 largest U.S. companies
- Nasdaq-100: Tech-heavy index
- Total Market: All publicly traded U.S. stocks
- International indices: Global diversification
- Bond indices: Fixed income exposure

Why Index Funds Win:
✓ Outperform 80% of active managers long-term
✓ Low costs = higher returns
✓ Instant diversification
✓ Transparent
✓ Tax-efficient
✓ Easy to understand

Drawbacks:
✗ Market returns (not beating market)
✗ No downside protection
✗ Concentration in large companies
✗ Limited flexibility

Getting Started:
1. Choose index fund family
2. Select appropriate indices
3. Set allocation percentage
4. Set up automatic investing
5. Rebalance annually""",
        "source": "Investment Products Guide",
        "tags": ["index-funds", "mutual-funds", "etfs"]
    },
    {
        "id": "emergency_fund",
        "title": "Building an Emergency Fund",
        "category": "financial-planning",
        "content": """An emergency fund is savings for unexpected expenses, kept in accessible accounts.

Why Emergency Funds Matter:
- Prevents taking on debt
- Covers job loss, medical bills, car repairs
- Provides peace of mind
- Enables long-term investing
- Reduces financial stress

How Much to Save:
3-6 months of essential expenses
- Tight budget: 3 months
- Variable income: 6-9 months
- Conservative approach: 6-12 months

Where to Keep Emergency Funds:
✓ High-yield savings account
✓ Money market account
✓ Short-term CDs
✗ Stock market (too risky)
✗ Under mattress (no returns)

Building Your Fund:
1. Start with $1,000 for immediate emergencies
2. Build to 1-2 months expenses
3. Build to full 3-6 months target
4. Replenish after use

Emergency Fund vs. Investing:
1. Build emergency fund first
2. Then start investing
3. Keep separate accounts
4. Don't tap for non-emergencies

Emergency Expenses:
- Medical bills
- Job loss/income interruption
- Major home/car repairs
- Unexpected travel
- Pet emergencies""",
        "source": "Personal Finance Guide",
        "tags": ["savings", "emergency-fund", "planning"]
    },
    {
        "id": "compound_interest",
        "title": "The Power of Compound Interest: Time Your Greatest Asset",
        "category": "fundamentals",
        "content": """Compound interest is interest earned on interest, creating exponential wealth growth over time.

How Compound Interest Works:
Year 1: $1,000 invested at 7% = $70 interest
Year 2: $1,070 at 7% = $74.90 interest (earning interest on interest!)
Year 3: $1,144.90 at 7% = $80.14 interest
Result: Money grows faster over time

Time Impact (Starting with $10,000 at 7%):
10 years: $19,672
20 years: $38,697
30 years: $76,123
40 years: $149,745
50 years: $294,204

Key Factors:
1. Principal: Starting amount
2. Interest Rate: Annual return
3. Time: Years until withdrawal
4. Frequency: How often interest compounds

Maximizing Compound Interest:
✓ Start early (even small amounts compound)
✓ Add regularly (dollar-cost averaging)
✓ Minimize taxes (retirement accounts)
✓ Keep costs low (low-fee funds)
✓ Don't withdraw early
✓ Be patient

Starting Early Example:
At 25: Invest $5,000/year until 65
At 35: Invest $5,000/year until 65
Difference: $300,000+ more by age 65!

Key Takeaway:
Time is your most valuable asset. Start investing early, even with small amounts.""",
        "source": "Wealth Building Guide",
        "tags": ["compound-interest", "investing", "time-value"]
    },
    {
        "id": "risk_vs_return",
        "title": "Understanding Risk vs. Return",
        "category": "investing-principles",
        "content": """Higher potential returns come with higher risk. Understanding this relationship is crucial for investing.

Risk-Return Relationship:
- Bonds: Low risk, low return
- Balanced Portfolio: Medium risk, medium return
- Stocks: High risk, high return
- Individual Stocks: Very high risk, variable return

Types of Risk:
1. Market Risk: Overall market declines affect all stocks
2. Company Risk: Individual company problems
3. Sector Risk: Entire industry decline
4. Interest Rate Risk: Bond prices fall when rates rise
5. Inflation Risk: Returns don't keep pace with inflation
6. Liquidity Risk: Hard to sell quickly without loss

Risk Tolerance Assessment:
Ask yourself:
- How would I feel seeing 20% portfolio decline?
- How long until I need the money?
- How much can I afford to lose?
- Can I stay invested during downturns?

Risk Reduction Strategies:
✓ Diversification
✓ Asset allocation
✓ Regular rebalancing
✓ Long-term horizon
✓ Dollar-cost averaging
✓ Emergency fund

Risk Management Rules:
1. Only invest money you won't need for 5+ years
2. Don't invest money needed soon
3. Diversify across assets and sectors
4. Accept inflation as a real risk
5. Don't try to avoid all risk (leads to low returns)""",
        "source": "Risk Management Guide",
        "tags": ["risk", "return", "investing-principles"]
    },
    {
        "id": "tax_loss_harvesting",
        "title": "Tax-Loss Harvesting: Turn Losses into Savings",
        "category": "tax",
        "content": """Tax-loss harvesting is selling losing investments to offset capital gains and reduce taxes.

How Tax-Loss Harvesting Works:
1. Identify losing positions
2. Sell at a loss
3. Use loss to offset capital gains
4. Reduce your tax bill
5. Reinvest proceeds

Capital Gains Rules:
- Long-term gains (held 1+ year): Lower tax rates
- Short-term gains: Taxed as ordinary income
- Losses offset gains dollar-for-dollar
- Excess losses ($3,000) can offset ordinary income

Tax-Loss Harvesting Process:
Step 1: Review portfolio for losses
Step 2: Sell positions with realized losses
Step 3: Calculate total losses
Step 4: Offset capital gains
Step 5: Reduce income by excess losses (up to $3,000)
Step 6: Reinvest to maintain target allocation

Wash Sale Rules:
- Can't buy same/similar security within 30 days
- Before or after the sale
- Violating rule disallows loss deduction
- Solution: Buy slightly different security temporarily

Tax-Loss Harvesting Mistakes:
✗ Not tracking basis (purchase price)
✗ Forgetting wash-sale window
✗ Harvesting in retirement accounts
✗ Over-trading (generating short-term gains)
✗ Not maintaining diversification

Best Practices:
✓ Document all trades carefully
✓ Use tax-loss harvesting software
✓ Harvest quarterly or year-end
✓ Maintain target allocation
✓ Consider holding periods carefully""",
        "source": "Tax Strategy Guide",
        "tags": ["taxes", "tax-loss-harvesting", "capital-gains"]
    },
    {
        "id": "inflation_protection",
        "title": "Inflation: Why Your Investments Need to Outpace It",
        "category": "economic-concepts",
        "content": """Inflation erodes purchasing power. Your investments must earn enough to beat inflation.

Understanding Inflation:
- Inflation: General increase in prices over time
- Average U.S. inflation: 3% annually
- Your cash: Loses 3% purchasing power yearly
- You need returns > inflation to build wealth

Real vs. Nominal Returns:
Nominal Return: Stated percentage gain
Real Return: Gain after inflation
Example: 5% return with 3% inflation = 2% real return

Inflation Impact Over Time:
$100 today with 3% inflation:
- In 10 years: Buying power = $74
- In 20 years: Buying power = $55
- In 30 years: Buying power = $41
- In 40 years: Buying power = $31

Inflation-Protected Investments:
- Stocks: Historically beat inflation (average 10%)
- TIPS: Treasury Inflation-Protected Securities
- Real Estate: Appreciates with inflation
- Commodities: Often rise with inflation
- I Bonds: Series I Savings Bonds (inflation-adjusted)

Common Mistakes:
✗ Keeping all money in savings account
✗ Assuming fixed returns match inflation
✗ Not adjusting for inflation in planning
✗ Ignoring long-term inflation impact

Inflation Strategy:
1. Understand inflation impact on goals
2. Invest for growth (stocks)
3. Maintain diversification
4. Consider inflation-protected securities
5. Review and rebalance regularly""",
        "source": "Economic Concepts Guide",
        "tags": ["inflation", "economic", "investing"]
    }
]

def create_knowledge_base():
    """Create knowledge base JSON files"""
    kb_path = Path(__file__).parent / "knowledge_base"
    kb_path.mkdir(parents=True, exist_ok=True)
    
    # Save articles grouped by category
    articles_by_category = {}
    for article in KNOWLEDGE_BASE_ARTICLES:
        category = article['category']
        if category not in articles_by_category:
            articles_by_category[category] = []
        articles_by_category[category].append(article)
    
    # Save each category as separate JSON file
    for category, articles in articles_by_category.items():
        file_path = kb_path / f"{category}.json"
        with open(file_path, 'w') as f:
            json.dump(articles, f, indent=2)
    
    print(f"Knowledge base created with {len(KNOWLEDGE_BASE_ARTICLES)} articles")

if __name__ == "__main__":
    create_knowledge_base()
