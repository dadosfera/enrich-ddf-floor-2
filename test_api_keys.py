#!/usr/bin/env python3
"""
API Key Testing Script - Test all configured data enrichment APIs
"""
import os
import requests
import time
from typing import Dict, List, Tuple

# Load environment variables from ~/vars/
def load_api_keys():
    """Load API keys from ~/vars/enrich-ddf-api-keys.env"""
    env_file = os.path.expanduser("~/vars/enrich-ddf-api-keys.env")
    env_vars = {}
    
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"❌ Environment file not found: {env_file}")
        return {}
    
    return env_vars

def test_hunter_io(api_key: str) -> Tuple[bool, str]:
    """Test Hunter.io API"""
    if api_key == "your_hunter_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    url = "https://api.hunter.io/v2/account"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            calls_used = data.get('data', {}).get('calls', {}).get('used', 0)
            calls_available = data.get('data', {}).get('calls', {}).get('available', 0)
            return True, f"✅ Hunter.io: {calls_used}/{calls_available} calls used"
        else:
            return False, f"❌ Hunter.io: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Hunter.io: {str(e)}"

def test_github(token: str) -> Tuple[bool, str]:
    """Test GitHub API"""
    if token == "your_github_token_here":
        return False, "❌ Placeholder token - needs configuration"
    
    url = "https://api.github.com/user"
    headers = {"Authorization": f"token {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            username = data.get('login', 'unknown')
            return True, f"✅ GitHub: Authenticated as {username}"
        else:
            return False, f"❌ GitHub: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ GitHub: {str(e)}"

def test_zerobounce(api_key: str) -> Tuple[bool, str]:
    """Test ZeroBounce API"""
    if api_key == "your_zerobounce_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    url = f"https://api.zerobounce.net/v2/getcredits?api_key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            credits = data.get('Credits', 'unknown')
            return True, f"✅ ZeroBounce: {credits} credits available"
        else:
            return False, f"❌ ZeroBounce: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ ZeroBounce: {str(e)}"

def test_apollo(api_key: str) -> Tuple[bool, str]:
    """Test Apollo.io API"""
    if api_key == "your_apollo_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    url = "https://api.apollo.io/v1/auth/health"
    headers = {"X-Api-Key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return True, f"✅ Apollo.io: API connection healthy"
        else:
            return False, f"❌ Apollo.io: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Apollo.io: {str(e)}"

def test_wiza(api_key: str) -> Tuple[bool, str]:
    """Test Wiza API"""
    if api_key == "your_wiza_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    # Wiza API endpoint for testing
    url = "https://api.wiza.co/api/v1/credits"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            credits = data.get('credits_remaining', 'unknown')
            return True, f"✅ Wiza: {credits} credits remaining"
        else:
            return False, f"❌ Wiza: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Wiza: {str(e)}"

def test_surfe(api_key: str) -> Tuple[bool, str]:
    """Test Surfe API"""
    if api_key == "your_surfe_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    # Surfe API endpoint for testing
    url = "https://api.surfe.com/v1/account"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return True, f"✅ Surfe: API connection successful"
        elif response.status_code == 401:
            return False, f"❌ Surfe: Invalid API key"
        else:
            return False, f"❌ Surfe: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Surfe: {str(e)}"

def test_coresignal(api_key: str) -> Tuple[bool, str]:
    """Test Coresignal API"""
    if api_key == "your_coresignal_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    # Coresignal API endpoint for testing
    url = "https://api.coresignal.com/cdapi/v1/linkedin/company/search"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"limit": 1}  # Minimal test query
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return True, f"✅ Coresignal: API connection successful"
        elif response.status_code == 401:
            return False, f"❌ Coresignal: Invalid API key"
        else:
            return False, f"❌ Coresignal: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Coresignal: {str(e)}"

def main():
    """Main testing function"""
    print("🔍 Testing Data Enrichment APIs...")
    print("=" * 50)
    
    # Load API keys
    api_keys = load_api_keys()
    if not api_keys:
        print("❌ No API keys found!")
        return
    
    # Test each API
    tests = [
        ("Hunter.io", "HUNTER_API_KEY", test_hunter_io),
        ("GitHub", "GITHUB_TOKEN", test_github),
        ("ZeroBounce", "ZEROBOUNCE_API_KEY", test_zerobounce),
        ("Apollo.io", "APOLLO_API_KEY", test_apollo),
        ("Wiza", "WIZA_API_KEY", test_wiza),
        ("Surfe", "SURFE_API_KEY", test_surfe),
        ("Coresignal", "CORESIGNAL_API_KEY", test_coresignal),
    ]
    
    results = []
    for service_name, key_name, test_func in tests:
        print(f"\n🧪 Testing {service_name}...")
        
        if key_name not in api_keys:
            results.append((service_name, False, f"❌ {key_name} not found"))
            continue
            
        api_key = api_keys[key_name]
        success, message = test_func(api_key)
        results.append((service_name, success, message))
        print(f"   {message}")
        
        # Rate limiting delay
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 API Testing Summary:")
    print("=" * 50)
    
    working_apis = 0
    total_apis = len(results)
    
    for service, success, message in results:
        print(f"{message}")
        if success:
            working_apis += 1
    
    print(f"\n🎯 Result: {working_apis}/{total_apis} APIs working properly")
    
    if working_apis == total_apis:
        print("🎉 All APIs are working! Ready for data enrichment.")
    elif working_apis > 0:
        print("⚠️  Some APIs need configuration or have issues.")
    else:
        print("❌ No APIs are working. Check your configuration.")

if __name__ == "__main__":
    main()
