#!/usr/bin/env python
"""
Direct test of LLM client to diagnose issues
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.llm_client import LLMClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_llm():
    """Test LLM client directly"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        return False

    print(f"✓ API Key found: {api_key[:20]}...")

    try:
        print("\n📝 Initializing LLM client...")
        llm = LLMClient(provider='gemini', api_key=api_key)
        print("✓ LLM client initialized")

        print("\n🤖 Testing simple prompt...")
        response = llm.generate("What are stocks in one sentence?")
        print(f"✓ Response: {response[:200]}...")

        print("\n✅ LLM is working correctly!")
        return True

    except RuntimeError as e:
        print(f"❌ API Error: {e}")
        logger.exception("Full error trace:")
        return False


if __name__ == "__main__":
    success = test_llm()
    sys.exit(0 if success else 1)
