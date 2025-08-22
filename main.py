from flask import Flask, send_from_directory, request, Response
import requests

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def root():
    return send_from_directory(".", "index.html")

# serve static files
@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(".", path)

# 🔑 iframe proxy route
@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    if not url:
        return "Missing url", 400

    resp = requests.get(url, stream=True)
    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    # ⚡ strip X-Frame headers so iframe works
    headers = [(name, value) for (name, value) in headers if not name.lower().startswith("x-frame")]
    headers = [(name, value) for (name, value) in headers if not name.lower().startswith("content-security-policy")]

    return Response(resp.content, resp.status_code, headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
