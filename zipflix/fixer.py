"""Correção de nomes em arquivos ZIP com suporte a Unicode."""

import os
import re
import shutil
import zipfile

INVALID_CHARS = re.compile(r'[<>:\"|?*\x00-\x1f]')
MAX_NAME_LENGTH = 255


def sanitize_name(name: str) -> str:
    r"""Remove caracteres proibidos no Windows, descarta segmentos perigosos e limita tamanhos.

    - Normaliza `\` -> `/`.
    - Remove caracteres inválidos (<>:"/\|?* e controle) e descarta segmentos vazios/`.`/`..`.
    - Limita cada componente a `MAX_NAME_LENGTH`.
    """
    cleaned = name.replace("\\", "/")
    trailing = cleaned.endswith("/")
    parts = []
    for part in cleaned.split("/"):
        p = INVALID_CHARS.sub("", part).strip()
        if p and p not in (".", ".."):
            parts.append(p)
    cleaned = "/".join(parts)
    cleaned = cleaned.rstrip(".")
    segments = cleaned.split("/") if cleaned else []
    cleaned = "/".join(seg[:MAX_NAME_LENGTH].rstrip() for seg in segments)
    if trailing and cleaned and not cleaned.endswith("/"):
        cleaned = cleaned + "/"
    return cleaned


def read_entries(path: str) -> list:
    with zipfile.ZipFile(path, "r") as zf:
        return zf.infolist()


def _clean_entries(path: str) -> list:
    cleaned = []
    seen = set()
    with zipfile.ZipFile(path, "r") as zf:
        for info in zf.infolist():
            name = sanitize_name(info.filename)
            if not name or name in seen:
                continue
            seen.add(name)
            cleaned.append((name, info))
    return cleaned


def fix_zip(src: str, dst: str) -> list:
    """Reescreve o ZIP de entrada com nomes sanitizados (UTF-8) em um novo ZIP."""
    if os.path.abspath(src) == os.path.abspath(dst):
        raise ValueError("src and dst must differ")
    results = []
    with zipfile.ZipFile(src, "r") as zin, \
         zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, info in _clean_entries(src):
            new_info = zipfile.ZipInfo(filename=name, date_time=info.date_time)
            new_info.compress_type = info.compress_type
            new_info.external_attr = info.external_attr
            new_info.create_system = info.create_system
            zout.writestr(new_info, zin.read(info))
            results.append((info.filename, name))
    return results


def extract_zip(src: str, dest: str) -> int:
    """Extrai um ZIP para o diretório, com nomes sanitizados."""
    os.makedirs(dest, exist_ok=True)
    count = 0
    with zipfile.ZipFile(src, "r") as zf:
        for name, info in _clean_entries(src):
            target = os.path.join(dest, *name.split("/"))
            if info.filename.endswith("/"):
                os.makedirs(target, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(target) or dest, exist_ok=True)
            with zf.open(info) as srcf, open(target, "wb") as f:
                shutil.copyfileobj(srcf, f)
            count += 1
    return count
