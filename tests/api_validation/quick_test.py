#!/usr/bin/env python3
"""
Quick API Validation - Test only the working APIs for rapid feedback
"""
import os

import requests


def load_api_keys():
    """Load API keys from ~/vars/"""
    env_file = os.path.expanduser("~/vars/enrich-ddf-api-keys.env")
    env_vars = {}

    try:
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"❌ {env_file} not found")
        return {}

    return env_vars


def test_working_apis():
    """Test only the 4 working APIs"""
    api_keys = load_api_keys()
    if not api_keys:
        return False

    print("🚀 Quick API Validation - Working APIs Only")
    print("=" * 50)

    # Test GitHub
    if "GITHUB_TOKEN" in api_keys:
        try:
            response = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"token {api_keys['GITHUB_TOKEN']}"},
                timeout=5,
            )
            print(f"✅ GitHub: {response.status_code == 200}")
        except:
            print("❌ GitHub: Connection failed")

    # Test Hunter.io
    if "HUNTER_API_KEY" in api_keys:
        try:
            response = requests.get(
                f"https://api.hunter.io/v2/account?api_key={api_keys['HUNTER_API_KEY']}",
                timeout=5,
            )
            print(f"✅ Hunter.io: {response.status_code == 200}")
        except:
            print("❌ Hunter.io: Connection failed")

    # Test ZeroBounce
    if "ZEROBOUNCE_API_KEY" in api_keys:
        try:
            response = requests.get(
                f"https://api.zerobounce.net/v2/getcredits?api_key={api_keys['ZEROBOUNCE_API_KEY']}",
                timeout=5,
            )
            print(f"✅ ZeroBounce: {response.status_code == 200}")
        except:
            print("❌ ZeroBounce: Connection failed")

    # Test Apollo.io
    if "APOLLO_API_KEY" in api_keys:
        try:
            response = requests.get(
                "https://api.apollo.io/v1/email_accounts",
                headers={"X-Api-Key": api_keys["APOLLO_API_KEY"]},
                timeout=5,
            )
            print(f"✅ Apollo.io: {response.status_code == 200}")
        except:
            print("❌ Apollo.io: Connection failed")

    print("\n🎯 Quick validation complete!")
    return True


if __name__ == "__main__":
    test_working_apis()
