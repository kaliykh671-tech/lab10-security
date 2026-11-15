import hashlib
import sqlite3
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)
DB = "shop.db"


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, qty INTEGER)")
    conn.execute("INSERT OR IGNORE INTO items (id, name, qty) VALUES (1, 'kava', 5)")
    conn.commit()
    conn.close()


@app.get("/search")
def search():
    name = request.args.get("name", "")
    conn = sqlite3.connect(DB)
    query = "SELECT id, name, qty FROM items WHERE name = '%s'" % name
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify(rows=rows)


@app.get("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    out = subprocess.run("ping -n 1 " + host, shell=True, capture_output=True, text=True)
    return jsonify(output=out.stdout[-400:])


@app.get("/demo/etag")
def demo_etag():
    data = b"static demo page"
    return jsonify(etag=hashlib.md5(data).hexdigest())


if __name__ == "__main__":
    init_db()
    app.run(port=5000, debug=True)
