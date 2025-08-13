from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "video-service is healthy"}

@app.get("/fetch-user/{user_id}")
async def fetch_user(user_id: int):
    url = f"http://user-service:8081/users/{user_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        return {"error": f"User service returned error: {exc.response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
