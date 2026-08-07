#!/usr/bin/env python3
"""Login Bypass — the login query is built by string concatenation (xorb64 delivery)."""
import os, sys, sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, "/challenge/_shared")
from fetch_material import fetch_material

CHALLENGE_KEY = os.environ.get("CHALLENGE_KEY", "or-1-equals-1")
_MAT = {}
_DB = sqlite3.connect(":memory:", check_same_thread=False)
_DB.execute("CREATE TABLE users(username TEXT, password TEXT, role TEXT, secret TEXT)")
_DB.execute("INSERT INTO users VALUES('guest','guest','user','no secret for you')")
_DB.execute("INSERT INTO users VALUES('admin',?,?,?)", (os.urandom(8).hex(), "admin", CHALLENGE_KEY))
_DB.commit()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/flag":
            self._send(200, _MAT.get("delivery_blob", "") + "\n")
            return
        if parsed.path == "/login":
            args = parse_qs(parsed.query)
            user = args.get("user", [""])[0]
            pwd = args.get("pass", [""])[0]
            query = ("SELECT role, secret FROM users "
                     f"WHERE username='{user}' AND password='{pwd}'")
            try:
                row = _DB.execute(query).fetchone()
            except Exception as exc:
                self._send(500, f"sql error: {exc}\n")
                return
            if row and row[0] == "admin":
                self._send(200, f"welcome admin. locker key = {row[1]}\n")
            elif row:
                self._send(200, "logged in, but this account holds no key.\n")
            else:
                self._send(401, "login failed\n")
            return
        self._send(200, "POST-less login at /login?user=&pass=. Flag blob at /flag.\n")

    def log_message(self, *a):
        pass


def main():
    _MAT.update(fetch_material())
    print("Login Bypass on :8080 — inject into /login to authenticate as admin.")
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()


if __name__ == "__main__":
    main()
