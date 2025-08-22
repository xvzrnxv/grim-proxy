from flask import Flask, request, Response, send_from_directory
import requests, os

app = Flask(__name__, static_folder="games", static_url_path="/games")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/games/<path:path>")
def serve_games(path):
    return send_from_directory("games", path)

@app.route("/proxy")
def proxy():
    target = request.args.get("url")
    if not target:
        return "No URL provided", 400

    try:
        r = requests.get(target, headers={"User-Agent": request.headers.get("User-Agent", "Mozilla/5.0")}, timeout=10)
        excluded_headers = ["content-encoding", "transfer-encoding", "connection"]
        headers = [(name, value) for (name, value) in r.headers.items() if name.lower() not in excluded_headers]

        return Response(r.content, r.status_code, headers)
    except Exception as e:
        return f"Proxy error: {e}", 500

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
