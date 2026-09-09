import httpx
from httpx_socks import SyncProxyTransport
from config import settings

API_URL = settings.OPENROUTER_CREDITS_API
# API_URL = "https://openrouter.ai/api/v1/models"

transport = SyncProxyTransport.from_url("socks5://127.0.0.1:1080")
key = settings.OPENROUTER_API_KEY
print(key)

with httpx.Client(transport=transport, timeout=30.0) as client:
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Accept": "application/json",
    }

    response = client.get(API_URL, headers=headers)
    print(response.json())