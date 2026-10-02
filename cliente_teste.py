"""Cliente MCP que conecta no servidor_mcp.py via stdio e grava evidencia-mcp.json."""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).parent
EVIDENCIA = RAIZ / "evidencia-mcp.json"

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ModuleNotFoundError:
    # O autograder roda `python cliente_teste.py` com o Python do PATH, que pode não
    # ter o SDK instalado; nesse caso reexecuta com o Python da .venv do projeto.
    python_venv = RAIZ / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python_venv.exists() or Path(sys.executable).resolve() == python_venv.resolve():
        raise
    sys.exit(subprocess.run([str(python_venv), __file__]).returncode)


async def coletar() -> dict:
    params = StdioServerParameters(
        command=sys.executable, args=[str(RAIZ / "servidor_mcp.py")]
    )
    async with stdio_client(params) as (leitura, escrita):
        async with ClientSession(leitura, escrita) as sessao:
            await sessao.initialize()
            recursos = (await sessao.list_resources()).resources
            uri = recursos[0].uri
            texto = (await sessao.read_resource(uri)).contents[0].text

    # Envelope no formato que o autograder do exercício ia-4.1 confere
    return {
        "transporte": "stdio",
        "servidor": "servidor_mcp.py",
        "resources": [str(r.uri) for r in recursos],
        "uri_lida": str(uri),
        "conteudo_chars": len(texto),
        "primeira_linha": next((l.strip() for l in texto.splitlines() if l.strip()), ""),
    }


if __name__ == "__main__":
    envelope = json.dumps(asyncio.run(coletar()), ensure_ascii=False, indent=2)
    EVIDENCIA.write_text(envelope + "\n", encoding="utf-8")
    # O autograder lê o envelope da saída do cliente, em UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
    print(envelope)
