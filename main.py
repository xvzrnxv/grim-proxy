from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/games/<path:filename>")
def serve_games(filename):
    return send_from_directory("games", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
