import httpx
import asyncio
import hmac
import hashlib

SECRET_KEY = b"aegis_secure_shared_key_2026_termux"
URL = "http://127.0.0.1:8000/decide"

async def send_request(client, i):
    company = "enterprise"
    latency = 20.0 + (i % 40)
    error = 0.01
    message = f"{company}:{latency}:{error}".encode()
    sig = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()
    
    payload = {
        "company_size": company,
        "latency_ms": latency,
        "error_rate": error,
        "signature": sig
    }
    
    try:
        response = await client.post(URL, json=payload)
        print(f"Request {i}: Status {response.status_code}")
    except Exception as e:
        print(f"Request {i} failed: {e}")

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client, i) for i in range(10)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
