from flask import Flask, send_from_directory, request, Response
import requests

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/proxy")
def proxy():
    target_url = request.args.get("url")
    if not target_url:
        return "Missing ?url=", 400

    try:
        resp = requests.get(target_url, headers={"User-Agent": "Mozilla/5.0"}, stream=True, timeout=10)
        excluded_headers = ["content-encoding", "transfer-encoding", "connection"]
        headers = [(name, value) for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers]
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Proxy error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
