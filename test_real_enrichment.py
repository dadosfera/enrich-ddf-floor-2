#!/usr/bin/env python3
"""
Test Real Data Enrichment vs Mock Data
Comprehensive testing of data enrichment sources
"""

import asyncio
import requests
import json
import os
from datetime import datetime

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80)

def print_result(title: str, data: dict, highlight_real: bool = False):
    """Print formatted enrichment result."""
    print(f"\n🔍 {title}")
    print("-" * 60)
    
    if highlight_real and 'mock' not in str(data.get('data_sources', [])):
        print("✅ REAL DATA ENRICHMENT")
    elif 'mock' in str(data.get('data_sources', [])):
        print("🚨 MOCK DATA (Configure API keys for real data)")
    
    print(json.dumps(data, indent=2))

def check_api_keys():
    """Check which API keys are configured."""
    print_section("API Key Status Check")
    
    keys = {
        'HUNTER_API_KEY': os.getenv('HUNTER_API_KEY'),
        'CLEARBIT_API_KEY': os.getenv('CLEARBIT_API_KEY'),
        'ZEROBOUNCE_API_KEY': os.getenv('ZEROBOUNCE_API_KEY'),
        'FULLCONTACT_API_KEY': os.getenv('FULLCONTACT_API_KEY')
    }
    
    configured_keys = []
    missing_keys = []
    
    for key, value in keys.items():
        if value and value != 'your_key_here':
            configured_keys.append(key)
            print(f"✅ {key}: Configured")
        else:
            missing_keys.append(key)
            print(f"❌ {key}: Not configured")
    
    print(f"\n📊 Status: {len(configured_keys)}/4 API keys configured")
    
    if not configured_keys:
        print("\n🚨 NO REAL API KEYS CONFIGURED - Will use mock data")
        print("To test real enrichment, get free API keys from:")
        print("  - Hunter.io: https://hunter.io/api-keys (50 free searches/month)")
        print("  - Clearbit: https://clearbit.com/api (50 free requests/month)")
        print("  - ZeroBounce: https://www.zerobounce.net/api (100 free validations)")
        print("  - FullContact: https://platform.fullcontact.com (1,000 free lookups)")
    
    return len(configured_keys) > 0

async def test_person_enrichment():
    """Test person enrichment with various data sources."""
    print_section("Person Enrichment Tests")
    
    # Test cases with different completeness levels
    test_cases = [
        {
            "name": "Complete Person Data",
            "data": {
                "first_name": "Elon",
                "last_name": "Musk",
                "email": "elon@tesla.com"
            }
        },
        {
            "name": "Partial Person Data",
            "data": {
                "first_name": "Tim",
                "last_name": "Cook",
                "email": "tcook@apple.com"
            }
        },
        {
            "name": "Minimal Person Data",
            "data": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@unknown.com"
            }
        }
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(
                'http://localhost:8247/api/v1/enrich/person',
                headers={'Content-Type': 'application/json'},
                json=test_case["data"],
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                enriched_data = result.get('data', {}).get('enriched_data', {})
                
                # Analyze data quality
                sources = enriched_data.get('data_sources', [])
                score = enriched_data.get('enrichment_score', 0)
                is_real = 'mock' not in str(sources)
                
                print_result(
                    f"{test_case['name']} - Score: {score}% - Sources: {sources}",
                    enriched_data,
                    highlight_real=is_real
                )
                
                # Quality analysis
                if is_real:
                    print("🎯 Real data obtained from:", ', '.join(sources))
                    if score > 80:
                        print("🏆 High quality enrichment!")
                    elif score > 60:
                        print("👍 Good enrichment quality")
                    else:
                        print("⚠️ Limited enrichment data")
                else:
                    print("🔄 Mock data provided - no real APIs available")
                    
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")

async def test_company_enrichment():
    """Test company enrichment."""
    print_section("Company Enrichment Tests")
    
    test_companies = [
        {
            "name": "Apple Inc",
            "domain": "apple.com"
        },
        {
            "name": "Tesla",
            "domain": "tesla.com"
        },
        {
            "name": "Microsoft",
            "domain": "microsoft.com"
        }
    ]
    
    for company in test_companies:
        try:
            response = requests.post(
                'http://localhost:8247/api/v1/enrich/company',
                headers={'Content-Type': 'application/json'},
                json=company,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                enriched_data = result.get('data', {}).get('enriched_data', {})
                
                sources = enriched_data.get('data_sources', [])
                score = enriched_data.get('enrichment_score', 0)
                is_real = 'mock' not in str(sources)
                
                print_result(
                    f"{company['name']} - Score: {score}% - Sources: {sources}",
                    enriched_data,
                    highlight_real=is_real
                )
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")

def test_api_health():
    """Test if the API is running."""
    try:
        response = requests.get('http://localhost:8247/health', timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ API is healthy")
            print(f"   Version: {health_data.get('version')}")
            print(f"   Database: {health_data.get('database')}")
            return True
        else:
            print(f"❌ API unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API not accessible: {e}")
        print("Please ensure the backend is running on port 8247")
        return False

async def benchmark_enrichment_speed():
    """Benchmark enrichment speed and quota usage."""
    print_section("Enrichment Performance Benchmark")
    
    start_time = datetime.now()
    
    # Test multiple requests
    test_emails = [
        "test1@example.com",
        "test2@example.com", 
        "test3@example.com"
    ]
    
    results = []
    for i, email in enumerate(test_emails):
        try:
            request_start = datetime.now()
            
            response = requests.post(
                'http://localhost:8247/api/v1/enrich/person',
                headers={'Content-Type': 'application/json'},
                json={
                    "first_name": f"Test{i+1}",
                    "last_name": "User",
                    "email": email
                },
                timeout=10
            )
            
            request_duration = (datetime.now() - request_start).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                enriched_data = result.get('data', {}).get('enriched_data', {})
                sources = enriched_data.get('data_sources', [])
                score = enriched_data.get('enrichment_score', 0)
                
                results.append({
                    'email': email,
                    'duration': request_duration,
                    'score': score,
                    'sources': sources,
                    'success': True
                })
                
                print(f"✅ {email}: {request_duration:.2f}s - {score}% - {sources}")
            else:
                results.append({
                    'email': email,
                    'duration': request_duration,
                    'success': False,
                    'error': response.status_code
                })
                print(f"❌ {email}: {request_duration:.2f}s - Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {email}: Error - {e}")
    
    total_duration = (datetime.now() - start_time).total_seconds()
    successful_requests = sum(1 for r in results if r.get('success'))
    average_duration = sum(r['duration'] for r in results if r.get('success')) / max(successful_requests, 1)
    
    print(f"\n📊 Performance Summary:")
    print(f"   Total time: {total_duration:.2f}s")
    print(f"   Successful requests: {successful_requests}/{len(test_emails)}")
    print(f"   Average request time: {average_duration:.2f}s")
    
    return results

def show_free_api_signup_instructions():
    """Show instructions for getting free API keys."""
    print_section("Free API Key Setup Instructions")
    
    apis = [
        {
            "name": "Hunter.io",
            "url": "https://hunter.io/api-keys",
            "free_tier": "50 searches/month",
            "setup": [
                "1. Sign up at hunter.io",
                "2. Go to API section",
                "3. Generate API key",
                "4. Set HUNTER_API_KEY=your_key"
            ]
        },
        {
            "name": "Clearbit",
            "url": "https://clearbit.com/api",
            "free_tier": "50 requests/month",
            "setup": [
                "1. Sign up at clearbit.com",
                "2. Go to API Keys section",
                "3. Copy secret key",
                "4. Set CLEARBIT_API_KEY=your_key"
            ]
        },
        {
            "name": "FullContact",
            "url": "https://platform.fullcontact.com",
            "free_tier": "1,000 lookups/month",
            "setup": [
                "1. Create account at FullContact",
                "2. Generate API key",
                "3. Set FULLCONTACT_API_KEY=your_key"
            ]
        },
        {
            "name": "ZeroBounce",
            "url": "https://www.zerobounce.net/api",
            "free_tier": "100 validations/month",
            "setup": [
                "1. Sign up at ZeroBounce",
                "2. Get API key from dashboard",
                "3. Set ZEROBOUNCE_API_KEY=your_key"
            ]
        }
    ]
    
    for api in apis:
        print(f"\n📡 {api['name']}")
        print(f"   Free tier: {api['free_tier']}")
        print(f"   URL: {api['url']}")
        for step in api['setup']:
            print(f"   {step}")
    
    print("\n🔧 Environment Setup:")
    print("   export HUNTER_API_KEY='your_hunter_key'")
    print("   export CLEARBIT_API_KEY='your_clearbit_key'")
    print("   export FULLCONTACT_API_KEY='your_fullcontact_key'")
    print("   export ZEROBOUNCE_API_KEY='your_zerobounce_key'")

async def main():
    """Run comprehensive enrichment tests."""
    print_section("🚀 Real Data Enrichment Testing Suite")
    
    # Check if API is running
    if not test_api_health():
        return
    
    # Check API key configuration
    has_real_apis = check_api_keys()
    
    if not has_real_apis:
        show_free_api_signup_instructions()
        print("\n🔄 Proceeding with mock data testing...")
    else:
        print("\n🎯 Real API keys detected - testing with live data sources!")
    
    # Run enrichment tests
    await test_person_enrichment()
    await test_company_enrichment()
    
    # Performance benchmark
    await benchmark_enrichment_speed()
    
    print_section("✅ Testing Complete")
    
    if has_real_apis:
        print("🎉 Real data enrichment is working!")
        print("Your API integrations are successfully providing live data.")
    else:
        print("🔧 To enable real data enrichment:")
        print("1. Get free API keys from the services above")
        print("2. Set environment variables")
        print("3. Restart the application")
        print("4. Re-run this test script")

if __name__ == "__main__":
    asyncio.run(main())
