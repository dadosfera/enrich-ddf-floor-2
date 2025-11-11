#!/usr/bin/env python3
"""
Enhanced API Key Testing Script - Test all configured data enrichment APIs
with correct endpoints and comprehensive validation
"""
import os
import requests
import time
import json
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
    """Test Hunter.io API with correct endpoint"""
    if api_key == "your_hunter_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    # Correct Hunter.io API endpoint
    url = f"https://api.hunter.io/v2/account?api_key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            calls_used = data.get('data', {}).get('calls', {}).get('used', 0)
            calls_available = data.get('data', {}).get('calls', {}).get('available', 0)
            return True, f"✅ Hunter.io: {calls_used}/{calls_available} calls used"
        elif response.status_code == 401:
            return False, f"❌ Hunter.io: Invalid API key"
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
    """Test Apollo.io API with correct endpoint"""
    if api_key == "your_apollo_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    # Apollo.io uses a different health check endpoint
    url = "https://api.apollo.io/v1/email_accounts"
    headers = {"X-Api-Key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            account_count = len(data.get('email_accounts', []))
            return True, f"✅ Apollo.io: API working ({account_count} email accounts)"
        elif response.status_code == 401:
            return False, f"❌ Apollo.io: Invalid API key"
        else:
            return False, f"❌ Apollo.io: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Apollo.io: {str(e)}"

def test_wiza(api_key: str) -> Tuple[bool, str]:
    """Test Wiza API with correct endpoint"""
    if api_key == "your_wiza_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    # Wiza uses a different API structure
    url = "https://wiza.co/api/v1/account"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return True, f"✅ Wiza: API connection successful"
        elif response.status_code == 401:
            return False, f"❌ Wiza: Invalid API key"
        elif response.status_code == 404:
            # Try alternative endpoint structure
            url2 = "https://app.wiza.co/api/v1/credits"
            response2 = requests.get(url2, headers=headers, timeout=10)
            if response2.status_code == 200:
                return True, f"✅ Wiza: API connection successful (alternative endpoint)"
            else:
                return False, f"❌ Wiza: API endpoints not accessible (404)"
        else:
            return False, f"❌ Wiza: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Wiza: {str(e)}"

def test_surfe(api_key: str) -> Tuple[bool, str]:
    """Test Surfe API with correct endpoint"""
    if api_key == "your_surfe_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    # Surfe API might use different endpoint structure
    url = "https://surfe.com/api/v1/me"
    headers = {"X-API-Key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return True, f"✅ Surfe: API connection successful"
        elif response.status_code == 401:
            return False, f"❌ Surfe: Invalid API key"
        elif response.status_code == 404:
            # Try alternative authentication method
            headers_alt = {"Authorization": f"Bearer {api_key}"}
            response2 = requests.get(url, headers=headers_alt, timeout=10)
            if response2.status_code == 200:
                return True, f"✅ Surfe: API connection successful (Bearer auth)"
            else:
                return False, f"❌ Surfe: API endpoints not accessible - may need documentation review"
        else:
            return False, f"❌ Surfe: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Surfe: {str(e)}"

def test_coresignal(api_key: str) -> Tuple[bool, str]:
    """Test Coresignal API with correct endpoint"""
    if api_key == "your_coresignal_api_key_here":
        return False, "❌ Placeholder key - needs configuration"
    
    # Coresignal API endpoint structure 
    url = "https://api.coresignal.com/cdapi/v1/linkedin/member/search/filter"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Simple test query
    payload = {
        "limit": 1,
        "title": "CEO"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return True, f"✅ Coresignal: API connection successful"
        elif response.status_code == 401:
            return False, f"❌ Coresignal: Invalid API key"
        elif response.status_code == 403:
            return False, f"❌ Coresignal: API key lacks permissions"
        elif response.status_code == 404:
            # Try alternative endpoint
            url2 = "https://api.coresignal.com/cdapi/v1/account"
            response2 = requests.get(url2, headers=headers, timeout=10)
            if response2.status_code == 200:
                return True, f"✅ Coresignal: API connection successful (account endpoint)"
            else:
                return False, f"❌ Coresignal: API endpoints not accessible"
        else:
            return False, f"❌ Coresignal: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ Coresignal: {str(e)}"

def test_bigdata_corp(api_key: str, secret: str) -> Tuple[bool, str]:
    """Test BigData Corp API (Brazilian data)"""
    if api_key == "your_bigdata_corp_api_key_here" or not api_key:
        return False, "❌ Placeholder key - needs configuration"
    
    # BigData Corp API for Brazilian CPF/CNPJ data
    url = "https://api.bigdatacorp.com.br/status"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-API-Secret": secret if secret != "your_bigdata_corp_secret_here" else ""
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return True, f"✅ BigData Corp: API connection successful"
        elif response.status_code == 401:
            return False, f"❌ BigData Corp: Invalid credentials"
        else:
            return False, f"❌ BigData Corp: HTTP {response.status_code}"
    except Exception as e:
        return False, f"❌ BigData Corp: {str(e)}"

def main():
    """Main testing function"""
    print("🔍 Enhanced API Testing for Data Enrichment APIs...")
    print("=" * 60)
    
    # Load API keys
    api_keys = load_api_keys()
    if not api_keys:
        print("❌ No API keys found!")
        return
    
    print("📦 Loaded API keys from ~/vars/enrich-ddf-api-keys.env")
    print(f"🔑 Found {len(api_keys)} API configurations")
    print()
    
    # Test each API with improved endpoints
    results = []
    
    # Test working APIs first
    working_tests = [
        ("GitHub", "GITHUB_TOKEN", test_github),
        ("ZeroBounce", "ZEROBOUNCE_API_KEY", test_zerobounce),
        ("Apollo.io", "APOLLO_API_KEY", test_apollo),
    ]
    
    # Test problematic APIs with enhanced logic
    enhanced_tests = [
        ("Hunter.io", "HUNTER_API_KEY", test_hunter_io),
        ("Wiza", "WIZA_API_KEY", test_wiza),
        ("Surfe", "SURFE_API_KEY", test_surfe),
        ("Coresignal", "CORESIGNAL_API_KEY", test_coresignal),
    ]
    
    # Special test for BigData Corp (needs both key and secret)
    if "BIGDATA_CORP_API_KEY" in api_keys and "BIGDATA_CORP_SECRET" in api_keys:
        enhanced_tests.append(("BigData Corp (🇧🇷)", None, lambda _: test_bigdata_corp(
            api_keys["BIGDATA_CORP_API_KEY"], 
            api_keys["BIGDATA_CORP_SECRET"]
        )))
    
    all_tests = working_tests + enhanced_tests
    
    for service_name, key_name, test_func in all_tests:
        print(f"🧪 Testing {service_name}...")
        
        if key_name and key_name not in api_keys:
            results.append((service_name, False, f"❌ {key_name} not found"))
            print(f"   ❌ {key_name} not found")
            continue
            
        if key_name:
            api_key = api_keys[key_name]
            success, message = test_func(api_key)
        else:
            success, message = test_func(None)
            
        results.append((service_name, success, message))
        print(f"   {message}")
        
        # Rate limiting delay
        time.sleep(1)
    
    # Summary with enhanced reporting
    print("\n" + "=" * 60)
    print("📊 Enhanced API Testing Summary:")
    print("=" * 60)
    
    working_apis = []
    broken_apis = []
    placeholder_apis = []
    
    for service, success, message in results:
        print(f"{message}")
        if success:
            working_apis.append(service)
        elif "placeholder" in message.lower() or "needs configuration" in message.lower():
            placeholder_apis.append(service)
        else:
            broken_apis.append(service)
    
    print(f"\n🎯 Final Results:")
    print(f"   ✅ Working APIs: {len(working_apis)}")
    print(f"   🔧 Need Configuration: {len(placeholder_apis)}")
    print(f"   ❌ Connection Issues: {len(broken_apis)}")
    print(f"   📊 Total APIs: {len(results)}")
    
    if working_apis:
        print(f"\n💪 Working APIs: {', '.join(working_apis)}")
    
    if placeholder_apis:
        print(f"\n⚙️  Need API Keys: {', '.join(placeholder_apis)}")
    
    if broken_apis:
        print(f"\n🔧 Need Investigation: {', '.join(broken_apis)}")
    
    print(f"\n{'🎉' if len(working_apis) >= 3 else '⚠️'} Status: {len(working_apis)}/{len(results)} APIs operational")

if __name__ == "__main__":
    main()
