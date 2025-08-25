# Contributing

Setup
1. Python 3.11 installieren
2. Virtuelle Umgebung:
   - python -m venv .venv
   - .\.venv\Scripts\Activate.ps1
   - pip install --upgrade pip
   - pip install pre-commit black isort flake8
   - pre-commit install

Branch-Flow
- dev = Arbeits-Branch
- main = stabil
- Feature: feat/<kurzname>, Fix: fix/<kurzname>

Vor jedem Commit (lokal)
- black .
- isort .
- flake8 .
- pre-commit run --all-files

PR-Flow
1) git checkout -b feat/<name>
2) commit(s)
3) git push -u origin feat/<name>
4) PR: base=dev, compare=feat/<name>
5) CI gr?n ? Review ? Merge
