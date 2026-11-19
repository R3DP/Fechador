# Solução de problemas

## Solução de problemas

**`command not found: sellbird`** — Rode `source .venv/bin/activate` primeiro.

**`ModuleNotFoundError: No module named 'sellbird'` após instalar (macOS)** — O Python 3.13 ignora silenciosamente arquivos `.pth` com a flag de arquivo oculto do macOS, e alguns Macs propagam essa flag para o `.venv`. Rode `sellbird install` de novo (ele corrige automaticamente), ou: `ln -s "$(pwd)/sellbird" .venv/lib/python3.13/site-packages/sellbird`

**`externally-managed-environment`** — Use um venv, não o Python do sistema.

**`SyntaxError` ou `ImportError` estranhos logo após instalar (macOS)** — Seu venv está em Python 3.9. `python3 -m venv` cria a partir de `/usr/bin/python3` (a versão que o macOS mantém em 3.9). Confira com `.venv/bin/python -V` e recrie: `rm -rf .venv && python3.13 -m venv .venv && source .venv/bin/activate && pip install -e .`

**O modo headless do Claude falha** — Rode `claude login` e confirme que a assinatura está ativa. Teste com `claude -p "say hi"`. No Docker, monte `~/.claude` no contêiner (gravável: a CLI renova o login ali). Se o log disser que a CLI do Claude "lacks --safe-mode" (ou outra flag), rode `claude update` (no Docker, reconstrua a imagem); o Sellbird retoma sozinho. Se o seu login do Claude depende de entradas `env` ou `apiKeyHelper` nos seus arquivos de configuração do Claude, defina essas variáveis no ambiente do Sellbird: as chamadas do Sellbird não leem arquivos de configuração. `sellbird status --check` confirma a CLI sem enviar um prompt.

**O dashboard diz "locked"** — Abra o link que `sellbird dashboard` imprimiu (ou `sellbird dashboard --url`). Se a mensagem disser que o arquivo de token não pode ser usado, siga a instrução: normalmente, apague `data/dashboard-token` e reinicie o dashboard. Acesse como `127.0.0.1` ou `localhost`; outros nomes de host são recusados.

**As chamadas do Codex falham** — Leia a linha do log; todo erro do Codex diz o que fazer. "Not logged in" ou "expired or is due for renewal" → use o Codex uma vez ou rode `codex login` com o ChatGPT. "Hasn't been verified with Sellbird" → instale a versão do Codex suportada indicada na mensagem. "Isolation could not be verified" → uma camada de configuração do Codex fora do seu `~/.codex` (por exemplo, uma configuração gerenciada ou em `/etc/codex`) força de volta uma ferramenta, hook, servidor MCP, instrução ou endpoint personalizado; o Sellbird se recusa a enviar prompts até que ela seja removida. Erros de catálogo de modelos → escolha um ID de modelo disponível do catálogo mostrado na mensagem, ou deixe `brain.model` em branco para selecionar um modelo listado. O Sellbird nunca muda para o Claude por conta própria.

**A descoberta não encontra nada** — Confirme os sinais primeiro (`sellbird signals --confirm free`); nada é coletado até você fazer isso. Se você está na fonte gratuita OpenStreetMap, ela cobre apenas atividades mapeadas e é fraca para negócios de área de atendimento — `sellbird discover --providers` mostra as alternativas.

**O Overpass está limitando as requisições** — É infraestrutura voluntária e gratuita. O Sellbird percorre três espelhos antes de desistir. Espere alguns minutos ou use um provedor pago para trabalho em volume.

**Os e-mails caem em spam** — Quase sempre é o domínio, não o texto. Verifique SPF/DKIM/DMARC, confirme que o warmup rodou ([TrulyInbox](https://trulyinbox.com/?via=sellbird) mostra a taxa de caixa de entrada; `sellbird warmup` a lê depois que conectado), reduza o volume pela metade.

**O Sellbird não faz nada durante o dia** — Verifique `quiet_hours` e se ele atingiu `max_daily_claude_percent`. `sellbird status` mostra o estado atual; a tabela `actions` registra cada decisão.

**Como paro agora mesmo?** — `Ctrl+C`, ou `sellbird sending pause` para parar o envio sem parar o laço. O estado fica no SQLite, então ele retoma limpo.

**Onde ficam meus dados?** — Tudo local: `data/sellbird.db`, `.env`, `sellbird.yaml`. Nada vai a lugar algum exceto pelas APIs que você configurou.
