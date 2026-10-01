# Transcript: "resuma minhas notas" via MCP

- **Cliente:** Claude Code (modelo claude-fable-5-1)
- **Servidor MCP:** `notas` (`server.py`, transporte stdio, configurado em `.mcp.json`)
- **Data:** 2026-10-01
- **Trecho:** pedido do usuário, chamada ao recurso e resposta do modelo, copiados da sessão. O conteúdo de `notas.md` não foi colado no chat; ele chegou ao modelo pela leitura do recurso MCP.

## Usuário

resuma minhas notas

## Chamada de ferramenta (Claude Code)

`ReadMcpResourceTool`

```json
{"server": "notas", "uri": "notas://notas.md"}
```

## Resultado devolvido pelo servidor MCP

```json
{"contents":[{"uri":"notas://notas.md","mimeType":"text/markdown","text":"Organizar exercício 1 e 2 da aula 4.\nOrganizar os pertences da viagem de segunda para BSB.\nIr à consulta odontológica hoje às 16h com toda a documentação necessária.\nEnviar as gravações das aulas para o Chris.\nVerificar no portal da EBC o número do artigo publicado.\n"}]}
```

## Claude

Li suas notas pelo recurso MCP `notas://notas.md` (servidor `notas`). São cinco pendências:

- **Hoje, 16h:** consulta odontológica, levando toda a documentação necessária.
- **Segunda:** viagem para BSB; falta organizar os pertences.
- **Aula 4:** organizar os exercícios 1 e 2.
- **Chris:** enviar as gravações das aulas.
- **EBC:** verificar no portal o número do artigo publicado.

A única com hora marcada é a consulta de hoje.
