from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__, static_folder="games", static_url_path="/games")

# Serve index.html at /
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Serve everything else from games/ folder
@app.route("/games/<path:path>")
def serve_games(path):
    return send_from_directory("games", path)

# Fallback route for static files (images, css, js, etc.)
@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
