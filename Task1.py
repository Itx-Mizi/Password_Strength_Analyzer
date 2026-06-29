import sys
import re
import argparse
import getpass
from typing import Dict

# Common passwords list
COMMON_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234",
    "111111", "1234567", "sunshine", "qwertyuiop", "letmein", "trustno1",
    "000000", "password1", "admin", "welcome", "monkey", "abc123", "football",
    "123123", "master", "hello", "freedom", "whatever", "dragon", "baseball",
    "superman", "batman", "iloveyou", "princess", "ninja", "1234567890",
    "starwars", "computer", "password123", "shadow", "secret", "qazwsx",
    "michael", "jesus", "soccer", "harley", "buster", "thomas", "tigger",
    "charlie", "robert", "samuel", "andrew", "daniel", "jordan", "hunter",
    "jessica", "ginger", "butter"
}

def check_common_passwords(password: str) -> bool:
    return password.lower() in {p.lower() for p in COMMON_PASSWORDS}

def calculate_strength(password: str) -> Dict:
    length = len(password)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]', password))
    
    patterns = {
        'sequential': bool(re.search(r'(0123456789|1234567890|qwertyuiop|asdfghjkl|zxcvbnm)', password.lower())),
        'repeating': bool(re.search(r'(.)\1{2,}', password)),
        'keyboard': bool(re.search(r'(qwert|asdfg|zxcvb|poiuytrewq|lkjhgfdsa|mnbvcxz)', password.lower())),
        'date_like': bool(re.search(r'\d{4}', password))
    }
    
    score = 0
    feedback = []
    
    # Length
    if length < 8:
        score -= 20
        feedback.append("❌ Password is too short. Use at least 12-16 characters.")
    elif length < 12:
        score += 10
        feedback.append("⚠ Good length, but aim for 16+.")
    else:
        score += 30
        feedback.append("✅ Excellent length!")
    
    # Complexity
    complexity = sum([has_lower, has_upper, has_digit, has_special])
    if complexity == 4:
        score += 50
        feedback.append("✅ Great character variety!")
    elif complexity == 3:
        score += 40
        feedback.append("⚠ Strong complexity, add one more type.")
    else:
        score += (complexity * 15)
        feedback.append("❌ Add more character types (upper, lower, numbers, symbols).")
    
    # Penalties
    if patterns['sequential']:
        score -= 30
        feedback.append("❌ Avoid sequential characters like '123' or 'qwerty'.")
    if patterns['repeating']:
        score -= 20
        feedback.append("❌ Avoid repeating characters like 'aaa'.")
    if patterns['keyboard']:
        score -= 25
        feedback.append("❌ Avoid keyboard patterns.")
    if patterns['date_like']:
        score -= 15
        feedback.append("❌ Avoid years or date patterns.")
    if check_common_passwords(password):
        score -= 50
        feedback.append("❌ This is a very common password! Change it immediately.")
    
    score = max(0, min(100, score))
    
    if score >= 80:
        strength = "Very Strong"
        color = "\033[92m"
    elif score >= 60:
        strength = "Strong"
        color = "\033[92m"
    elif score >= 40:
        strength = "Medium"
        color = "\033[93m"
    elif score >= 20:
        strength = "Weak"
        color = "\033[91m"
    else:
        strength = "Very Weak"
        color = "\033[91m"
    
    return {
        "score": score,
        "strength": strength,
        "color": color,
        "feedback": feedback,
        "metrics": {"length": length, "lower": has_lower, "upper": has_upper, "digit": has_digit, "special": has_special}
    }

def print_report(password, result):
    print("\n" + "="*60)
    print("🔐 PASSWORD STRENGTH ANALYSIS")
    print("="*60)
    print(f"Password : {'*' * len(password)}")
    print(f"Strength : {result['color']}{result['strength']}\033[0m ({result['score']}/100)")
    print("\n📊 METRICS:")
    m = result['metrics']
    print(f"   Length   : {m['length']} chars")
    print(f"   Lower    : {'✅' if m['lower'] else '❌'}")
    print(f"   Upper    : {'✅' if m['upper'] else '❌'}")
    print(f"   Numbers  : {'✅' if m['digit'] else '❌'}")
    print(f"   Special  : {'✅' if m['special'] else '❌'}")
    
    print("\n💡 FEEDBACK:")
    for fb in result['feedback']:
        print(f"   • {fb}")
    print("="*60)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", help="Password to check")
    parser.add_argument("--hide", action="store_true", help="Hide password input")
    args = parser.parse_args()
    
    if args.password:
        pwd = args.password
    elif args.hide:
        pwd = getpass.getpass("Enter password: ")
    else:
        pwd = input("Enter password: ")
    
    if not pwd:
        print("❌ Password cannot be empty!")
        sys.exit(1)
    
    result = calculate_strength(pwd)
    print_report(pwd, result)

if __name__ == "__main__":
    main()
