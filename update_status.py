import os
import requests

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
ARKSTATUS_API_KEY = os.environ["ARKSTATUS_API_KEY"]
ARKSTATUS_SERVER_ID = os.environ["ARKSTATUS_SERVER_ID"]

# ---- Get ARK server status ----
ark_url = f"https://arkstatus.com/api/v1/servers/{ARKSTATUS_SERVER_ID}"

ark_response = requests.get(
    ark_url,
    headers={"X-API-Key": ARKSTATUS_API_KEY},
    timeout=30,
)

ark_response.raise_for_status()
payload = ark_response.json()

if not payload.get("success"):
    raise RuntimeError(f"ARK Status API error: {payload}")

server = payload["data"]

if server.get("status") == "online":
    player_count = int(server.get("players", 0))
    new_name = f":green_circle: Online Now: {player_count}"
else:
    new_name = ":red_circle: ARK Offline"

# ---- Check current Discord channel name ----
discord_url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}"

headers = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json",
}

channel_response = requests.get(
    discord_url,
    headers=headers,
    timeout=30,
)

channel_response.raise_for_status()
current_name = channel_response.json()["name"]

# Only rename if something actually changed
if current_name == new_name:
    print(f"No change needed: {current_name}")
else:
    update_response = requests.patch(
        discord_url,
        headers=headers,
        json={"name": new_name},
        timeout=30,
    )

    update_response.raise_for_status()
    print(f"Updated Discord channel: {current_name} -> {new_name}")
