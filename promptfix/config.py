import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-pro"

INTERACTIVE_THRESHOLD = 0.8
LOW_CONFIDENCE_THRESHOLD = 0.5

CATEGORIES = {
    "自指悖论": "self_referential_paradox",
    "超现实目标": "surreal_goal",
    "不可判定": "undecidable",
    "无限递归": "infinite_recursion",
    "极端模糊": "extreme_ambiguity",
    "有解": "solvable"
}

SEVERITY_COLORS = {
    "low": "\033[94m",    # blue
    "medium": "\033[93m", # yellow
    "high": "\033[91m",   # red
    "safe": "\033[92m"    # green
}

STATUS_COLORS = {
    "safe": "\033[92m",       # green
    "unsolvable_detected": "\033[91m",  # red
    "ambiguous": "\033[93m"   # yellow
}