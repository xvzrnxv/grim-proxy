from flask import Flask, request, Response, send_from_directory
import requests

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return send_from_directory("static", "index.html")

@app.route('/proxy')
def proxy():
    target_url = request.args.get("url")
    if not target_url:
        return "No URL provided", 400

    resp = requests.get(target_url)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    # Strip frame-blocking headers
    headers = [(name, value) for (name, value) in headers
               if name.lower() not in ["x-frame-options", "content-security-policy"]]

    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
