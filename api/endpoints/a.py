import asyncio
import httpx

# Define your constants
BASE_URL = "https://shark-app-6wiyn.ondigitalocean.app/api/v1"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/login"
TASK_ENDPOINT = f"{BASE_URL}/tasks/{{id}}"
LOGIN_PAYLOAD = {"email": "scascascasc", "password": "sacsacascsacasc"}

async def fetch_task_by_id(task_id: int) -> dict:
    """
    Logs in to get the token and fetches the task details by ID.
    """
    async with httpx.AsyncClient() as client:
        print("Attempting to log in...")
        
        # Step 1: Login and get the token
        login_response = await client.post(LOGIN_ENDPOINT, json=LOGIN_PAYLOAD)
        if login_response.status_code != 201:
            print(f"Login failed: {login_response.status_code} {login_response.text}")
            raise ValueError("Unable to log in.")

        data=token = login_response.json()
        token = data.get("token")
        user_data=data["user"]["id"]
        user_role=data["user"]["user_role"]["role"]
        print(user_role)
        
        print(user_data)
        if not token:
            print("Error: Token not found in the login response.")
            raise ValueError("Token not found in login response.")
        
        print("Login successful! Token received.")

        return user_data


async def main():
    task_id = 5250
    try:
        print("Starting the process...")
        result = await fetch_task_by_id(task_id)
        print("\nTask Details Retrieved:")
        print(result)
    except Exception as e:
        print("Error:", e)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
