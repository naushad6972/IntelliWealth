import re
import logging
from typing import Tuple, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

logger = logging.getLogger(__name__)

# Heuristic Rules & Keyword Map
CATEGORY_KEYWORD_MAP: Dict[str, list] = {
    "Food": ["swiggy", "zomato", "restaurant", "cafe", "starbucks", "mcdonalds", "kfc", "dominos", "pizza", "burger", "coffee", "baking", "supermarket", "grocery", "dmart", "blinkit", "zepto", "bigbasket"],
    "Travel": ["uber", "ola", "rapido", "flight", "indigo", "airindia", "irctc", "railway", "bus", "redbus", "metro", "cab", "taxi", "toll", "fastag"],
    "Shopping": ["amazon", "flipkart", "myntra", "zara", "h&m", "nike", "adidas", "shopping", "apparel", "clothing", "electronics", "croma", "reliancedigital"],
    "Bills": ["electricity", "power", "water", "broadband", "jio", "airtel", "vi", "recharge", "utility", "gas", "bill", "postpaid"],
    "Healthcare": ["apollo", "pharmacy", "netmeds", "pharmeasy", "hospital", "clinic", "doctor", "lab", "pathology", "medicine"],
    "Entertainment": ["netflix", "prime", "spotify", "bookmyshow", "hotstar", "cinema", "movie", "gaming", "steam", "playstation"],
    "Education": ["udemy", "coursera", "school", "college", "tuition", "coaching", "books", "course", "skillshare"],
    "Salary": ["salary", "payroll", "stipend", "acme corp", "remuneration", "dividend", "income credit"],
    "Investment": ["zerodha", "groww", "upstox", "mutual fund", "sip", "stocks", "etf", "nps", "ppf", "fd", "lic"],
    "Rent": ["rent", "landlord", "housing", "society maintenance", "apartment"],
    "Fuel": ["hpcl", "bpcl", "iocl", "petrol", "diesel", "fuel", "shell"],
    "Insurance": ["insurance", "lic", "hdfc ergo", "max bupa", "policy", "premium"]
}

class TransactionCategorizer:
    def __init__(self):
        self._init_ml_model()

    def _init_ml_model(self):
        """Train lightweight Naive Bayes + TF-IDF model on synthetic corpus"""
        training_texts = []
        training_labels = []

        for category, keywords in CATEGORY_KEYWORD_MAP.items():
            for kw in keywords:
                # Add variations for better feature learning
                training_texts.extend([
                    f"UPI/{kw.upper()}/PAYMENT",
                    f"CARD TXN AT {kw.upper()}",
                    f"POS {kw} ONLINE STORE",
                    kw,
                    f"PURCHASE AT {kw} OUTLET"
                ])
                training_labels.extend([category] * 5)

        self.vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1, 2))
        X = self.vectorizer.fit_transform(training_texts)
        self.clf = MultinomialNB()
        self.clf.fit(X, training_labels)

    def categorize(self, merchant: str, raw_description: str = "", amount: float = 0.0) -> Tuple[str, float, str]:
        text = f"{merchant} {raw_description}".lower()

        # 1. Rule-Based Exact Keyword Search (High Precision, Confidence = 0.95 - 1.0)
        for category, keywords in CATEGORY_KEYWORD_MAP.items():
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', text) or kw in text:
                    return category, 0.95, "RULE"

        # 2. Machine Learning Naive Bayes Classifier (Confidence = 0.7 - 0.9)
        try:
            vec = self.vectorizer.transform([text])
            probs = self.clf.predict_proba(vec)[0]
            max_idx = np.argmax(probs)
            top_category = self.clf.classes_[max_idx]
            confidence = float(probs[max_idx])

            if confidence >= 0.35:
                return top_category, round(confidence, 2), "ML"
        except Exception as e:
            logger.warning(f"ML Categorizer fallback exception: {e}")

        # 3. Heuristic / Default Fallback
        if amount < 0:
            return "Salary", 0.7, "RULE"

        return "Miscellaneous", 0.5, "FALLBACK"

categorizer_engine = TransactionCategorizer()
