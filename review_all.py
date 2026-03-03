from app.agents.code_reviewer import revisar_codigo
import os

for root, _, files in os.walk("."):
    for f in files:
        if f.endswith(".py"):
            print(f"\n🔍 Revisando {f}")
            resultado = revisar_codigo(os.path.join(root, f))
            print(resultado)
