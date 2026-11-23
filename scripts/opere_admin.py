#!/usr/bin/env python3
"""Mini admin locale per data/opere.json.

Uso:
  python3 scripts/opere_admin.py
  python3 scripts/opere_admin.py --port 8787 --data data/opere.json

Espone:
  GET  /                         -> UI admin
  GET  /api/opere                -> JSON completo
  GET  /api/opere?gallery=ID     -> galleria
  PUT  /api/opere/<gid>/<idx>    -> aggiorna campi (titolo,didascalia,anno,annoDubbio,nota,credito,fonte,link,file,img)
  POST /api/opere/<gid>          -> aggiunge opera
  DELETE /api/opere/<gid>/<idx>  -> elimina opera
  POST /api/opere/<gid>/move     -> {from,to} oppure {index,dir:"up"|"down"}
  POST /api/opere/<gid>/sort     -> {by:"anno"|"titolo"}
"""
from __future__ import annotations

import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "opere.json"
ADMIN_HTML = Path(__file__).resolve().with_name("opere_admin.html")


class Store:
    def __init__(self, path: Path):
        self.path = path

    def load(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data):
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    def gallery(self, data, gid):
        for g in data.get("gallerie", []):
            if g.get("id") == gid:
                return g
        raise KeyError(gid)


def json_bytes(obj, status=200):
    body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    return status, body, "application/json; charset=utf-8"


class Handler(BaseHTTPRequestHandler):
    store: Store

    def log_message(self, fmt, *args):
        print(f"{self.client_address[0]} {fmt % args}")

    def _send(self, status, body: bytes, ctype="text/plain; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        n = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(n) if n else b"{}"
        return json.loads(raw.decode("utf-8"))

    def _error(self, status, msg):
        self._send(*json_bytes({"error": msg}, status=status))

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            if not ADMIN_HTML.exists():
                return self._error(404, f"manca {ADMIN_HTML}")
            body = ADMIN_HTML.read_bytes()
            return self._send(200, body, "text/html; charset=utf-8")
        if u.path == "/api/opere":
            data = self.store.load()
            qs = parse_qs(u.query)
            gid = qs.get("gallery", [None])[0]
            if gid:
                try:
                    g = self.store.gallery(data, gid)
                except KeyError:
                    return self._error(404, f"galleria non trovata: {gid}")
                return self._send(*json_bytes(g))
            return self._send(*json_bytes(data))
        if u.path == "/api/galleries":
            data = self.store.load()
            gs = [{"id": g.get("id"), "titolo": g.get("titolo"), "count": len(g.get("opere", []))} for g in data.get("gallerie", [])]
            return self._send(*json_bytes(gs))
        return self._error(404, "not found")

    def do_PUT(self):
        u = urlparse(self.path)
        parts = [p for p in u.path.split("/") if p]
        # /api/opere/<gid>/<idx>
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "opere":
            gid, idx_s = parts[2], parts[3]
            try:
                idx = int(idx_s)
            except ValueError:
                return self._error(400, "indice non valido")
            try:
                payload = self._read_json()
            except Exception as e:
                return self._error(400, f"json non valido: {e}")
            data = self.store.load()
            try:
                g = self.store.gallery(data, gid)
            except KeyError:
                return self._error(404, f"galleria non trovata: {gid}")
            ops = g.get("opere", [])
            if idx < 0 or idx >= len(ops):
                return self._error(404, "indice fuori range")
            o = ops[idx]
            for k in ("titolo", "didascalia", "nota", "credito", "fonte", "link", "file", "img"):
                if k in payload:
                    v = payload[k]
                    if v is None or v == "":
                        o.pop(k, None)
                    else:
                        o[k] = v
            if "anno" in payload:
                v = payload["anno"]
                if v is None or v == "" or v == "-":
                    o.pop("anno", None)
                else:
                    o["anno"] = int(v)
            if "annoDubbio" in payload:
                v = payload["annoDubbio"]
                if v is True:
                    o["annoDubbio"] = True
                else:
                    o.pop("annoDubbio", None)
            self.store.save(data)
            return self._send(*json_bytes({"ok": True, "index": idx, "opera": o}))
        return self._error(404, "not found")

    def do_POST(self):
        u = urlparse(self.path)
        parts = [p for p in u.path.split("/") if p]
        try:
            payload = self._read_json()
        except Exception as e:
            return self._error(400, f"json non valido: {e}")
        data = self.store.load()
        # /api/opere/<gid>
        if len(parts) == 3 and parts[:2] == ["api", "opere"]:
            gid = parts[2]
            try:
                g = self.store.gallery(data, gid)
            except KeyError:
                return self._error(404, f"galleria non trovata: {gid}")
            ops = g.setdefault("opere", [])
            o = {"titolo": payload.get("titolo", ""), "didascalia": payload.get("didascalia", "")}
            for k in ("nota", "credito", "fonte", "link", "file", "img"):
                if payload.get(k):
                    o[k] = payload[k]
            if payload.get("anno") not in (None, "", "-"):
                o["anno"] = int(payload["anno"])
            if payload.get("annoDubbio") is True:
                o["annoDubbio"] = True
            idx = payload.get("index")
            if idx is None:
                idx = len(ops)
            idx = max(0, min(int(idx), len(ops)))
            ops.insert(idx, o)
            self.store.save(data)
            return self._send(*json_bytes({"ok": True, "index": idx, "opera": o}, status=201))
        # /api/opere/<gid>/move
        if len(parts) == 4 and parts[:2] == ["api", "opere"] and parts[3] == "move":
            gid = parts[2]
            try:
                g = self.store.gallery(data, gid)
            except KeyError:
                return self._error(404, f"galleria non trovata: {gid}")
            ops = g.get("opere", [])
            src = int(payload.get("from", payload.get("index", -1)))
            if src < 0 or src >= len(ops):
                return self._error(400, "indice sorgente non valido")
            if "to" in payload:
                dst = int(payload["to"])
            else:
                d = payload.get("dir")
                dst = src - 1 if d == "up" else src + 1 if d == "down" else src
            dst = max(0, min(dst, len(ops) - 1))
            item = ops.pop(src)
            ops.insert(dst, item)
            self.store.save(data)
            return self._send(*json_bytes({"ok": True, "from": src, "to": dst}))
        # /api/opere/<gid>/sort
        if len(parts) == 4 and parts[:2] == ["api", "opere"] and parts[3] == "sort":
            gid = parts[2]
            try:
                g = self.store.gallery(data, gid)
            except KeyError:
                return self._error(404, f"galleria non trovata: {gid}")
            by = payload.get("by", "anno")
            ops = g.get("opere", [])
            if by == "anno":
                ops.sort(key=lambda o: (o.get("anno") is None, o.get("anno", 9999), o.get("titolo", "")))
            elif by == "titolo":
                ops.sort(key=lambda o: (o.get("titolo") or "").lower())
            else:
                return self._error(400, "by deve essere anno|titolo")
            self.store.save(data)
            return self._send(*json_bytes({"ok": True, "by": by, "count": len(ops)}))
        return self._error(404, "not found")

    def do_DELETE(self):
        u = urlparse(self.path)
        parts = [p for p in u.path.split("/") if p]
        if len(parts) == 4 and parts[:2] == ["api", "opere"]:
            gid, idx_s = parts[2], parts[3]
            try:
                idx = int(idx_s)
            except ValueError:
                return self._error(400, "indice non valido")
            data = self.store.load()
            try:
                g = self.store.gallery(data, gid)
            except KeyError:
                return self._error(404, f"galleria non trovata: {gid}")
            ops = g.get("opere", [])
            if idx < 0 or idx >= len(ops):
                return self._error(404, "indice fuori range")
            removed = ops.pop(idx)
            self.store.save(data)
            return self._send(*json_bytes({"ok": True, "removed": removed.get("titolo")}))
        return self._error(404, "not found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--data", default=str(DEFAULT_DATA))
    args = ap.parse_args()
    store = Store(Path(args.data).resolve())
    Handler.store = store
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Opere admin: http://{args.host}:{args.port}")
    print(f"Data: {store.path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
