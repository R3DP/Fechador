# Extensões

Uma extensão é um pacote Python separado que se soma ao Sellbird sem alterá-lo
por patch. Ela pode adicionar:

- **rotas do dashboard**: servidas atrás do login do dashboard, depois de todas as
  rotas nativas, então uma extensão pode adicionar caminhos, mas nunca substituir um;
- **etapas de tick**: funções assíncronas executadas uma vez ao fim de cada ciclo de heartbeat;
- **comandos**: subcomandos `sellbird <name>`. Um nome que a CLI nativa já
  usa é recusado;
- **regras de envio**: consultadas antes de cada e-mail, depois das verificações do
  próprio Sellbird. Uma regra retorna `send_hooks.Hold(reason)` (o e-mail espera pelo próximo
  ciclo), `send_hooks.Cancel(reason)`, ou None. Ela pode barrar um e-mail, nunca
  liberar um, e uma regra que levanta exceção retém o e-mail;
- **cabeçalhos de envio**: cabeçalhos extras para um e-mail, como `List-Unsubscribe`.
  Cabeçalhos de posse do Sellbird (From, To, Subject, Message-ID e similares) são
  recusados. Um e-mail que precisa de cabeçalhos que a caixa de entrada não suporta (o
  Microsoft 365 não suporta) espera em vez de sair sem eles.

Uma instalação padrão não tem extensões e se comporta exatamente como sem elas.

## Escrevendo uma

Declare um entry point no grupo `sellbird.extensions`. Seu valor é uma
função que recebe o registro:

```toml
# your package's pyproject.toml
[project.entry-points."sellbird.extensions"]
myext = "myext.sellbird_plugin:install"
```

```python
# myext/sellbird_plugin.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/api/myext/hello")
async def hello():
    return {"hello": "world"}


async def sync(ctx):              # ctx.config, ctx.state (a StateManager)
    ...


def configure(parser):            # add arguments, return the function to run
    parser.add_argument("--dry-run", action="store_true")
    return lambda args: print("ran", args.dry_run)


async def warm_enough(check):     # check.item, check.prospect, check.config, check.state
    from sellbird.send_hooks import Hold
    return Hold("still warming") if check.cold and not await is_warm(check) else None


def install(registry):
    registry.add_router(router)
    registry.add_tick_step("myext.sync", sync)
    registry.add_cli_command("myext", configure, help="Run myext")
    registry.add_send_rule("myext.warm", warm_enough)
    registry.add_send_headers("myext.unsubscribe",
                              lambda item: [("List-Unsubscribe", "<mailto:stop@example.org>")])
    # Inboxes whose `connection` is "myext" send and read through your MailProvider.
    registry.add_mailbox_connection("myext", lambda row, *, config, env, secrets: MyProvider(row))
```

## As regras

- **As extensões carregam uma vez por processo,** no primeiro uso, na ordem do
  nome do entry point.
- **Um `install` que falha para o Sellbird, citando o nome da extensão.** Ele nunca
  roda com meia extensão instalada.
- **As etapas de tick são isoladas.** Uma etapa que levanta exceção ou passa de dois
  minutos é registrada e ignorada. Ela nunca para o heartbeat nem as outras etapas.
- **Nomes são palavras curtas em minúsculas:** letras, dígitos, `.`, `_` ou `-`.
  Prefixe etapas de tick com o nome da sua extensão (`myext.sync`).
- **Extensões são código confiável.** Elas rodam no processo do Sellbird, com o
  acesso do Sellbird aos seus dados e chaves. Instale só o que você instalaria
  como qualquer outro pacote Python.

## Rodando o Sellbird para outra pessoa

`sellbird.dashboard.build_app(guard=, routers=)` retorna um novo app que
serve todas as rotas nativas, com seus routers primeiro e seu próprio middleware de login
no lugar do token do dashboard. Defina `app.state.home` como um
`sellbird.workspace_home.Home`, e cada requisição roda com os arquivos e o banco
desse home. Recursos que só fazem sentido no computador do próprio usuário chamam
`require_self_hosted()`, que responde `409` em um home hospedado.
