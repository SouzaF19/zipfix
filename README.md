# ZipFix

**Um CLI para corrigir e extrair arquivos ZIP com nomes Unicode no Windows.**

[![CI](https://github.com/SouzaF19/zipfix/actions/workflows/ci.yml/badge.svg)](https://github.com/SouzaF19/zipfix/actions/workflows/ci.yml)
[![Release](https://img.shields.io/badge/release-v0.1.0-blue)](https://github.com/SouzaF19/zipfix/releases/tag/v0.1.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://github.com/SouzaF19/zipfix/blob/main/LICENSE)

---

## 📑 Sumário

- [Sobre o problema](#-sobre-o-problema)
- [A solução](#-a-solução)
- [Funcionalidades](#-funcionalidades)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Como funciona](#-como-funciona)
- [Desenvolvimento](#-desenvolvimento)
- [Testes](#-testes)
- [CI](#-ci)
- [Release](#-release)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Sobre o problema

Ao descompactar arquivos `.zip` no Windows, nomes de arquivos que contêm caracteres
especiais ou Unicode (acentuação, símbolos, emojis) podem chegar corrompidos — virando
`????`, `Ã£`, ou sequências ininteligíveis.

Isso acontece porque a especificação do formato ZIP exige que nomes não-ASCII sejam
marcados com o *flag* de UTF-8 (bit `0x800`) na entrada. Dependendo da ferramenta que
escreveu ou leu o ZIP, esse flag é ignorado ou aplicado de forma inconsistente, resultando
em perda de caracteres.

### Por que isso importa

- Extrair um ZIP com `Compress-Archive` / `Expand-Archive` no PowerShell pode gerar nomes quebrados;
- Prefixos e nomes com `ä`, `ç`, `ã`, `€`, emojis e combinações passam a ser ininteligíveis;
- Leitores em outras plataformas (Linux, Web, Android) reagem mal a nomes malformados.

---

## 🔧 A solução

O **ZipFix** é um pequeno CLI que:

1. Lê um arquivo `.zip`;
2. Valida e sanitiza cada entrada (remove caracteres proibidos no Windows e limita o tamanho);
3. Reescreve o ZIP com nomes seguros e com encoding correto (UTF-8);
4. Extrai os arquivos de forma determinística.

---

## ✨ Funcionalidades

- ✅ Correção de nomes em entradas de ZIP;
- ✅ Sanitização de caracteres inválidos no Windows;
- ✅ Limitação de tamanho de nome;
- ✅ Reescrita de ZIP com encoding correto;
- ✅ Extração com nomes sanitizados;
- ✅ Relatório de entradas reescritas/extraídas.

---

## 🧰 Instalação

```bash
pip install zipfix
```

ou, via ferramenta de empacotamento:

```bash
uv tool install zipfix
```

---

## 🚀 Uso

```bash
# Corrigir (reescrever) um ZIP
zipflix fix entrada.zip --out saida_corrigida.zip

# Extrair um ZIP com nomes sanitizados
zipflix extract entrada.zip destino/
```

### Exemplo

```bash
zipflix fix ./downloads/arquivo.zip --out ./downloads/arquivo_corrigido.zip
zipflix extract ./downloads/arquivo_corrigido.zip ./extraido/
```

---

## 🧠 Como funciona

- Usa o módulo nativo de ZIP (stdlib) que trata UTF-8;
- Emite o novo arquivo com o flag UTF-8 nas entradas;
- Sanitiza nomes proibidos no Windows (`|`, `<`, `>`, `:`, `"`, `?`, `*`, `\`) e caracteres de controle.

---

## 🗂️ Estrutura do projeto

```text
C:/zipflix
├── zipflix/
│   ├── __init__.py
│   ├── cli.py
│   ├── fixer.py
│   └── __main__.py
├── tests/
│   └── test_fixer.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── Makefile
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## 🔭 Próximos passos

- Testes com ZIPs reais, incluindo nomes com emoji;
- Suporte a criptografia (AES);
- Publicação no PyPI.

---

## 🧪 Desenvolvimento

```bash
make install
make test
make run INPUT=./entrada.zip OUT=./saida.zip
make build
make clean
```

---

## 🧪 Testes

```bash
python -m unittest discover -s tests -v
```

---

## ⚙️ CI

GitHub Actions roda os testes em todo push/PR para `main`.

---

## 🚀 Release

Tags seguem o formato `vX.Y.Z` (ex.: `v0.1.0`).

---

## 🤝 Contribuindo

1. Fork;
2. Branch;
3. Testes;
4. PR.

---

## 📄 Licença

MIT — ver [LICENSE](LICENSE).
