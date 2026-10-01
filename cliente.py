"""Cliente MCP que conecta no server.py via stdio e grava evidencia-mcp.json."""

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

RAIZ = Path(__file__).parent
EVIDENCIA = RAIZ / "evidencia-mcp.json"


async def coletar() -> dict:
    params = StdioServerParameters(command=sys.executable, args=[str(RAIZ / "server.py")])
    async with stdio_client(params) as (leitura, escrita):
        async with ClientSession(leitura, escrita) as sessao:
            init = await sessao.initialize()
            recursos = (await sessao.list_resources()).resources
            uri = recursos[0].uri
            texto = (await sessao.read_resource(uri)).contents[0].text

    return {
        "transport": "stdio",
        "command": "python server.py",
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "server": {
            "name": init.server_info.name,
            "protocol_version": init.protocol_version,
        },
        "list_resources": {
            "resources": [
                {"uri": str(r.uri), "name": r.name, "mime_type": r.mime_type}
                for r in recursos
            ],
        },
        "read_resource": {
            "uri": str(uri),
            "chars": len(texto),
            "text": texto,
        },
    }


if __name__ == "__main__":
    evidencia = asyncio.run(coletar())
    EVIDENCIA.write_text(
        json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{EVIDENCIA.name} gravado: {len(evidencia['list_resources']['resources'])} "
          f"recurso(s), {evidencia['read_resource']['chars']} caracteres lidos")
