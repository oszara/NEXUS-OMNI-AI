import os
import subprocess

def mkdir(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def file_missing(path):
    return not os.path.exists(path)

# 1️⃣ Directorios
mkdir("app")
mkdir("app/agents")
mkdir("tests")
mkdir(".github/workflows")

# 2️⃣ .gitignore
if file_missing(".gitignore"):
    write_file(".gitignore", """__pycache__/
*.pyc
.env
venv/
dist/
build/
""")

# 3️⃣ requirements.txt
if file_missing("requirements.txt"):
    write_file("requirements.txt", """ollama
fastapi
uvicorn
pytest
""")

# 4️⃣ GitHub CI
if file_missing(".github/workflows/ci.yml"):
    write_file(".github/workflows/ci.yml", """name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
""")

# 5️⃣ Test base
if file_missing("tests/test_basic.py"):
    write_file("tests/test_basic.py", """def test_basic():
    assert True
""")

print("Estructura completada.")

# 6️⃣ Instalar dependencias
subprocess.run(["pip", "install", "-r", "requirements.txt"])

# 7️⃣ Commit automático
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Auto-structure: added missing project files"])
