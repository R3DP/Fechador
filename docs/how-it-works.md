# Como o Sellbird funciona

## Por que a história da assinatura importa

Todo outro agente de vendas autônomo cobra por token. É exatamente por isso que custam o
que custam: um agente que pensa em laço, o dia todo, é um agente que queima créditos de API
em laço, o dia todo. Os fornecedores resolvem isso pensando menos — prompts mais curtos,
modelos mais baratos, menos passadas.

O Sellbird usa a CLI respaldada por assinatura do provedor que você escolher: `claude`
para o Claude Code, ou um `codex app-server` isolado para o Codex. Ambos retornam texto
com as ferramentas do modelo desativadas. O Sellbird cuida da prospecção e das operações
de e-mail por conta própria.

As chamadas do Claude rodam sem nada da sua configuração própria do Claude Code: sem
`CLAUDE.md` (seu, do projeto ou de qualquer pasta pai), sem hooks, skills, plugins,
servidores MCP ou arquivos de configuração, sem ferramentas, em uma pasta temporária
vazia, e nada é salvo nos seus transcripts do Claude. Seu login (assinatura ou
`claude setup-token`) e qualquer política gerenciada pelo admin continuam valendo. Isso
exige uma CLI do Claude com `--safe-mode`; com uma mais antiga, o Sellbird pausa em vez
de enviar prompts sem isolamento e pede para rodar `claude update`. Para verificar isso
offline na sua CLI instalada, sem credenciais nem rede: `SELLBIRD_CLAUDE_CLI_TESTS=1 pytest tests/test_claude_cli_isolation.py`.

A assinatura que você selecionou cobre as chamadas ao modelo, sujeitas aos limites de uso
dela. Isso permite ao Sellbird usar sua biblioteca de skills para personalização e
tratamento de respostas sem uma conta separada de API de modelo.

**O que isso custa para você:**

| | |
|---|---|
| Claude Pro/Max ou um plano ChatGPT com acesso ao Codex | sua assinatura atual |
| Encontrar empresas | **$0** na fonte padrão, ou ~$0,37 por 1.000 na paga mais barata |
| Ler os sites delas | **$0** — três requisições HTTP cada, sem chamada a modelo |
| Escrever e enviar | sua assinatura + uma caixa de e-mail (~$7/mês Google Workspace) |
| Ferramentas de prospecção | **nenhuma.** Sem Apollo, sem ZoomInfo, sem Clearbit, sem Clay. |

Para comparar, as ferramentas que o Sellbird substitui começam em $250–500/mês — e são
mais fracas exatamente onde o Sellbird é mais forte: pequenos negócios locais com 5–50
pessoas, onde a cobertura de contatos de um único provedor para por volta de 30% e
microempresas costumam estar totalmente ausentes.

**O Sellbird também se orça.** Ele lê a cota da assinatura do provedor ativo e se limita
para deixar folga para o seu próprio trabalho no Claude ou Codex. Defina
`max_daily_claude_percent: 80` para qualquer provedor — o nome da configuração é anterior
ao suporte ao Codex. Se a cota não puder ser lida, o Sellbird a reporta como indisponível
e volta ao seu orçamento diário de chamadas.

O Sellbird roda localmente com o seu próprio login. Confira os termos e limites de uso do
provedor que você escolher.

---

## O que o Sellbird realmente faz

O Sellbird roda um heartbeat: acorda, confere o orçamento, decide o que mais precisa ser
feito, faz, registra, dorme. A cada 15 minutos por padrão.

```
                 ┌──────────────────────────────────────┐
                 ↓                                      │
   Wake  →  Quiet hours?  →  Budget OK?  →  Decide  →  Act  →  Log  →  Sleep
                 │               │
              (sleep)         (sleep)
```

Ele decide de forma determinística, sem perguntar a um modelo o que fazer — isso queimaria
uma chamada com algo que pode ser derivado de quatro contagens:

```
handle replies  >  send campaigns  >  write campaigns  >  prospect  >  idle (analyze)
```

A criação de perfil e o esvaziamento da caixa de saída acompanham **todo** ciclo, de
qualquer forma, porque não custam nada e precisam acontecer no prazo.

## Estrutura do projeto

```
sellbird/
├── main.py              # heartbeat loop
├── brain.py             # Claude/Codex provider selection + skills + usage
├── claude_runtime.py    # Isolated Claude CLI calls (safe mode, no tools, clean dir)
├── codex.py             # Isolated Codex subscription runtime
├── state.py             # SQLite schema, migrations, observations, cohorts
├── signals.py           # the 23-signal catalog Sellbird proposes
├── pipeline.py          # DISCOVER → PROFILE chaining
├── gate.py              # deterministic pre-send checks
├── dashboard.py         # FastAPI JSON API
├── dashboard_auth.py    # dashboard token, Host/Origin checks
├── collectors/
│   ├── discover.py      # provider adapters, junk filtering, entity resolution
│   └── profile.py       # the free HTTP profiler
├── agents/              # scout, writer, sender, handler, analyst
├── integrations/        # mail providers, email finder, quota
└── web/                 # dashboard HTML/CSS/JS — no build step

skills/                  # ← the sales knowledge. Editable Markdown.
prompts/                 # ← agent system prompts. Also editable Markdown.
tests/                   # 242 tests
```

---

## Filosofia

**Autônomo não significa sem supervisão.** Horário de silêncio, tetos de gasto, limites
de envio, uma fila de aprovação, um bloqueio determinístico antes do envio e um kill
switch. O Sellbird pergunta antes de gastar e antes de enviar, até você dizer para não.

**Você decide o que é um bom prospect.** O Sellbird propõe sinais; você os confirma. Uma
lista de prospects que você não consegue explicar é uma lista de prospects para a qual você
não deveria enviar.

**Se dá para obter de forma determinística, não use um modelo.** Posição no ranking, detecção
de tecnologias, filtragem de lixo, a decisão de prioridade, o bloqueio antes do envio —
tudo código simples. Claude ou Codex fica reservado para as partes que exigem julgamento.
É por isso que isto roda em uma assinatura.

**Uma falha é uma observação, não silêncio.** "Nenhuma página de equipe encontrada" é um
achado. "O Overpass está limitando as requisições" é um achado. Falhas silenciosas
parecem exatamente com resultados limpos, e é assim que uma execução quebrada passa por
mercado vazio.

**O banco de dados é o ativo, não o agente.** A lista inicial vale pouco. Os mesmos sinais
observados ao longo de trimestres — quem trocou de agência, quem passou a gastar com
anúncios, quem deixou o conteúdo envelhecer — valem muito.

**Tudo é editável.** Prompts, skills, configuração, o dashboard. Tudo texto simples. Você
não precisa ser desenvolvedor para mudar como o Sellbird vende.
