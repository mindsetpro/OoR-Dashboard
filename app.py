from flask import Flask, render_template, jsonify, request, redirect
import os
import requests

app = Flask(__name__)

# Replace these with your Discord application credentials
CLIENT_ID = "1177696282932945077"
CLIENT_SECRET = "zTHtnpYUIOKtzT2s9Qs-jMLLtut6tadS"
REDIRECT_URI = "https://mindsetpro.github.io/OoR-Dashboard/"
DISCORD_API_URL = "https://discord.com/api/v10"

# Specify the server ID to exclude
EXCLUDED_SERVER_ID = 1180244346696634419

@app.before_first_request
def activate_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

async def fetch_user_servers(user_id):
    if user_id not in server_data:
        await fetch_server_data(user_id)

@app.route('/api/servers', methods=['POST'])
async def get_servers():
    user_id = request.json.get('user_id')

    # Fetch the user's servers if not already fetched
    await fetch_user_servers(user_id)

    return jsonify({"servers": server_data.get(user_id, [])})


@app.route('/login')
def login():
    return redirect(f"{DISCORD_API_URL}/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(f"{DISCORD_API_URL}/oauth2/token", data=data, headers=headers)
    json_response = response.json()
    access_token = json_response.get('access_token')

    if access_token:
        user_info = get_user_info(access_token)
        user_id = user_info.get('id')
        return render_template('index.html', user_id=user_id)
    else:
        return "Authentication failed"

def get_user_info(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(f"{DISCORD_API_URL}/users/@me", headers=headers)
    return response.json()

@app.route('/api/servers', methods=['POST'])
def get_servers():
    user_id = request.json.get('user_id')
    user_servers = server_data.get(user_id, [])

    # Exclude the specified server
    user_servers = [server for server in user_servers if server != EXCLUDED_SERVER_ID]

    return jsonify({"servers": user_servers})

@app.route('/')
def index():
    user_id = request.args.get('user_id')
    return render_template('index.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
