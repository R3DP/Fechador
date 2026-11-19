# Configuração e comandos

## Configuração

Dois arquivos, ambos texto puro.

**`.env`** — credenciais. Cada variável documentada junto com onde obtê-la. A única obrigatória é um provedor de e-mail; todo o resto é opcional.

**`sellbird.yaml`** — quem o Sellbird é e para quem ele vende:

```yaml
persona:      { name, company, role, email, tone }
product:      { name, description, pricing, key_benefits, objection_responses, offer }
icp:          { industries, titles, company_size, geography, hiring_signals, geo_coordinates }
channels:
  email:      { provider: gmail | microsoft | smtp | instantly, max_daily_sends, per_inbox_daily_cap,
                require_approval, send_to_risky, min_write_score, max_bounce_rate, follow_ups, warmup, send_window, signature }
usage:        { max_daily_claude_percent, heartbeat_interval_minutes, quiet_hours }
brain:        { provider: claude | codex, model, reasoning_effort }   # opcional; claude por padrão
writer:       { humanizer, site_facts, require_tip }   # opcional; humanizer true adiciona uma passada de edição por lote usando ~/.claude/skills/humanizer/SKILL.md
              # site_facts (padrão true): o Writer vê o que os sinais gratuitos da homepage encontraram (sem dados estruturados,
              # um site desatualizado ou muito pequeno, rastreadores de IA bloqueados) para um e-mail poder citar uma coisa concreta a mudar.
              # Eles vêm de uma leitura automatizada de uma página e podem estar errados, então confira a afirmação de um rascunho
              # contra o site antes de aprová-lo. false os mantém longe do Writer.
              # require_tip (padrão false): true escreve um primeiro e-mail só para um prospect com algo concreto no qual
              # basear sua dica (uma descoberta do site, um fato de startup, um sinal ou as notas do Scout). Os demais são
              # marcados como "no_tip" e pulados, em vez de receberem um rascunho que diz não ter conselho. O dashboard os mostra
              # como "Nothing to write about yet"; `sellbird retry-writes --no-tip` os devolve à fila.
              # email_rules: suas próprias regras markdown para o formato dos e-mails (veja The skills library)
```

`min_write_score` (0-100, padrão 0) é a menor pontuação de aderência do Scout para a qual o writer
redige: um prospect abaixo dela mantém seu endereço entregável mas não recebe
sequência, então chamadas ao Claude e envios vão para as melhores correspondências primeiro.

`follow_ups` (padrão true) definido como `false` faz uma campanha escalonar apenas seu primeiro e-mail no Gmail, Microsoft e SMTP. Os passos 2 e 3 nunca são preparados, então nenhum pode sair para alguém que não respondeu. Uma resposta ainda é lida, e a resposta espera na Caixa de saída para você, como de costume. O Writer ainda redige a sequência inteira; o Sender apenas não escalona os passos posteriores.

`max_daily_claude_percent` limita a assinatura que `brain.provider` usar (o nome é anterior ao suporte ao Codex).

Se `sellbird.local.yaml` existir, ele ganha. Está no gitignore, então um fork pode carregar configuração real de produto enquanto o `sellbird.yaml` versionado continua um template — ninguém publica seu posicionamento e preço por acidente.

### Comandos

```bash
sellbird run                   # the heartbeat loop
sellbird dashboard             # web UI at 127.0.0.1:5555 (--url: print the unlock link)
sellbird signals               # review/confirm what to prospect against
sellbird discover              # find businesses; --providers / --estimate
sellbird profile               # read discovered companies' sites (free)
sellbird train <url>           # learn a product from its website (--provider codex --model gpt-5.5)
sellbird status                # pipeline summary
sellbird usage                 # active provider's quota + per-agent tokens
sellbird outbox                # review queued email
sellbird export                # deliverable prospects → CSV
sellbird precleared-key        # free key for the cold-email check, saved to .env
sellbird companies             # company register → CSV: every company, fit, and why it wasn't contacted
sellbird sending pause|resume  # kill switch
sellbird suppressions [add|remove <value>]  # addresses and domains never emailed
sellbird inboxes list|connect|test|pause|resume|cap|name|remove|use  # several sending inboxes
sellbird tray                  # menu-bar (macOS) / tray (Windows) icon; --status prints the state
sellbird autostart install|uninstall|status  # start the tray at login
sellbird mcp install [claude|codex]  # let your coding agent read Sellbird and pause sending
sellbird warmup [domain]       # is the sending domain ready? (SPF/DKIM/DMARC, age, blocklists, warmup)
sellbird trulyinbox connect    # connect TrulyInbox so Sellbird reads the mailbox's warmup
sellbird retry-writes          # retry prospects the Writer gave up on
sellbird gmail auth            # one-time Gmail OAuth
sellbird microsoft auth|test  # one-time Microsoft 365 sign-in (docs/microsoft365.md)
```

Exportações CSV de prospects excluem contatos que pediram descadastro, inclusive ao usar
os filtros `--status` ou `--email-status`. `sellbird export --all` é uma exportação de dados
brutos sem filtro, para inspeção: inclui contatos descadastrados e não verificados
e não deve ser importada como lista de contato. O download CSV de prospects do dashboard
segue a mesma política; `?all=true` seleciona sua exportação bruta.

## Várias caixas de envio

A caixa principal é a que `channels.email.provider` configura. Você pode enviar
de mais caixas que já possui, além dela:

```bash
sellbird inboxes connect gmail --address two@yourdomain.co      # login pelo navegador
sellbird inboxes connect microsoft --address three@yourdomain.co
sellbird inboxes connect smtp --address four@yourdomain.co --smtp-host smtp.example.com
sellbird inboxes list                                           # cada caixa e os envios frios de hoje
```

- **Onde ficam os logins.** No keychain do seu sistema (serviço `sellbird`), nunca
  no banco ou em um arquivo. Uma caixa Gmail ou Microsoft guarda apenas seu refresh
  token; a senha de uma caixa SMTP é pedida no prompt, nunca na
  linha de comando. Entrar com uma conta diferente de `--address` não conecta
  nada. Docker e outras máquinas headless não têm keychain, então caixas extras
  não podem ser conectadas ali ainda.
- **Qual caixa envia o quê.** O primeiro e-mail de um prospect sai da caixa
  com mais espaço restante hoje. Depois que algo numa thread saiu, seus
  follow-ups e as respostas do Sellbird saem da mesma caixa. Uma resposta é
  respondida a partir da caixa em que chegou.
- **Tetos.** Cada caixa, inclusive a principal, envia até
  `per_inbox_daily_cap` e-mails frios por dia (padrão 30), ou o número que você definir
  com `sellbird inboxes cap <address> <n>`. Uma caixa conectada com
  `--warmup-started YYYY-MM-DD` sobe a partir daquele dia como
  `channels.email.warmup` descreve; a caixa principal sobe a partir de
  `warmup.start_date`. `max_daily_sends` continua sendo o teto de tudo enviado
  num dia, então aumente-o quando adicionar caixas.
- **Pausar e remover.** `sellbird inboxes pause <address>` para uma caixa.
  Seus primeiros e-mails não enviados se movem para as outras, e threads que ela
  iniciou esperam por ela. `remove` para de usá-la de vez: threads que ela
  iniciou terminam. Seu login permanece no keychain até você apagá-lo lá.
- **Escolher caixas por campanha.** `sellbird inboxes use <campaign>
  <address>...` limita as novas threads de uma campanha a essas caixas (`main` é
  a caixa principal); sem endereços, usa todas as caixas novamente.
- Respostas são lidas de todas as caixas a cada ciclo. Se uma não puder ser lida,
  nada é enviado naquele ciclo, como com uma só caixa, e a aba Hoje diz
  qual caixa.
- A aba **Caixas de entrada** do dashboard mostra cada caixa com os envios frios de hoje
  contra seu teto. Clique numa para pausar, retomar, definir teto, renomear, verificar ou remover.
  **Adicionar caixa de entrada** conecta uma: Gmail e Microsoft 365 abrem o login
  no navegador do computador que roda o Sellbird (precisa da mesma
  configuração `GMAIL_CLIENT_ID`/`M365_CLIENT_ID` da caixa principal), e uma senha SMTP
  vai direto para o keychain do seu sistema e nunca é mostrada de novo.
  Num servidor sem navegador, use `sellbird inboxes connect`.
- Seu agente de código pode listar caixas e pausar uma (`inboxes_list`,
  `inbox_pause`); só você retoma uma ou muda seu teto.
- Uma extensão pode adicionar outra forma de conectar uma caixa com
  `registry.add_mailbox_connection` ([docs/extensions.md](extensions.md)).

## O app da barra de menu

`sellbird tray` coloca o Sellbird na barra de menu do macOS (a bandeja do Windows). Ele
inicia o dashboard se ele não estiver rodando, e então deixa você iniciar e parar o
Sellbird, pausar e retomar o envio, e abrir o dashboard, já desbloqueado.
Sair do ícone deixa o Sellbird rodando. `sellbird autostart install` inicia
o ícone quando você faz login: um LaunchAgent no macOS, um atalho na pasta Inicializar no
Windows. Ele só mexe na própria entrada e recusa se houver outra coisa
naquele caminho. O Linux não tem bandeja: rode `sellbird dashboard` e `sellbird run`
como serviços.

## Seu agente de código (MCP)

`sellbird mcp install` adiciona o Sellbird ao Claude Code (`sellbird mcp install codex`
para Codex). Ele mostra primeiro a mudança exata na configuração do seu agente e a aplica
só com um sim, mexe apenas na própria entrada e recusa se já houver uma entrada do Sellbird
que ele não escreveu. `--print` mostra a entrada para adicionar à mão em qualquer
outro cliente MCP; `sellbird mcp uninstall` a remove de novo.

Seu agente então fala com o dashboard em execução (`sellbird dashboard`) com seu
próprio token, `data/agent-token`, nunca o seu. Com ele o agente pode ler
tudo o que o Sellbird sabe (Hoje, campanhas, contatos, empresas, conversas, a Caixa de saída, sinais, uso, setup), estimar o que uma execução de discovery
custaria e pausar o envio. Ele não pode aprovar ou enviar e-mail, retomar
o envio, confirmar sinais, iniciar discovery, mudar configurações ou chaves, ou apagar
nada: o dashboard responde 403 ao token do agente para toda rota que
não está na sua pequena allowlist (`sellbird/agent_policy.py`).
