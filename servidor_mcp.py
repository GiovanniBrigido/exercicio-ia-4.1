"""Servidor MCP que expõe o arquivo notas.md como resource."""

from pathlib import Path

from mcp.server import MCPServer

NOTAS = Path(__file__).parent / "notas.md"

mcp = MCPServer("notas")


@mcp.resource(
    "notas://notas.md",
    name="notas",
    title="Notas",
    description="Lista de tarefas e lembretes do arquivo notas.md",
    mime_type="text/markdown",
)
def ler_notas() -> str:
    # Lido a cada requisição, então edições no arquivo aparecem sem reiniciar o servidor
    return NOTAS.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")
