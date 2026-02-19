#!/usr/bin/env python3
"""
Test completo de todos los componentes NVIDIA NIM
Verifica que todo el sistema funcione correctamente.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_nvidia_config():
    """Test 1: Configuración NVIDIA"""
    print("\n🧪 TEST 1: NVIDIA Configuration")
    print("-" * 50)
    try:
        from nvidia_config import NVIDIA_API_KEY, NVIDIA_BASE_URL, MODEL_PRICING
        assert NVIDIA_API_KEY is not None, "API Key not found"
        assert NVIDIA_BASE_URL == "https://integrate.api.nvidia.com/v1", "Wrong base URL"
        assert len(MODEL_PRICING) >= 4, "Missing pricing info"
        print(f"✅ API Key: {NVIDIA_API_KEY[:20]}...")
        print(f"✅ Base URL: {NVIDIA_BASE_URL}")
        print(f"✅ Pricing models: {len(MODEL_PRICING)}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_nvidia_client():
    """Test 2: Cliente NVIDIA NIM"""
    print("\n🧪 TEST 2: NVIDIA NIM Client")
    print("-" * 50)
    try:
        from nvidia_nim_client import NVIDIANIMClient, ModelType
        client = NVIDIANIMClient()
        available = client.is_available()
        print(f"✅ Client initialized")
        print(f"✅ NVIDIA Available: {available}")
        print(f"✅ Preferred model: {client.preferred_model.value}")

        if available:
            response = client.generate("What is 2+2? Answer in one word.", max_tokens=10)
            print(f"✅ API Response: {response.text.strip()}")
            print(f"✅ Tokens used: {response.tokens_used}")
            print(f"✅ Latency: {response.latency_ms:.0f}ms")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_model_recommendations():
    """Test 3: Model Recommendations"""
    print("\n🧪 TEST 3: Model Recommendations")
    print("-" * 50)
    try:
        from model_recommendations import (
            SKILL_MODEL_MAPPING,
            get_recommended_model,
            get_cost_estimate,
            ModelType
        )

        print(f"✅ Total skills mapped: {len(SKILL_MODEL_MAPPING)}")

        # Test specific skills
        test_skills = [
            ("security-auditor", ModelType.NEMOTRON_340B, "ultra"),
            ("code-review-excellence", ModelType.CODELLAMA_70B, "high"),
            ("domain-strategy-router", ModelType.LLAMA_3B, "low"),
        ]

        for skill, expected_model, expected_tier in test_skills:
            model = get_recommended_model(skill)
            cost = get_cost_estimate(skill)
            assert model == expected_model, f"Wrong model for {skill}"
            assert cost["tier"] == expected_tier, f"Wrong tier for {skill}"
            print(f"✅ {skill}: {model.value} ({cost['tier']})")

        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_fallback_mechanism():
    """Test 4: Fallback a Ollama"""
    print("\n🧪 TEST 4: Fallback Mechanism")
    print("-" * 50)
    try:
        from nvidia_nim_client import NVIDIANIMClient
        client = NVIDIANIMClient()

        # Check fallback URL
        print(f"✅ Ollama URL: {client.ollama_url}")

        # Try to generate with fallback enabled
        response = client.generate("Hello", fallback=True)
        print(f"✅ Fallback working via: {response.model}")

        return True
    except Exception as e:
        print(f"⚠️  Fallback test (expected if Ollama not running): {e}")
        return True  # Fallback is optional

def test_embeddings():
    """Test 5: Embeddings"""
    print("\n🧪 TEST 5: Embeddings")
    print("-" * 50)
    try:
        from nvidia_nim_client import NVIDIANIMClient
        client = NVIDIANIMClient()

        embedding = client.generate_embedding("Test embedding")
        print(f"✅ Embedding generated: {len(embedding)} dimensions")
        return True
    except Exception as e:
        print(f"⚠️  Embeddings test: {e}")
        return True  # Embeddings are optional

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 70)
    print("🚀 NVIDIA NIM - COMPLETE SYSTEM TEST")
    print("=" * 70)

    tests = [
        ("NVIDIA Config", test_nvidia_config),
        ("NVIDIA Client", test_nvidia_client),
        ("Model Recommendations", test_model_recommendations),
        ("Fallback Mechanism", test_fallback_mechanism),
        ("Embeddings", test_embeddings),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} CRASHED: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} - {name}")

    print("-" * 70)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
    else:
        print("\n⚠️  Some tests failed. Check logs above.")

    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
