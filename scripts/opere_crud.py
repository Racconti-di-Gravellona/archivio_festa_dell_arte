#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parents[1] / "data" / "opere.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def get_gallery(data, gid):
    for g in data.get("gallerie", []):
        if g.get("id") == gid:
            return g
    raise SystemExit(f"galleria non trovata: {gid}")


def find_indices(ops, match=None, index=None):
    if index is not None:
        if index < 0 or index >= len(ops):
            raise SystemExit(f"indice fuori range: {index} (0..{len(ops)-1})")
        return [index]
    if match is None:
        raise SystemExit("specifica --index o --match")
    m = match.lower()
    idxs = []
    for i, o in enumerate(ops):
        hay = " ".join(str(o.get(k, "")) for k in ("titolo", "didascalia", "file", "img", "nota", "credito"))
        if m in hay.lower():
            idxs.append(i)
    if not idxs:
        raise SystemExit(f"nessuna opera trovata per: {match}")
    return idxs


def require_one(idxs, match):
    if len(idxs) != 1:
        raise SystemExit(f"match ambiguo ({len(idxs)} risultati) per: {match} — usa --index")
    return idxs[0]


def cmd_list(args):
    data = load(args.data)
    gids = [args.gallery] if args.gallery else [g.get("id") for g in data.get("gallerie", [])]
    for gid in gids:
        g = get_gallery(data, gid)
        ops = g.get("opere", [])
        print(f"== {gid} ({len(ops)}) ==")
        for i, o in enumerate(ops):
            anno = o.get("anno", "-")
            ident = o.get("file") or o.get("img") or ""
            print(f"{i:3d} | {anno!s:>4} | {o.get('titolo','')} | {ident}")
        if not args.gallery:
            print()


def cmd_show(args):
    data = load(args.data)
    g = get_gallery(data, args.gallery)
    ops = g.get("opere", [])
    idxs = find_indices(ops, args.match, args.index)
    for i in idxs:
        print(f"--- {args.gallery}[{i}] ---")
        print(json.dumps(ops[i], ensure_ascii=False, indent=2))


def cmd_set(args):
    data = load(args.data)
    g = get_gallery(data, args.gallery)
    ops = g.get("opere", [])
    idxs = find_indices(ops, args.match, args.index)
    if args.all_matches:
        targets = idxs
    else:
        targets = [require_one(idxs, args.match or args.index)]
    fields = {
        "titolo": args.titolo,
        "didascalia": args.didascalia,
        "nota": args.nota,
        "credito": args.credito,
        "fonte": args.fonte,
        "link": args.link,
        "file": args.file,
        "img": args.img,
    }
    changed = 0
    for i in targets:
        o = ops[i]
        for k, v in fields.items():
            if v is not None:
                o[k] = v
        if args.anno is not None:
            if args.anno.lower() in ("none", "null", "-"):
                o.pop("anno", None)
            else:
                o["anno"] = int(args.anno)
        if args.anno_dubbio is not None:
            if args.anno_dubbio.lower() == "true":
                o["annoDubbio"] = True
            elif args.anno_dubbio.lower() == "false":
                o["annoDubbio"] = False
        if args.clear_anno_dubbio:
            o.pop("annoDubbio", None)
        changed += 1
        print(f"updated {args.gallery}[{i}] {o.get('titolo','')}")
    if not args.dry_run:
        save(args.data, data)
    print(f"salvati: {0 if args.dry_run else changed} (dry-run={args.dry_run})")


def cmd_add(args):
    data = load(args.data)
    g = get_gallery(data, args.gallery)
    ops = g.setdefault("opere", [])
    if not args.titolo or not args.didascalia:
        raise SystemExit("--titolo e --didascalia sono obbligatori per add")
    o = {"titolo": args.titolo, "didascalia": args.didascalia}
    for k in ("nota", "credito", "fonte", "link", "file", "img"):
        v = getattr(args, k)
        if v is not None:
            o[k] = v
    if args.anno is not None:
        o["anno"] = int(args.anno)
    if args.anno_dubbio:
        o["annoDubbio"] = True
    pos = args.index if args.index is not None else len(ops)
    pos = max(0, min(pos, len(ops)))
    ops.insert(pos, o)
    if not args.dry_run:
        save(args.data, data)
    print(f"added {args.gallery}[{pos}] {o['titolo']} (dry-run={args.dry_run})")


def cmd_delete(args):
    data = load(args.data)
    g = get_gallery(data, args.gallery)
    ops = g.get("opere", [])
    idx = require_one(find_indices(ops, args.match, args.index), args.match or args.index)
    removed = ops.pop(idx)
    if not args.dry_run:
        save(args.data, data)
    print(f"deleted {args.gallery}[{idx}] {removed.get('titolo','')} (dry-run={args.dry_run})")


def cmd_move(args):
    data = load(args.data)
    g = get_gallery(data, args.gallery)
    ops = g.get("opere", [])
    idx = require_one(find_indices(ops, args.match, args.index), args.match or args.index)
    if args.to is not None:
        dest = args.to
    elif args.up:
        dest = idx - args.up
    elif args.down:
        dest = idx + args.down
    else:
        raise SystemExit("specifica --to, --up o --down")
    dest = max(0, min(dest, len(ops) - 1))
    item = ops.pop(idx)
    ops.insert(dest, item)
    if not args.dry_run:
        save(args.data, data)
    print(f"moved {args.gallery} {idx} -> {dest} {item.get('titolo','')} (dry-run={args.dry_run})")


def cmd_sort(args):
    data = load(args.data)
    gids = [args.gallery] if args.gallery else [g.get("id") for g in data.get("gallerie", [])]
    for gid in gids:
        g = get_gallery(data, gid)
        ops = g.get("opere", [])
        if args.by == "anno":
            ops.sort(key=lambda o: (o.get("anno") is None, o.get("anno", 9999), o.get("titolo", "")))
        elif args.by == "titolo":
            ops.sort(key=lambda o: o.get("titolo", "").lower())
        else:
            raise SystemExit(f"campo sort non supportato: {args.by}")
        print(f"sorted {gid} by {args.by}")
    if not args.dry_run:
        save(args.data, data)
    print(f"salvato (dry-run={args.dry_run})")


def main():
    p = argparse.ArgumentParser(description="CRUD per opere in data/opere.json (titolo, didascalia/testo, anno, ordinamento)")
    p.add_argument("--data", default=str(DEFAULT_DATA), help="percorso opere.json")
    p.add_argument("--dry-run", action="store_true", help="non scrivere il file")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("list", help="elenca opere")
    sp.add_argument("--gallery", help="id galleria (murales, arredo, ...)")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("show", help="mostra opere (JSON)")
    sp.add_argument("--gallery", required=True)
    sp.add_argument("--index", type=int)
    sp.add_argument("--match")
    sp.set_defaults(func=cmd_show)

    sp = sub.add_parser("set", help="modifica campi (titolo, didascalia, anno, ...)")
    sp.add_argument("--gallery", required=True)
    sp.add_argument("--index", type=int)
    sp.add_argument("--match")
    sp.add_argument("--all-matches", action="store_true")
    sp.add_argument("--titolo")
    sp.add_argument("--didascalia")
    sp.add_argument("--anno", help="numero, oppure none/null per rimuovere")
    sp.add_argument("--anno-dubbio", choices=["true", "false"])
    sp.add_argument("--clear-anno-dubbio", action="store_true")
    sp.add_argument("--nota")
    sp.add_argument("--credito")
    sp.add_argument("--fonte")
    sp.add_argument("--link")
    sp.add_argument("--file")
    sp.add_argument("--img")
    sp.set_defaults(func=cmd_set)

    sp = sub.add_parser("add", help="aggiunge un'opera")
    sp.add_argument("--gallery", required=True)
    sp.add_argument("--index", type=int, help="posizione (default: fine)")
    sp.add_argument("--titolo", required=True)
    sp.add_argument("--didascalia", required=True)
    sp.add_argument("--anno", type=int)
    sp.add_argument("--anno-dubbio", action="store_true")
    sp.add_argument("--nota")
    sp.add_argument("--credito")
    sp.add_argument("--fonte")
    sp.add_argument("--link")
    sp.add_argument("--file")
    sp.add_argument("--img")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("delete", help="rimuove un'opera")
    sp.add_argument("--gallery", required=True)
    sp.add_argument("--index", type=int)
    sp.add_argument("--match")
    sp.set_defaults(func=cmd_delete)

    sp = sub.add_parser("move", help="sposta un'opera (ordinamento)")
    sp.add_argument("--gallery", required=True)
    sp.add_argument("--index", type=int)
    sp.add_argument("--match")
    sp.add_argument("--to", type=int, help="indice destinazione")
    sp.add_argument("--up", type=int, nargs="?", const=1)
    sp.add_argument("--down", type=int, nargs="?", const=1)
    sp.set_defaults(func=cmd_move)

    sp = sub.add_parser("sort", help="ordina opere")
    sp.add_argument("--gallery", help="se omesso, tutte le gallerie")
    sp.add_argument("--by", default="anno", choices=["anno", "titolo"])
    sp.set_defaults(func=cmd_sort)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
