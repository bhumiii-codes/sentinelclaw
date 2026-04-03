import json
import os
from datetime import datetime
from core.logger import log_decision

POLICY_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'policy.json')

INJECTION_KEYWORDS = [
    "ignore", "bypass", "override", "forget", "disregard",
    "ignore all", "ignore previous", "sell everything",
    "unlimited", "no limit", "remove limit", "hack",
    "jailbreak", "as an ai", "pretend", "simulate no rules"
]

THREAT_LEVELS = {
    "ticker_not_allowed": "MEDIUM",
    "exceeds_max_value": "MEDIUM",
    "short_selling": "HIGH",
    "outside_trading_hours": "LOW",
    "exceeds_max_quantity": "MEDIUM",
    "prompt_injection": "CRITICAL",
    "invalid_action": "HIGH",
    "daily_trade_limit": "HIGH"
}

def load_policy():
    with open(POLICY_PATH, 'r') as f:
        return json.load(f)

def detect_injection(text):
    text_lower = text.lower()
    for keyword in INJECTION_KEYWORDS:
        if keyword in text_lower:
            return True, keyword
    return False, None

def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M")

def enforce(action, ticker, quantity, price_per_unit, instruction=None):
    policy = load_policy()  # hot-reload every time
    
    total_value = quantity * price_per_unit
    current_time = get_current_time()
    
    # Check prompt injection first
    if instruction:
        injected, keyword = detect_injection(instruction)
        if injected:
            threat = THREAT_LEVELS["prompt_injection"]
            reason = f"PROMPT INJECTION detected — keyword: '{keyword}'"
            log_decision(action, ticker, quantity, total_value, "BLOCKED", reason)
            print_threat(threat)
            return False, reason

    # Check valid action
    if action not in policy["allowed_actions"]:
        threat = THREAT_LEVELS["invalid_action"]
        reason = f"Action '{action}' is not permitted by policy"
        log_decision(action, ticker, quantity, total_value, "BLOCKED", reason)
        print_threat(threat)
        return False, reason

    # Check ticker
    if ticker not in policy["allowed_tickers"]:
        threat = THREAT_LEVELS["ticker_not_allowed"]
        reason = f"Ticker '{ticker}' is not in allowed list: {policy['allowed_tickers']}"
        log_decision(action, ticker, quantity, total_value, "BLOCKED", reason)
        print_threat(threat)
        return False, reason

    # Check trade value
    if total_value > policy["max_trade_value"]:
        threat = THREAT_LEVELS["exceeds_max_value"]
        reason = f"Trade value ${total_value:.2f} exceeds max allowed ${policy['max_trade_value']}"
        log_decision(action, ticker, quantity, total_value, "BLOCKED", reason)
        print_threat(threat)
        return False, reason

    # Check quantity
    if quantity > policy["max_quantity"]:
        threat = THREAT_LEVELS["exceeds_max_quantity"]
        reason = f"Quantity {quantity} exceeds max allowed {policy['max_quantity']}"
        log_decision(action, ticker, quantity, total_value, "BLOCKED", reason)
        print_threat(threat)
        return False, reason

    # Check short selling
    if action == "sell" and not policy["allow_short_selling"]:
        threat = THREAT_LEVELS["short_selling"]
        reason = "Short selling is not permitted by policy"
        log_decision(action, ticker, quantity, total_value, "BLOCKED", reason)
        print_threat(threat)
        return False, reason

    # Check trading hours
    start = policy["trading_hours_start"]
    end = policy["trading_hours_end"]
    if not (start <= current_time <= end):
        threat = THREAT_LEVELS["outside_trading_hours"]
        reason = f"Trade attempted at {current_time} — outside allowed hours ({start}–{end})"
        log_decision(action, ticker, quantity, total_value, "BLOCKED", reason)
        print_threat(threat)
        return False, reason

    # All checks passed
    reason = "All policy constraints satisfied"
    log_decision(action, ticker, quantity, total_value, "ALLOWED", reason)
    return True, reason

def print_threat(level):
    colors = {
        "LOW":      "\033[93m",   # yellow
        "MEDIUM":   "\033[33m",   # orange
        "HIGH":     "\033[91m",   # red
        "CRITICAL": "\033[95m",   # magenta
    }
    reset = "\033[0m"
    color = colors.get(level, "")
    print(f"         ⚠️  Threat Level: {color}{level}{reset}")
    