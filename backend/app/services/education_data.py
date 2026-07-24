from typing import Dict, Any, List

INVESTMENT_TOPICS: Dict[str, Dict[str, Any]] = {
    "sip": {
        "topic_id": "sip",
        "title": "Systematic Investment Plan (SIP)",
        "definition": "A Systematic Investment Plan (SIP) is an investment vehicle offered by mutual funds that allows individuals to invest a fixed amount regularly (monthly or quarterly) into a chosen mutual fund scheme.",
        "benefits": [
            "Rupee Cost Averaging lowers average cost per unit during market dips.",
            "Disciplined and automated monthly investing habit.",
            "Compounding interest growth over long-term horizons.",
            "Flexible investment amounts starting as low as ₹500/month."
        ],
        "risks": [
            "Subject to equity market volatility and short-term price fluctuations.",
            "No guaranteed fixed returns; returns depend on underlying fund performance."
        ],
        "examples": [
            "Investing ₹5,000 every month on the 5th into Nifty 50 Index Fund for 10 years."
        ],
        "beginner_tips": [
            "Start early to maximize the power of compounding.",
            "Automate SIP debits on your salary date.",
            "Step up your SIP amount annually by 10% as your income grows."
        ],
        "learning_resources": [
            {"title": "SEBI Investor Education Portal", "url": "https://investor.sebi.gov.in"},
            {"title": "AMFI Guide to SIP", "url": "https://www.amfiindia.com"}
        ],
        "faqs": [
            {"q": "Can I stop or pause a SIP at any time?", "a": "Yes, SIPs offer complete flexibility without penalties for pausing or cancelling."},
            {"q": "What is the ideal tenure for an equity SIP?", "a": "Minimum 5 to 7 years to smooth out short-term market cycles."}
        ]
    },
    "mutual_funds": {
        "topic_id": "mutual_funds",
        "title": "Mutual Funds",
        "definition": "A mutual fund pools money from multiple investors to purchase a diversified portfolio of stocks, bonds, or money market instruments managed by professional Asset Management Companies (AMCs).",
        "benefits": [
            "Instant diversification across dozens of companies.",
            "Professional portfolio management by experienced fund managers.",
            "High liquidity compared to real estate or physical gold."
        ],
        "risks": [
            "Market risk, credit risk (for debt funds), and expense ratio costs."
        ],
        "examples": [
            "Investing in a Large Cap Equity Mutual Fund tracking top 100 blue-chip companies."
        ],
        "beginner_tips": [
            "Prefer Direct Plan Growth options over Regular plans to save on commissions.",
            "Choose low expense ratio passive Index Funds for core holdings."
        ],
        "learning_resources": [
            {"title": "AMFI India Mutual Fund Basics", "url": "https://www.amfiindia.com"}
        ],
        "faqs": [
            {"q": "What is the difference between Direct and Regular plans?", "a": "Direct plans have lower expense ratios because no distributor commissions are deducted."}
        ]
    },
    "stocks": {
        "topic_id": "stocks",
        "title": "Direct Stocks & Equities",
        "definition": "Shares representing fractional ownership in a publicly traded corporation listed on stock exchanges (e.g. NSE, BSE).",
        "benefits": [
            "Potential for high capital appreciation and dividend payouts.",
            "Direct voting rights and ownership stake in top companies."
        ],
        "risks": [
            "High volatility, individual company risk, and potential capital loss if unhedged."
        ],
        "examples": [
            "Buying shares of fundamental blue-chip companies in banking, IT, or consumer goods."
        ],
        "beginner_tips": [
            "Conduct fundamental analysis before buying individual stocks.",
            "Never invest emergency funds or borrowed capital into direct equities."
        ],
        "learning_resources": [
            {"title": "NSE India Educational Modules", "url": "https://www.nseindia.com"}
        ],
        "faqs": [
            {"q": "Should beginners start with stocks or mutual funds?", "a": "Beginners are advised to build a core portfolio with Index Mutual Funds before picking individual stocks."}
        ]
    },
    "etfs": {
        "topic_id": "etfs",
        "title": "Exchange Traded Funds (ETFs)",
        "definition": "ETFs are marketable securities that track an index, commodity, or sector basket and trade on stock exchanges like regular shares.",
        "benefits": [
            "Ultra-low expense ratios (often < 0.10%).",
            "Real-time intraday trading liquidity on stock exchanges."
        ],
        "risks": [
            "Tracking error relative to benchmark index and market liquidity risk."
        ],
        "examples": [
            "Nifty 50 ETF, Nifty Bank ETF, or Gold ETF."
        ],
        "beginner_tips": [
            "Use ETFs to gain low-cost passive exposure to market indices."
        ],
        "learning_resources": [
            {"title": "NSE ETF Education Hub", "url": "https://www.nseindia.com"}
        ],
        "faqs": [
            {"q": "Do I need a Demat account to buy ETFs?", "a": "Yes, ETFs are bought and sold via stock exchange Demat & Trading accounts."}
        ]
    },
    "bonds": {
        "topic_id": "bonds",
        "title": "Fixed Income & Bonds",
        "definition": "Bonds are fixed income instruments issued by governments or corporations to raise capital, paying periodic coupon interest.",
        "benefits": [
            "Predictable, fixed income coupon payments.",
            "Lower volatility and capital preservation compared to equity."
        ],
        "risks": [
            "Interest rate risk, inflation risk, and corporate credit default risk."
        ],
        "examples": [
            "RBI Floating Rate Savings Bonds, Government Securities (G-Secs), Corporate AAA Bonds."
        ],
        "beginner_tips": [
            "Match bond maturities with your short-to-medium term financial goals."
        ],
        "learning_resources": [
            {"title": "RBI Retail Direct Portal", "url": "https://rbiretaildirect.org.in"}
        ],
        "faqs": [
            {"q": "How do interest rate hikes affect existing bond prices?", "a": "When interest rates rise, existing fixed bond prices fall, and vice versa."}
        ]
    },
    "emergency_fund": {
        "topic_id": "emergency_fund",
        "title": "Emergency Fund Building",
        "definition": "A dedicated liquid cash reserve covering 3 to 6 months of mandatory living expenses reserved for unexpected crises.",
        "benefits": [
            "Financial safety net preventing debt traps or distress asset sales."
        ],
        "risks": [
            "Low yield compared to equity investments."
        ],
        "examples": [
            "Keeping 3 months of expenses in a High Yield Savings Account + 3 months in Liquid Mutual Funds."
        ],
        "beginner_tips": [
            "Build your emergency fund FIRST before starting high-risk equity investments."
        ],
        "learning_resources": [
            {"title": "Financial Planning Standards Board", "url": "https://fpsb.org"}
        ],
        "faqs": [
            {"q": "Where should an emergency fund be stored?", "a": "In highly liquid, capital-safe accounts: high-yield savings accounts or liquid debt mutual funds."}
        ]
    }
}
