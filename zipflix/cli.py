"""Interface de linha de comando do ZipFix."""

import argparse
import sys
import zipfile

from zipflix import __version__
from zipflix import fixer


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="zipflix",
        description="Corrige e extrai arquivos ZIP com nomes Unicode no Windows.",
    )
    parser.add_argument("--version", action="version", version=f"zipflix {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_fix = sub.add_parser("fix", help="Reescreve um ZIP com nomes sanitizados.")
    p_fix.add_argument("input", help="Caminho do ZIP de entrada.")
    p_fix.add_argument("--out", required=True, help="Caminho de saída do ZIP corrigido.")

    p_extract = sub.add_parser("extract", help="Extrai um ZIP com nomes sanitizados.")
    p_extract.add_argument("input", help="Caminho do ZIP de entrada.")
    p_extract.add_argument("dest", help="Diretório de destino da extração.")

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
            results = fixer.fix_zip(args.input, args.out)
            print(f"OK: {len(results)} entries reescritas -> {args.out}")
            for orig, new in results:
                print(f"  {orig}  ==>  {new}")
            return 0

        if args.command == "extract":
            count = fixer.extract_zip(args.input, args.dest)
            print(f"OK: {count} entries extraidos para {args.dest}")
            return 0
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"zipflix: erro: {exc}", file=sys.stderr)
        return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
