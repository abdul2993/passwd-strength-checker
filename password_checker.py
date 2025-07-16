#!/usr/bin/env python3
import math
import os

COMMON_PASSWORDS_FILE = "common_passwords.txt"
PREVIOUS_PASSWORDS_FILE = "used_passwords.txt"

def print_banner():
    banner = r"""
\033[1m
    █████╗ ██╗  ██╗      ███████╗███████╗
   ██╔══██╗╚██╗██╔╝      ██╔════╝██╔════╝
   ███████║ ╚███╔╝ █████╗█████╗  █████╗  
   ██╔══██║ ██╔██╗ ╚════╝██╔══╝  ██╔══╝  
   ██║  ██║██╔╝ ██╗      ██║     ██║     
   ╚═╝  ╚═╝╚═╝  ╚═╝      ╚═╝     ╚═╝     
     AKJ's PASSWD CHECKER
\033[0m
    """
    print(banner)

def load_common_passwords():
    if not os.path.exists(COMMON_PASSWORDS_FILE):
        return {"password", "123456", "123456789", "qwerty", "abc123", "admin"}
    with open(COMMON_PASSWORDS_FILE, "r") as file:
        return set(line.strip().lower() for line in file)

def load_previous_passwords():
    if os.path.exists(PREVIOUS_PASSWORDS_FILE):
        with open(PREVIOUS_PASSWORDS_FILE, "r") as file:
            return [line.strip() for line in file]
    return []

def save_password(password):
    with open(PREVIOUS_PASSWORDS_FILE, "a") as file:
        file.write(password + "\n")

def calculate_entropy(password):
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() for c in password): pool += 32
    if pool == 0:
        return 0
    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)

def check_strength(entropy):
    if entropy >= 80:
        return "Very Strong"
    elif entropy >= 60:
        return "Strong"
    elif entropy >= 40:
        return "Moderate"
    elif entropy >= 20:
        return "Weak"
    else:
        return "Very Weak"

def main():
    print_banner()
    print("🔐 Password Strength Checker CLI Tool")
    print("======================================\n")

    common_passwords = load_common_passwords()
    previous_passwords = load_previous_passwords()

    password = input("Enter a password to check: ").strip()

    if password.lower() in common_passwords:
        print("❌ This password is too common!")
    elif any(password in old or old in password for old in previous_passwords):
        print("⚠️ This password is similar to a previously used one!")
    else:
        entropy = calculate_entropy(password)
        strength = check_strength(entropy)
        print(f"\n✅ Entropy: {entropy} bits")
        print(f"🔒 Strength: {strength}")

        if len(password) >= 8 and strength != "Very Weak":
            save_password(password)
            print("📁 Password saved (not reused).\n")
        else:
            print("❗ Password too short or weak. Not saved.\n")

if __name__ == "__main__":
    main()
