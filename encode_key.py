#!/usr/bin/env python3
"""Helper script to encode OpenAI API key to Base64."""
import base64
import sys


def encode_key(api_key: str) -> str:
    """Encode API key to Base64."""
    encoded = base64.b64encode(api_key.encode('utf-8'))
    return encoded.decode('utf-8')


def main():
    """Main function."""
    print("🔐 OpenAI API Key Encoder")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # Key provided as argument
        api_key = sys.argv[1]
    else:
        # Interactive input
        print("\nВведите ваш OpenAI API ключ (начинается с sk-):")
        api_key = input("> ").strip()
    
    if not api_key:
        print("❌ Ошибка: ключ не может быть пустым")
        sys.exit(1)
    
    if not api_key.startswith("sk-"):
        print("⚠️  Предупреждение: обычно OpenAI ключи начинаются с 'sk-'")
        confirm = input("Продолжить? (y/n): ")
        if confirm.lower() != 'y':
            print("Отменено.")
            sys.exit(0)
    
    # Encode the key
    encoded_key = encode_key(api_key)
    
    print("\n✅ Ключ успешно закодирован!")
    print("\n📋 Добавьте эту строку в ваш .env файл:")
    print("-" * 50)
    print(f"OPENAI_API_KEY_BASE64={encoded_key}")
    print("-" * 50)
    
    # Verify by decoding
    decoded = base64.b64decode(encoded_key).decode('utf-8')
    if decoded == api_key:
        print("\n✓ Проверка: декодирование работает корректно")
    else:
        print("\n⚠️  Предупреждение: проблема с кодированием/декодированием")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nОтменено пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)

