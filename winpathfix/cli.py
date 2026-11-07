"""Interface de linha de comando do WinPathFix."""

import argparse
import os
import sys

from winpathfix import __version__
from winpathfix import fixer


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="winpathfix",
        description="Renomeia arquivos soltos com caracteres invalidos no Windows.",
    )
    parser.add_argument("--version", action="version", version=f"winpathfix {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    p_fix = sub.add_parser("fix", help="Renomeia arquivos invalidos em um diretorio.")
    p_fix.add_argument("directory", help="Diretório a escanear.")
    p_fix.add_argument("--dry-run", action="store_true", help="Apenas lista os renomes.")
    return parser


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "fix":
            renames = fixer.collect_renames(args.directory)
            print(f"OK: {len(renames)} arquivos com nomes invalidos encontrados em {args.directory}")
            for old, new in renames:
                print(f"  {old}  ==>  {new}")
            if not args.dry_run and renames:
                applied = fixer.apply_renames(args.directory, renames)
                print(f"Aplicados: {len(applied)} renomes")
            return 0
    except (OSError, ValueError) as exc:
        print(f"winpathfix: erro: {exc}", file=sys.stderr)
        return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
