#!/usr/bin/env python3
"""Test script to verify configuration loading with Base64 OpenAI key."""
import sys
import base64
from pathlib import Path


def test_base64_encoding():
    """Test Base64 encoding/decoding."""
    print("🧪 Testing Base64 encoding/decoding...")
    
    test_key = "sk-test-key-12345"
    encoded = base64.b64encode(test_key.encode('utf-8')).decode('utf-8')
    decoded = base64.b64decode(encoded).decode('utf-8')
    
    assert decoded == test_key, "Encoding/decoding mismatch!"
    print(f"   ✓ Test key: {test_key}")
    print(f"   ✓ Encoded: {encoded}")
    print(f"   ✓ Decoded: {decoded}")
    print("   ✅ Base64 encoding/decoding works!\n")


def check_env_file():
    """Check if .env file exists and has correct format."""
    print("📁 Checking .env file...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("   ⚠️  .env file not found")
        print("   💡 Create it from env.example: cp env.example .env\n")
        return False
    
    content = env_path.read_text()
    
    if "OPENAI_API_KEY_BASE64=" in content:
        print("   ✅ .env file has OPENAI_API_KEY_BASE64\n")
        return True
    elif "OPENAI_API_KEY=" in content and "OPENAI_API_KEY_BASE64=" not in content:
        print("   ⚠️  .env file still uses old format (OPENAI_API_KEY)")
        print("   💡 Please migrate to OPENAI_API_KEY_BASE64")
        print("   💡 Run: python3 encode_key.py\n")
        return False
    else:
        print("   ⚠️  .env file format unclear\n")
        return False


def test_config_loading():
    """Test loading configuration."""
    print("⚙️  Testing configuration loading...")
    
    try:
        # Remove loguru warning
        import warnings
        warnings.filterwarnings("ignore")
        
        from bot.config import settings
        
        print(f"   ✓ Bot token: {'*' * 10}{settings.bot_token[-10:] if len(settings.bot_token) > 10 else '***'}")
        print(f"   ✓ Database URL: {settings.database_url.split('@')[0]}@***")
        print(f"   ✓ OpenAI key (decoded): sk-{'*' * 20}{settings.openai_api_key[-5:] if len(settings.openai_api_key) > 5 else '***'}")
        print(f"   ✓ Report time: {settings.report_time}")
        print(f"   ✓ Timezone: {settings.timezone}")
        print("   ✅ Configuration loaded successfully!\n")
        return True
        
    except FileNotFoundError:
        print("   ❌ .env file not found")
        print("   💡 Create it from env.example\n")
        return False
    except ValueError as e:
        print(f"   ❌ Configuration error: {e}\n")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}\n")
        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("🔐 boto-sapiens Configuration Test")
    print("=" * 60)
    print()
    
    # Test 1: Base64 encoding
    test_base64_encoding()
    
    # Test 2: Check .env file
    env_ok = check_env_file()
    
    # Test 3: Load configuration (only if .env exists)
    if env_ok:
        config_ok = test_config_loading()
    else:
        print("⏭️  Skipping configuration loading test (fix .env first)\n")
        config_ok = False
    
    # Summary
    print("=" * 60)
    if env_ok and config_ok:
        print("✅ All tests passed! Your configuration is ready.")
        print("🚀 You can now run: python bot/main.py")
    else:
        print("⚠️  Some issues found. Please fix them before running the bot.")
        print("📖 See QUICKSTART.md or MIGRATION_BASE64.md for help")
    print("=" * 60)
    
    return 0 if (env_ok and config_ok) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)

