from flask import abort, request, Flask, jsonify
import os
import server_proxy

app = Flask(__name__)

AFK_KEYWORD = os.getenv("AFK_KEYWORD", "afk").lower()
AFK_THRESHOLD = int(os.getenv("AFK_THRESHOLD", 1800))  # In seconds
API_PORT = int(os.getenv("API_PORT", 6504))
API_TOKEN = os.getenv("API_TOKEN", "")
API_TOKEN_HEADER_NAME = os.getenv("API_TOKEN_HEADER_NAME", "X-API-Token")

def check_api_token():
    if API_TOKEN:
        token = request.headers.get("X-API-Token")
        if token != API_TOKEN:
            abort(401)


@app.route("/api/status")
@app.route("/api/status/")
def status():
    check_api_token()

    try:
        server = server_proxy.get_server_proxy()
        users = server.getUsers()
        channels = server.getChannels()

        user_list = []
        for user in users.values():
            ch_name = channels[user.channel].name
            is_afk = (
                AFK_KEYWORD in ch_name.lower() or
                user.idlesecs >= AFK_THRESHOLD
            )
            user_list.append({
                "mumble-id": user.name,
                "channel": ch_name,
                "afk": is_afk,
                "idle_seconds": user.idlesecs
            })
            total_users = len(user_list)
        if not user_list:
            user_list = [{"mumble-id": "Noone is here...", "channel": "Be the first!"}]
            total_users = 0
        return jsonify({"status": "online","total_users_online": total_users ,"users": user_list})
    except Exception as e:
        print(f"API-Error: {e}")
        return jsonify({"status": "offline","total_users_online": 0 , "users": [{"mumble-id": "Noone is here...", "channel": "How could they... The server is offline!"}]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=API_PORT, use_reloader=False)