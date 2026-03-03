from app.agents.code_reviewer import revisar_codigo
import os

SKIP_DIRS = {"venv", ".venv", "__pycache__", "build", "dist", ".eggs", ".git", "node_modules"}

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if f.endswith(".py"):
            print(f"\n🔍 Revisando {f}")
            resultado = revisar_codigo(os.path.join(root, f))
            print(resultado)
