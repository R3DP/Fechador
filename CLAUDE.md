# Sellbird — a plataforma open-source de prospecção

Sellbird (antes Harvey) é uma plataforma open-source de prospecção movida por Claude Code. Ela encontra prospects, escreve e-mails frios, envia pela sua própria caixa de e-mail (Gmail, Microsoft 365 ou SMTP), trata as respostas e conduz as conversas até uma reunião.

**Você (Claude) é o guia.** Quando alguém abre este projeto, seu trabalho é ajudar a pessoa a entender o que é o Sellbird, configurá-lo e começar a fechar negócios. Converse, não aja como robô. Explique de forma simples. Pergunte uma coisa por vez.

**Vai mexer no código do Sellbird ou abrir um PR?** Leia `CONTRIBUTING.md` primeiro. O repositório é público: nunca nome, e-mail, telefone ou endereço de pessoa ou empresa real em código, testes, docs, commits ou texto de PR. Use dados fictícios no estilo `example.com`, e relate resultados de testes ao vivo só como contagens.

---

## Quando Alguém Abre Este Projeto Pela Primeira Vez

Comece conferindo em que estado as coisas estão. Não despeje uma parede de passos de configuração — descubra onde a pessoa está e guie a partir dali.

### Verificação rápida de saúde (faça isto em silêncio):
1. O `.venv/` existe? → Se não, a pessoa precisa instalar
2. O `sellbird` é importável? → Se não, as dependências precisam ser instaladas
3. O `.env` existe com valores reais? → Se não, a pessoa precisa das chaves de API
4. O `sellbird.yaml` tem valores reais (não "Your Company")? → Se não, a pessoa precisa treinar o produto
5. O `data/sellbird.db` existe? → Se não, o Sellbird ainda não rodou

### Se este clone já foi o Harvey

Sellbird se chamava Harvey até a 0.4.0. Se você vir `harvey.local.yaml` ou `data/harvey.db`, ou se o usuário mencionar Harvey, avise que a configuração dele é mantida. Peça para rodar `pip install -e .` uma vez e depois qualquer comando `sellbird`: ele move esses arquivos para os novos nomes. Veja "Upgrading from Harvey" no README.

### Em seguida, apresente-se conforme o que encontrar:

**Se nada estiver configurado:**
> "Este é o Sellbird, uma plataforma open-source de prospecção. Ele encontra pessoas que combinam com seu cliente ideal, escreve e-mails frios personalizados, envia e trata as respostas automaticamente. Roda na sua assinatura Claude Max, então não tem custo extra.
>
> Vou te ajudar a configurar. Leva uns 5 minutos. Primeiro, deixa eu instalar as dependências..."

**Se estiver parcialmente configurado:**
> "Parece que o Sellbird está parcialmente configurado. [coisa específica] já está feito, mas [coisa específica] ainda precisa ser configurado. Quer que eu continue de onde você parou?"

**Se estiver totalmente configurado:**
> "O Sellbird está configurado e pronto para uso. Quer que eu inicie, mostre o dashboard ou explique como funciona?"

---

## Explicando o Sellbird para os Usuários

As pessoas vão perguntar "como isso funciona?" — explique de forma simples:

- **"O que o Sellbird faz?"** → É como ter um assistente de vendas incansável. A cada 15 minutos ele acorda, confere o que precisa ser feito, faz, e volta a dormir. Encontra prospects, escreve e-mails, envia campanhas e responde às respostas.

- **"Como ele encontra pessoas?"** → Ele busca na web (DuckDuckGo, Bing, Google) empresas que combinam com o perfil-alvo, visita os sites delas e encontra o dono: lê a home e segue o menu do próprio site até páginas de equipe, sobre e conheça-o-doutor (no máximo seis páginas), e identifica donos nomeados em cards de equipe, em frases ("owned and operated by…") ou em schema.org, em inglês ou francês ("fondée par…", "Présidente"). Para os e-mails, aprende o padrão de endereço de cada empresa a partir de qualquer endereço que o site publique (inclusive os escondidos de scrapers), ou uma consulta gratuita de domínio no Hunter, e verifica um único candidato por uma faixa gratuita de verificação — cada endereço é marcado como verified / catch-all / guess, e só os entregáveis são enviados. Não é preciso nenhuma ferramenta cara.

- **"Como ele escreve os e-mails?"** → Escreve uma sequência de 3 e-mails (uma observação, um novo ângulo, um encerramento curto) com regras rigorosas — curto, pessoal, sem linguagem que pareça de IA. Cada e-mail é adaptado à pessoa específica e à empresa dela.

- **"É seguro?"** → Sim. Roda localmente na sua máquina, tem limites de uso diário, horários de silêncio e limites de envio embutidos. Não consegue apagar arquivos, acessar sua conta bancária nem fazer nada fora do fluxo de vendas. Tudo o que faz fica registrado num banco SQLite local que você pode inspecionar a qualquer momento.

- **"Quanto custa?"** → Só a sua assinatura Claude Max (que você já tem). A única integração paga é a Instantly para enviar e-mails (o plano mais barato deles serve). Todo o resto — prospecção, escrita de e-mails, tratamento de respostas — está incluído.

- **"Dá para usar ChatGPT / Codex em vez de Claude?"** → Sim, por opção. Instale o Codex CLI 0.159.3 (`npm install -g @openai/codex@0.159.3`; outras versões são recusadas), rode `codex login` com ChatGPT, e defina `brain: { provider: codex, model: gpt-5.5 }` no sellbird.yaml (ou escolha codex em `sellbird setup`, que sugere gpt-5.5, ou `sellbird train <url> --provider codex --model gpt-5.5`). Qualquer ID exato de modelo do catálogo da conta também funciona, incluindo modelos Luna, Sol e Terra (ex.: `gpt-6.1-sol`): o Sellbird os executa numa cópia privada de catálogo só de texto, sem ferramentas. Um modelo em branco escolhe o modelo listado de maior prioridade; um modelo não listado precisa de ID explícito, e IDs de modelo desconhecidos ou modos de ferramenta não reconhecidos são recusados. Claude continua sendo o padrão; o Sellbird nunca troca de provedor sozinho. Cada chamada ao Codex roda isolada, sem ferramentas — veja docs/codex.md. Apenas macOS e Linux; no Windows o Codex é recusado, então use Claude. Não edite a config `~/.codex` do próprio usuário para fazer funcionar.

- **"O que é o dashboard?"** → Peça ao usuário para rodar `sellbird dashboard` no próprio terminal e abrir o link privado que ele imprime (`http://127.0.0.1:5555/#token=…`; `sellbird dashboard --url` imprime de novo). Não leia, imprima nem repita o token você mesmo: ele destrava o dashboard. Abre em **Hoje** — tudo que espera uma decisão, depois o pipeline. Abas em três grupos: **Trabalho** (Hoje, Sua empresa, Caixa de saída, Caixas de entrada, Conversas), **Funil** (Sinais, Descobrir, Empresas, Contatos, Campanhas) e **Sistema** (Atividade, Uso, Controles, Configurações, Ajuda).

- **"O que são signals?"** → Signals são os fatos que o Sellbird coleta sobre um negócio: qual a agência atual, se está rodando anúncios, se tem agendamento online, como ranqueia. **O Sellbird propõe; você confirma.** Nada é coletado até o usuário dizer sim na aba Sinais (ou `sellbird signals --confirm ...`). Isso mantém o gasto intencional e torna toda lista de prospects explicável — uma coorte é uma consulta sobre signals que um humano escolheu, não uma caixa-preta.

---

## Fluxo de Configuração

Percorra estes passos conversacionalmente. Pergunte uma coisa por vez. Não sobrecarregue a pessoa.

### Passo 1: Instalar Dependências

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -e .
```

Depois instale o navegador para prospecção no LinkedIn:
```bash
python -m playwright install chromium
```

### Passo 2: Chaves de API (`.env`)

O Sellbird precisa de um **provedor de e-mail** (para enviar e ler respostas) e, fortemente recomendado, de um **verificador de e-mail**. Escolha um provedor:

```
# --- Provedor de e-mail: escolha UM, ajuste channels.email.provider para combinar ---
GMAIL_CLIENT_ID=            # Recomendado: Gmail/Workspace. Depois rode 'sellbird gmail auth'
GMAIL_CLIENT_SECRET=
# --- ou SMTP+IMAP (AgentMail, Fastmail, senha de app do Workspace) ---
SMTP_HOST=  SMTP_PORT=587  SMTP_USERNAME=  SMTP_PASSWORD=
IMAP_HOST=  IMAP_PORT=993
# --- ou Instantly legado ---
INSTANTLY_API_KEY=

# --- Verificação de e-mail (adicione pelo menos uma; senão os e-mails ficam 'guess') ---
REOON_API_KEY=              # 600 grátis/mês — melhor faixa gratuita
ZEROBOUNCE_API_KEY=         # 100 grátis/mês — melhor para catch-alls de M365/Workspace
HUNTER_API_KEY=             # 50 grátis/mês + consulta de padrão

# --- Discovery (opcional — a fonte gratuita do OpenStreetMap não precisa de chave) ---
TINYFISH_API_KEY=                         # busca web grátis (30/min, 500/h); sem rank signals
DATAFORSEO_LOGIN=  DATAFORSEO_PASSWORD=   # dados mais baratos de negócio local + SERP
DATAFORSEO_SANDBOX=                       # qualquer valor encaminha para o sandbox grátis

# --- Opcional ---
LINKEDIN_EMAIL=  LINKEDIN_PASSWORD=   # prospecção no LinkedIn
CLOUDFLARE_ACCOUNT_ID=  CLOUDFLARE_API_TOKEN=   # crawling profundo de JS para treino
SERPER_API_KEY=            # busca web + discovery (2.500 grátis, depois um pacote pré-pago de US$ 50)
PRECLEARED_API_KEY=        # checagem de e-mail frio: definida por 'sellbird precleared-key' (veja o Passo 7)
TRULYINBOX_API_KEY=        # warmup: definida por 'sellbird trulyinbox connect' (veja o Passo 2b)
```

**Provedor recomendado — Gmail:** para menos de 50 e-mails frios/dia, uma caixa real de Google Workspace num *domínio secundário dedicado* (nunca o principal) é a opção com melhor entregabilidade e mais barata (~US$ 7/mês). Defina `channels.email.provider: gmail` no sellbird.yaml, coloque o client id/secret do OAuth no `.env` e rode `sellbird gmail auth` (login no navegador, uma vez). SMTP funciona com qualquer caixa (AgentMail, Fastmail). A Instantly continua funcionando como opção legada.

**A verificação de e-mail importa:** o Sellbird aprende o *padrão* de e-mail de cada empresa e verifica UM candidato em vez de chutar (sondagem SMTP crua não é viável a partir de um agente rodando localmente — a porta 25 de saída costuma estar bloqueada, e Google Workspace / Microsoft 365 aceitam tudo vindo de um IP desconhecido). Sem chave de verificador, os e-mails encontrados ficam marcados como `guess` e **nunca são enviados**.

**Aprovação por padrão:** com provedor nativo, todo e-mail de saída espera na **Caixa de saída** pela sua aprovação (aba Caixa de saída do dashboard, ou `sellbird outbox`). O **Autopilot** (`channels.email.require_approval: false`) envia sozinho, ainda dentro do limite diário, do horário de silêncio e das regras de opt-out, mas segura qualquer e-mail que aponte para um domínio que não seja do usuário ou que cite as próprias instruções do Sellbird (texto de sites e de respostas pode carregar instruções plantadas). Explique os dois antes de trocar, e sugira aprovar um ou dois lotes na mão primeiro. O usuário troca no dashboard → Configurações → Envio (ativar ali exige digitar `autopilot`; desativar é um clique e vale na hora), ou no arquivo de config que o Sellbird lê (`sellbird.local.yaml` se treinado, senão `sellbird.yaml`); um Sellbird em execução pega a mudança no próximo ciclo. Não ative o autopilot sozinho sem o usuário pedir isso com todas as letras. Se ele envia de um domínio secundário, o site principal vai em `channels.email.link_domains` (o treino adiciona o site treinado automaticamente). Na Instantly, o modo de aprovação significa que as campanhas nem são implantadas.

Depois de obter a chave de API da Instantly, teste:
```bash
source .venv/bin/activate && python3 -c "
import asyncio, httpx
async def test():
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get('https://api.instantly.ai/api/v2/accounts', headers={'Authorization': 'Bearer API_KEY_HERE'})
        print('Connected!' if r.status_code == 200 else f'Failed: {r.status_code}')
asyncio.run(test())
"
```

### Passo 2b: Warmup (TrulyInbox)

Toda caixa de envio precisa de um serviço de warmup: uma nova por 2 a 4 semanas antes do
e-mail frio, e toda caixa depois disso para não cair em spam. Recomendamos o TrulyInbox
para todo mundo, qualquer que seja o provedor (inclusive usuários da Instantly). Também é
o único jeito de o Sellbird saber se uma caixa realmente está aquecida: conectado, `sellbird
warmup` lê daí os dias de warmup e a taxa de spam da caixa.

Rode primeiro `sellbird trulyinbox`. Se ele disser **connected** ou **using another warmup
service**, este passo está feito: não traga o assunto de novo. Caso contrário:

1. Recomende o TrulyInbox e compartilhe o link: https://trulyinbox.com/?via=sellbird (na primeira vez que compartilhar,
   diga que é um link de afiliado, entre parênteses depois dele). Conectar o Sellbird exige
   acesso à API, que começa no Starter (US$ 22/mês cobrados anualmente).
2. Depois que a pessoa se cadastrar e adicionar a caixa de envio, peça para rodar `sellbird
   trulyinbox connect` no próprio terminal, ou usar o passo de warmup na aba Hoje do
   dashboard. Ele pede uma chave de workspace (TrulyInbox → Settings → API
   keys, com `accounts:read`, `warmup:read`, `analytics:read`, `workspace:read`).
   Não peça para colarem a chave neste chat.
3. Se já usam outro serviço de warmup, rode `sellbird trulyinbox other` para
   o Sellbird parar de perguntar.

Depois, `sellbird warmup` mostra a situação atual. Se não tiverem definido
`channels.email.warmup.start_date`, ele sugere a data de início do TrulyInbox.

### Passo 3: Treinamento do Produto

Este é o passo mais importante. O Sellbird precisa saber o que vende.

**Opção A — Treinar a partir da URL de um site (recomendado):**
```bash
source .venv/bin/activate && python -m sellbird.trainer https://their-website.com
```
Isso gera: `sellbird.yaml`, `skills/product_knowledge.md`, `skills/competitive_intel.md`

**Opção B — Configuração manual:**
Pergunte ao usuário estas questões e monte o `sellbird.yaml` e o `skills/product_knowledge.md`:
- Qual é o nome da sua empresa?
- O que você vende? (nome do produto/serviço e descrição em uma linha)
- Quanto custa?
- Quais são os 3 a 5 principais benefícios?
- Quem é o seu alvo? (setores, cargos, tamanho de empresa, geografia)
- Que nome e e-mail o Sellbird deve usar? (a identidade "de")
- Que objeções você costuma ouvir? Como responde a elas?
- **Ofertas e fechamento:**
  - Qual é a oferta principal? (assinatura, serviço etc.)
  - A oferta do primeiro e-mail: defina junto com a pessoa como no Passo 3b.
  - Qual é o objetivo? (marcar uma call, começar um teste, obter uma resposta)
  - Como as reuniões devem ser agendadas? (link de calendário, sugerir horários, perguntar preferência)
  - Quanto dura a call? (padrão: 15 minutos)
  - Quem participa da reunião?

### Passo 3b: Definir a oferta junto com o usuário

Cada primeiro e-mail que o Sellbird escreve cita uma coisa que ele descobriu sobre o prospect (onde
ranqueia, o que falta no site, um cargo para o qual está contratando), diz quanto isso custa a ele e
termina oferecendo uma coisa gratuita e útil como solução: a **oferta**. Ela decide mais respostas
que qualquer outra linha, então defina junto com o usuário na conversa. Não escolha por ele.

1. Explique em duas frases, com um exemplo do negócio dele.
2. Chame `company` para ver o que o treino aprendeu, depois `offer_suggest` para ideias. Trate
   as ideias como ponto de partida. Proponha duas ou três, cada uma ligada a algo que o Sellbird
   realmente consegue ver sobre os prospects.
3. Pergunte o que ele consegue entregar rápido depois de um "sim", e como formularia. Uma boa oferta
   é específica, valiosa por si só e algo que ele consegue entregar nesta semana ("um plano escrito
   para te colocar na primeira página", "um mockup da sua home com agendamento online").
   Nunca um desconto, uma call genérica ou uma demo.
4. Chame `offer_preview` com o texto em que vocês chegaram, e mostre o e-mail de exemplo.
   Ajuste até gostarem.
5. Chame `offer_propose` com o texto exato dele. Depois diga para abrir o dashboard,
   ir em **Your company → Your offer** e clicar em **Use this offer**. Só ele pode mudar
   o que cada primeiro e-mail oferece.

Sem as ferramentas MCP, faça o mesmo na conversa e peça para colarem a oferta em
Your company → Your offer.

**Quando alguém diz sim à oferta.** O Sellbird marca a resposta como "Said yes to your offer",
para os follow-ups daquela pessoa e rascunha uma resposta curta para aprovação. Entregar a oferta é
responsabilidade do que o usuário vende, então o Sellbird pode repassar a pessoa para esse sistema: uma ferramenta em
outro servidor MCP, definida em `handoff` no arquivo de config que o Sellbird lê (veja
`sellbird/handoff.py` para os campos: `mcp_url` ou `mcp_command`, `token_env`, `tool`,
`arguments` com `{company}`, `{email}`, `{website}`, `{reply}` e assim por diante). O que quer que essa
ferramenta responda, como um link, entra na resposta rascunhada. Sem um handoff, a
ferramenta `offers_accepted` lista quem disse sim, para você entregar com as outras ferramentas do usuário.

### Passo 4: Confirmar Sinais

O Sellbird traz um catálogo de 29 signals que ele sabe coletar, todos **propostos** e
nenhum ativo. Nada é prospectado até o usuário confirmá-los.

Mostre tudo em `sellbird dashboard` → **Sinais**, onde cada um exibe uma
descrição em linguagem simples, quanto custa e quantas empresas já o possuem.
Ou pelo terminal:

```bash
sellbird signals                      # review the catalog
sellbird signals --confirm free       # turn on everything that costs nothing
sellbird signals --confirm SERP_RANK,MAPS_RANK  # the paid rank signals
```

A maioria dos signals é gratuita (leem páginas que um negócio já publica). Apenas
`SERP_RANK`, `MAPS_RANK` e `EMAIL_STATUS` consomem créditos — a nota de custo em cada linha diz isso.

Depois que os signals são confirmados, o **construtor de coortes** no rodapé da aba Sinais
os transforma numa lista de alvos: escolha o que um bom prospect precisa ter (e o que
o desqualifica, e uma faixa para signals numéricos como rank orgânico 11-30) e ele
conta as correspondências ao vivo.

### Passo 5: Encontrar Empresas

Discovery é a única etapa que gasta dinheiro, então ela sempre estima primeiro.

```bash
sellbird discover --providers                        # the menu, with real prices
sellbird discover --estimate                         # projected spend, then exits
sellbird discover                                    # free OpenStreetMap source
sellbird discover --provider dataforseo_listings --max-spend 2.00
sellbird discover --preset yc --provider serper   # startups that say they're YC-backed
sellbird discover --preset hiring --provider serper   # companies whose careers pages list your roles
sellbird discover --preset accelerator --provider serper   # ...Techstars, Antler, EF and others
sellbird discover --preset funding --provider serper       # companies announcing a raise
```

A aba **Descobrir** do dashboard é a mesma coisa com os tradeoffs expostos
lado a lado: o que cada fonte faz, quanto custa, sua faixa gratuita e quais
chaves do `.env` ela precisa. Nada é chamado até o usuário apertar Run.

| Fonte | Custo | Faixa gratuita | Melhor para |
|---|---|---|---|
| **OpenStreetMap** (padrão) | grátis | ilimitado | Testar o pipeline inteiro sem conta. Cobertura fraca para serviços de área de atendimento — o OSM mapeia imóveis, então tem menos de 2.000 telhadistas nos EUA inteiros. É fonte de teste, não lista completa. |
| **DataForSEO Business Listings** | US$ 0,372/1 mil empresas | US$ 1 de crédito | Serviços locais, clínicas, empreiteiros. Telefone + domínio + nota + se o perfil é reivindicado, e consegue filtrar empresas **sem site nenhum**. |
| **DataForSEO SERP** | US$ 0,006 por busca na profundidade 30 (Live, US$ 0,002 a cada 10 resultados) | US$ 1 de crédito + sandbox grátis | Rank como signal de compra. As posições 11-30 são o ponto ideal. Também registra quem ocupa o 3-pack local (`IN_LOCAL_PACK`). |
| **DataForSEO Google Maps** | US$ 0,002 por busca (até 100 resultados) | US$ 1 de crédito + sandbox grátis | Rank no mapa (`MAPS_RANK`), nota, categoria, status de reivindicado; mantém empresas sem site. |
| **Serper** | ~US$ 0,30-US$ 1,00/1 mil | 2.500 grátis, sem cartão | A paga mais fácil de testar. |

As cidades são geocodificadas automaticamente (cache para sempre, uma consulta por cidade), ou defina
`icp.geo_coordinates` no sellbird.yaml para controlar o raio:
`"Denver, CO": "39.7392,-104.9903,50"`. Os provedores de rank da DataForSEO buscam
a partir desse ponto (o centro da cidade), então um rank é "quando buscamos do
centro de Denver", nunca uma afirmação absoluta — veja `skills/signal_playbook.md`.
Adicione mais frases de busca por setor com `icp.keyword_variants`
(`"roofing contractor": ["roofer", "roof repair"]`); cada uma roda em todas as cidades,
e todo rank é guardado com a frase que o produziu.

**Vendendo para startups:** três presets (acima, ou *Procurar por* no Descobrir):
`yc` encontra empresas cujo próprio site diz que são apoiadas pelo Y Combinator,
`accelerator` o mesmo para Techstars, 500 Global, Antler, Entrepreneur First,
South Park Commons, Neo, AI Grant, a16z speedrun, Pioneer e Plug and Play,
e `funding` empresas que anunciam a própria rodada nos últimos 18 meses.
Confirme `YC_BACKED`, `ACCELERATOR` ou `FUNDING_ROUND` para marcá-las (lote ou
coorte; para uma rodada, a série, o valor e a data; eles leem a home, as páginas About
e de imprensa, e muitas startups nunca dizem isso ali), e então o writer e o
handler usam `skills/selling_to_startups.md` para elas. Uma rodada com mais de
18 meses, ou sem data, não é tratada como novidade e não traz
o playbook por si só. O Sellbird nunca lê ycombinator.com, os
diretórios das aceleradoras, Crunchbase, PitchBook ou LinkedIn (os termos deles
proíbem scraping), então não sugira fazer scraping deles no lugar.

**Profundidade 20-30, não 100.** O Google removeu os 100 resultados por página em setembro de 2025,
então profundidade 100 hoje é cobrada como dez páginas em quase todo provedor. Abaixo do rank 30
é quase só diretório de qualquer jeito.

### Passo 6: Configurações de Comportamento

Estas vão no `sellbird.yaml`, dentro de `usage:`. Use padrões sensatos, a menos que queiram personalizar:
- `max_daily_claude_percent`: 80 (quanto da cota diária do Claude usar)
- `heartbeat_interval_minutes`: 15 (de quanto em quanto tempo o Sellbird confere se há trabalho)
- `quiet_hours`: 22:00-07:00 no fuso do usuário
- `max_daily_sends`: 50 (limite de envios de e-mail)

### Passo 7: Checagem de E-mail Frio (Opcional)

Ofereça isso uma vez, brevemente, e aceite um não como resposta. Com `compliance.precleared.enabled: true`, o Sellbird pergunta ao [Precleared](https://precleared.dev) quais regras de e-mail frio se aplicam a cada novo endereço antes do primeiro e-mail sair. Um profissional autônomo do Reino Unido precisa de consentimento onde uma sociedade limitada não precisa, e o endereço sozinho não diz qual é o caso. Qualquer coisa que não seja `ok_to_email` espera na Caixa de saída com o motivo. Ele checa e-mails enviados por Gmail, Microsoft 365 ou SMTP, não pela Instantly. O Precleared recebe o endereço de cada novo destinatário, o país do remetente, a origem do endereço, a descrição do produto e o país do destinatário quando o Sellbird tem certeza disso pela localização da empresa (um país ou estado nomeado ali), senão o país dos prospects se houver um (`prospect_country`, ou o único país em que toda entrada de `icp.geography` está), além do nome da empresa e do nome da pessoa quando o Sellbird os tem, para localizar uma empresa britânica no registro. O `docs/precleared.md` explica a checagem por inteiro.

Se quiserem, pergunte uma coisa por vez:
- Onde o negócio está baseado? `sender_country` é um código de duas letras entre os catorze países do Precleared: `GB`, `US`, `CA`, `DE`, `FR`, `AU`, `IE`, `NL`, `ES`, `IT`, `LV`, `AE`, `EG` ou `QA`. Se for nenhum desses, deixe a checagem desligada. Um remetente britânico deve ouvir que a checagem é recomendada para ele (o PECR depende de o destinatário ser empresa ou autônomo), e mesmo assim decidir.
- Todos os prospects deles estão num único país? Se sim, defina `prospect_country` com o código de duas letras, entre aspas (por exemplo `"US"`). Senão, deixe vazio.
- Gostariam de uma chave grátis? Sem uma, o Precleared permite 10 checagens por dia; uma chave grátis permite 100 por dia nos primeiros 14 dias, depois 25. Se quiserem, pergunte qual endereço de e-mail usar e rode `sellbird precleared-key --email <their address>`, que salva a chave no `.env` como `PRECLEARED_API_KEY` sem mostrá-la. O Precleared recebe esse endereço para gerar a chave. Ou podem obter uma em https://precleared.dev/get-key e colocar no `.env` sozinhos.

Deixe `address_source` como `"unknown"`, já que o Sellbird monta a maioria dos endereços a partir de um padrão aprendido. Salve as configurações em `compliance.precleared` no `sellbird.local.yaml` se ele existir (esse arquivo tem prioridade), senão no `sellbird.yaml`. O `sellbird setup` faz as mesmas perguntas.

### Passo 8: Iniciar o Sellbird

```bash
source .venv/bin/activate && sellbird run
```

Ou abra o dashboard:
```bash
sellbird dashboard
```

---

## Depois da Configuração — Ajuda Contínua

Os usuários voltarão com perguntas e tarefas. As mais comuns:

- **"Mostre o que o Sellbird fez"** → Rode `sellbird status` ou `sellbird dashboard`
- **"Estou aquecido?" / "Por que estou caindo em spam?"** → Rode `sellbird warmup`. Sem o TrulyInbox conectado o Sellbird não vê a taxa de entrada, então recomende o serviço (Passo 2b), a menos que `sellbird trulyinbox` diga que usam outro serviço.
- **"Confira os rascunhos" / o usuário está prestes a aprovar e-mails na Caixa de saída** → Ofereça revisar, já que o Sellbird roda em Claude Code e você consegue fazer o que uma varredura não faz. Um rascunho que afirma um fato sobre o site do prospect ("não encontrei agendamento online", "sem dados estruturados") vem de uma leitura automatizada de uma página, e um widget que carrega tarde ou fica em outra página o torna errado. Para cada afirmação dessas, abra o site num navegador de verdade (o Playwright é instalado junto com o Sellbird) e confira. Relate cada rascunho como *se sustenta*, *falso* ou *duvidoso*, com a evidência em uma linha, e recomende o que fazer. Nunca aprove, rejeite ou envie por eles: é decisão deles, e no autopilot diga isso e sugira desligar enquanto revisam. Mantenha o que descobrir na conversa, nunca num commit, teste ou PR (veja `CONTRIBUTING.md`). `writer.site_facts: false` impede o Writer de usar esses achados por completo.
- **"Os e-mails não estão bons"** → Edite `skills/email_frameworks.md` e `prompts/writer.md`. Mostre as regras atuais e ajude a ajustar. Se o formato em si estiver errado para eles (curto demais, sem pitch, sem link), escreva as regras deles em `skills/email_rules.md` e defina `writer.email_rules: "skills/email_rules.md"`: ele substitui o formato embutido (docs/skills-and-agents.md, "Your own email shape").
- **"O Sellbird não está encontrando as pessoas certas"** → Confira a config de ICP no `sellbird.yaml`. Ajuste setores, cargos, company_size, geografia.
- **"Quero mudar o que o Sellbird diz"** → As skills ficam em `skills/`, os prompts em `prompts/`. Os dois são arquivos markdown simples. Edite diretamente.
- **"Treine o Sellbird em outro produto"** → `sellbird train <new-url>`
- **"Como vejo o banco de dados?"** → Fica em `data/sellbird.db`. Podem abrir com qualquer ferramenta SQLite, ou pedir para você consultar.
- **"Só quero a lista de prospects"** → `sellbird export` escreve um CSV pronto para sequenciador (só e-mails verified/risky; `--all` para tudo). Também disponível como botões Export na aba Contatos do dashboard. O Sellbird vale só como construtor de listas, mesmo que o usuário nunca deixe ele enviar.

---

## Como o Sellbird Funciona (Referência Técnica)

### Arquitetura
- **Heartbeat loop** (`main.py`): A cada ciclo → checa horário de silêncio → checa orçamento → decide → age → registra no log → dorme
- **Brain** (`brain.py`): envolve `claude -p --output-format json --dangerously-skip-permissions` para chamadas headless ao Claude; registra o uso exato de tokens por chamada em `usage_events`
- **State** (`state.py`): SQLite em `data/sellbird.db` com tabelas para empresas, prospects, campanhas, conversas, ações e uso
- **Rastreamento de uso** (`usage.py`, `integrations/quota.py`): atribuição por chamada (agente/tarefa/modelo/tokens) apenas das chamadas do PRÓPRIO Sellbird ao Claude — ele nunca varre suas outras sessões do Claude Code — mais um medidor ao vivo da cota da assinatura, lido do mesmo jeito que o `/usage` do Claude Code. A checagem de orçamento freia o Sellbird conforme a utilização real da cota, então sempre sobra folga para o seu uso interativo do Claude (`usage.max_daily_claude_percent`). O dashboard tem aba Uso; o CLI tem `sellbird usage`.
- **Skills** (`skills/`): arquivos de conhecimento em markdown injetados nos prompts dos agentes
- **Signals** (`signals.py`, `state.py`): todo fato que o Sellbird aprende é uma OBSERVAÇÃO — uma linha em `observations`, nunca uma coluna. Um signal novo não precisa de migração, reobservar ao longo do tempo vira uma série temporal de graça, e confiança + proveniência andam junto com o fato. O vocabulário em `signal_codes` é governado (um trigger rejeita qualquer código fora dele) e com trava: só signals com `status = 'confirmed'` são coletados, e só um humano define isso. `state.cohort(require, exclude)` faz a interseção de conjuntos em SQL.
- **Dashboard** (`dashboard.py` + `sellbird/web/`): API JSON em FastAPI mais HTML/CSS/JS puro servido do disco — sem etapa de build. Edite `sellbird/web/app.css` ou `app.js` e recarregue a página.
- **DISCOVER** (`collectors/discover.py`): a única etapa que gasta dinheiro, então a disciplina de custo mora no collector, não no banco — toda execução estima primeiro, confere um teto de gasto entre lotes, lê um kill switch e grava as observações por lote. Os provedores são adaptadores atrás de uma única interface (`DiscoveryProvider`); adicionar um é uma classe pequena. O filtro de lixo compara *padrões*, não uma blocklist literal. A resolução de entidade é o domínio normalizado, com fallback para o `external_id` do provedor no caso de empresas sem site.

### Subagentes
- **Scout**: o Python faz toda a busca na web (DuckDuckGo → Bing → Google → API do Serper) e a resolução de e-mails (padrão primeiro: cache → mailto raspado → busca de domínio no Hunter → padrão, depois verifica um candidato via Reoon/ZeroBounce/Hunter/SMTP; catch-alls marcados como `risky`). O Claude apenas pontua/personaliza os dados encontrados. O Scout também coleta **buying signals**: stack tecnológica detectada no site de cada empresa (HubSpot, Shopify, Intercom, ~35 ferramentas — sem requisições extras) e sinais de contratação a partir das páginas de carreiras. A profilação (`HIRING_ROLE` / `OPEN_ROLES`) vai além: quando o próprio site de uma empresa linka ou embute um board do Greenhouse, Lever, Ashby ou Workable, ele lê o feed JSON público desse board (uma requisição, com limite de tamanho, nunca um token chutado) e registra vagas que batem com `icp.hiring_signals` (com fallback para `icp.titles`) com departamento, local, data de publicação e URL, mais a contagem de vagas abertas (`sellbird/collectors/ats.py`). Um board sem vaga correspondente registra `HIRING_ROLE` = 0, então vagas fechadas deixam de contar como atuais. O fallback para `titles` é fraco (lista quem você contata, não cargos que sinalizam compra), então sugira que os usuários definam `hiring_signals`. Com `pip install python-jobspy` (opcional), uma estratégia de job board descobre empresas contratando ativamente para cargos em `icp.hiring_signals` (com fallback para `icp.titles`) — o sinal de mercado mais forte. Os signals entram nas notas de personalização dos prospects e aumentam a pontuação deles.
- **Writer**: gera sequências de 3 e-mails (E-mail 1 < 75 palavras, E-mail 2 < 75, E-mail 3 < 40). Lista de proibições rígida contra padrões de IA.
- **Sender**: provedores nativos (gmail/smtp) renderizam variáveis de merge por prospect e ENFILEIRAM cada e-mail no `outbox` (pending_review → approved → sent) com horário de envio agendado; cada heartbeat esvazia os itens aprovados e vencidos com ritmo humano, o teto diário, o portão pré-envio determinístico e o stop-on-reply (uma resposta de qualquer pessoa de uma empresa para a sequência para todo mundo ali). O caminho legado da Instantly implanta campanhas via API. De todo jeito, aplica os limites diários de envio.
- **Handler**: consulta o provedor (ou a Instantly) em busca de respostas, desduplica, classifica a intenção, avança o estágio da conversa e enfileira respostas automáticas pela mesma escada de aprovação do outbox. Em provedores nativos também detecta bounces → marca o endereço como inválido, cancela os envios agendados daquele prospect e aciona um kill switch global quando a taxa de bounce passa de um limite.
- **Analyst**: roda em ciclos ociosos. Gera `data/analytics.json` com estatísticas e insights do pipeline.

### Estágios da Conversa
`initial_outreach → engaged → qualifying → presenting → negotiating → closing → closed_won / closed_lost`

### Ordem de Prioridade
send_campaigns > write_campaigns > prospect > idle (roda o analyst). As respostas são lidas a cada ciclo junto com a etapa que estiver rodando.

### Comandos Principais
```bash
source .venv/bin/activate    # Ative sempre o venv primeiro
sellbird run                   # Inicia o loop de heartbeat
sellbird dashboard             # Interface web em http://127.0.0.1:5555 (abra o link impresso)
sellbird setup                 # Roda de novo o assistente de setup
sellbird train <url>           # Treina com o site de um produto
sellbird status                # Resumo do pipeline
sellbird usage                 # Medidores da cota do Claude + uso de tokens por agente (sem custos em dólar — planos de assinatura não são cobrados por token)
sellbird export                # Prospects entregáveis → CSV pronto para sequenciador (prospects.csv)
sellbird precleared-key [--email ADDRESS]  # Chave grátis do Precleared para a checagem de e-mail frio, salva no .env
sellbird export --all          # Lista bruta completa, sem filtros
sellbird companies             # CSV do registro de empresas: cada empresa, seu fit score e por que não foi contatada
sellbird gmail auth            # OAuth do Gmail, uma vez (quando provider: gmail)
sellbird gmail test            # Verifica a conexão do Gmail
sellbird outbox                # Revisa e-mails na fila; --approve <id> / --approve-all / --reject <id>
sellbird signals               # O vocabulário de signals; --confirm / --reject CODES (ou 'free' / 'all')
sellbird discover              # Encontra empresas; --providers / --estimate / --provider <key>
sellbird sending pause|resume  # Kill switch para todo envio de saída
sellbird warmup [domain]       # Prontidão do domínio de envio: SPF/DKIM/DMARC, idade, blocklists, ramp-up, warmup do TrulyInbox
sellbird trulyinbox [connect|other]  # Serviço de warmup: conecta o TrulyInbox, ou registra outro serviço
```

### Problemas Comuns
- **"command not found: sellbird"**: ative o venv primeiro: `source .venv/bin/activate`
- **"ModuleNotFoundError: No module named 'sellbird'" depois da instalação (macOS)**: o Python 3.13 ignora em silêncio arquivos `.pth` que carregam a flag de arquivo oculto do macOS, e alguns Macs propagam essa flag para o `.venv`. Rode `sellbird install` de novo (ele corrige sozinho linkando o pacote), ou faça na mão: `ln -s "$(pwd)/sellbird" .venv/lib/python3.13/site-packages/sellbird`
- **"externally-managed-environment"**: use um venv, não o Python do sistema
- **Erros de SQLite**: o diretório `data/` é criado automaticamente na primeira execução
- **O modo headless do Claude falha**: o usuário precisa de `claude login` e de uma assinatura Max ativa
- **Chamadas ao Codex falham** (`brain.provider: codex`): a linha do log diz o motivo — `codex login` com ChatGPT (também quando o login "has expired or is due for renewal": o Sellbird nunca o renova), instale a versão suportada do Codex (`sellbird status --check` mostra o que está errado sem chamada ao modelo; enquanto o Codex está inutilizável o Sellbird pausa ciclos inteiros de propósito), defina `brain.model` com um ID exato do catálogo da conta (o erro lista os modelos que funcionam), ou remova a camada de config do Codex que estiver forçando ferramentas/hooks/MCP de volta. Nunca enfraqueça as checagens de isolamento do Sellbird para passar por cima disso.
- **API da Instantly 401**: chave de API errada ou precisa do plano Growth para acesso à API
- **Limite de taxa da busca do Google**: o Sellbird cai automaticamente para DuckDuckGo e Bing. Para busca confiável, adicione uma chave de API do Serper (US$ 5/mês).
