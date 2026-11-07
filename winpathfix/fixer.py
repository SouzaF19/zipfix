"""Renomeacao segura de arquivos soltos com caracteres invalidos no Windows."""

import os
import re

INVALID_CHARS = re.compile(r'[<>:\"|?*\x00-\x1f]')
MAX_NAME_LENGTH = 255


def sanitize_name(name: str) -> str:
    r"""Remove caracteres proibidos no Windows e limita o tamanho do nome."""
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


def collect_renames(dir_path: str) -> list:
    """Lista renomes (arquivo -> novo nome) para arquivos invalidos em dir_path."""
    renames = []
    for entry in sorted(os.listdir(dir_path)):
        full = os.path.join(dir_path, entry)
        if not os.path.isfile(full):
            continue
        new = sanitize_name(entry)
        if new != entry and new:
            renames.append((entry, new))
    return renames


def apply_renames(dir_path: str, renames: list) -> list:
    """Aplica renomes no diretorio; retorna lista de novos nomes criados."""
    done = []
    for old, new in renames:
        src = os.path.join(dir_path, old)
        dst = os.path.join(dir_path, new)
        if os.path.exists(src) and not os.path.exists(dst):
            os.rename(src, dst)
            done.append(new)
    return done
