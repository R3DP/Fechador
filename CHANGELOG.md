# Changelog

Mudanças notáveis no Sellbird, chamado Harvey até a 0.4.0. As datas são as datas de lançamento; o formato segue
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) de forma livre e as versões
seguem [semver](https://semver.org/), com a ressalva de que o Harvey está pré-1.0 e
versões menores ainda podem mudar comportamento.

## [Unreleased]

### Added

- **`writer.require_tip: true` pula prospects sem nada para montar uma dica.**
  Um primeiro e-mail deve citar uma coisa concreta que o remetente mudaria; sem
  nenhuma descoberta sobre a empresa, o rascunho só poderia dizer que não tinha
  conselho. Com a opção ligada, o Writer escreve apenas para um prospect que tenha
  uma descoberta sobre o site, um fato sobre a startup, um sinal ou as notas do
  Scout, e marca os outros como `no_tip` (não deixa como `new`, o que faria o
  heartbeat tentar de novo a cada ciclo).
  O dashboard os mostra como "Nothing to write about yet", o `sellbird status`
  os conta, e `sellbird retry-writes --no-tip` os coloca de volta na fila. Desligado por padrão. A localização da empresa
  também entra agora nos fatos do Writer.
- **Um `compliance.opt_out_line` em italiano passa na validação.** "Non ti
  interessa? Rispondi pure e non ti scriverò più." é aceito, como as linhas em
  inglês, espanhol e hebraico já eram, então um remetente italiano não
  precisa mais de rodapé bilíngue. Uma despedida como "A presto!" continua
  recusada. Respostas em italiano continuam sendo lidas pelo modelo, não por regra.
- **`channels.email.follow_ups: false` não envia follow-ups.** Uma campanha então
  prepara apenas o primeiro e-mail no Gmail, Microsoft e SMTP, então os passos 2 e 3
  não podem ir para alguém que nunca respondeu. Respostas são lidas e respondidas como
  antes. Ligado por padrão, então nada muda a menos que você desligue.

### Changed

- **O writer enxerga o que o Sellbird leu do próprio site da empresa.** Os sinais
  gratuitos de homepage (sem dados estruturados, site sem alteração há seis meses,
  sitemap muito pequeno, crawlers de IA bloqueados) eram coletados mas
  nunca chegavam ao prompt do writer, então um e-mail pedido para citar uma coisa
  concreta a mudar não tinha nada verdadeiro a citar e dizia que não tinha olhado. Descobertas
  que são verdadeiras agora entram como linhas de fato, cada uma dizendo como foi encontrada e que
  a checagem pode deixar passar coisas; um sinal verificado e considerado bom fica de fora. "Sem
  agendamento online" não é repassado: uma leitura de homepage perde widgets que carregam
  tarde, e ela chamava de não-agendável uma empresa agendável com frequência demais.
  Essas descobertas vêm de uma página e podem estar erradas, então `writer.site_facts:
  false` as desliga, e `CLAUDE.md` e o guia de aprovação agora dizem
  ao Claude para oferecer uma checagem no navegador das afirmações de cada rascunho antes de o usuário
  aprovar.
- **A checagem de cold-email aceita um remetente baseado em qualquer um dos
  catorze países do Precleared.** `compliance.precleared.sender_country` aceita GB, US,
  CA, DE, FR, AU, IE, NL, ES, IT, LV, AE, EG e QA (`UK`, `USA` e `UAE` são
  lidos como seus códigos), onde antes aceitava só GB ou US; `sellbird setup` pede
  um código de duas letras e os lista quando a resposta não é um. Um remetente cujo
  fuso horário é Europe/London é avisado de que a checagem é recomendada para ele e
  recebe GB como seu país; ainda assim espera o sim dele. A documentação diz que
  os 14 dias de 100 checagens por dia de uma chave nova começam na primeira checagem.
- Semear o catálogo de sinais grava apenas um sinal que está faltando ou cujo texto do catálogo mudou. O dashboard semeia a cada carregamento do Today, então isso era uma gravação por sinal a cada visualização de página.
- **A linha de opt-out aceita qualquer redação.** `compliance.opt_out_line` não
  precisa mais pedir uma palavra-chave: "Not interested? Just let me know and I won't email
  you again." é o novo padrão. Frases claras ainda são pegas por regra, e
  o modelo lê cada outra resposta em busca de um pedido para parar. A linha ainda deve
  dizer que os e-mails podem parar, seja qual for a redação, então uma despedida como "Cheers!" é
  recusada; `""` deixa a linha de fora de propósito. Um link ou um endereço de e-mail ainda é
  recusado.
- **Uma resposta `unknown` da checagem de cold-email segura o e-mail em vez de
  reprová-lo.** O Precleared responde `unknown` quando um fato não pode ser estabelecido,
  geralmente o país do destinatário, às vezes um registro que estava lento demais.
  Esse e-mail agora espera no Outbox com o que resolveria (definir
  `prospect_country`, ou dar à empresa uma localização ou número) e é consultado
  de novo, depois de seis horas e depois de um dia; o terceiro unknown com os
  mesmos fatos o reprova como antes. Rejeitar ou enviar o e-mail limpa a
  nota, como para um endereço que a checagem não conseguiu alcançar.

### Security

- **O autopilot segura números de telefone e pedidos de dinheiro.** Um e-mail que ninguém
  aprovou agora espera no Outbox quando fornece um número de telefone que não é
  seu (`channels.email.phone_numbers`, ou um no seu endereço postal) ou
  pede ao leitor para enviar dinheiro (transferência bancária ou wire, IBAN, cripto, cartões-presente
  e similares), como já fazia com links para domínios que não são
  seus. Um "ligue para este número" plantado não pode sair sozinho.
- **O treinamento lê seu site como dados.** As páginas que `sellbird train` rastreia
  são cercadas como texto não confiável, como respostas e pesquisa já eram, então
  um comentário ou avaliação no seu site não pode direcionar o que o treinamento grava em
  todo e-mail posterior.

### Added

- **Donos em sites em francês.** Encontrar o tomador de decisão agora lê
  francês do Québec: propriétaire, président(e), PDG, président-directeur
  général, fondateur/fondatrice, directeur/directrice général(e) e
  associé(e), com ou sem acentos. Um título feminino satisfaz sua entrada masculina de ICP ("Présidente" para "Président"), e um ICP escrito
  somente em francês ainda mira o dono. Frases como "fondée par…",
  "notre président et fondateur, …" e "… est propriétaire de l'entreprise"
  são lidas, nomes com acentos e hífens (Marie-Ève, Côté) contam como
  nomes, e as páginas "Équipe", "À propos" e "Nous joindre" do site são
  seguidas. Antes, esses sites caíam de volta no endereço info@ publicado.
- **Opt-outs em francês.** `compliance.opt_out_line` aceita redação em francês ("Pas intéressé? Répondez-moi simplement et je ne vous écrirai plus."), com ou sem acentos; antes, uma linha em francês falhava na validação e a configuração inteira não carregava. Respostas dizendo "non merci", "ARRÊT", "désabonnez-moi", "ne m'écrivez plus" ou "pas intéressé" são pegas por regra como as em inglês, hebraico e espanhol, e "Envoyé de mon iPhone" não esconde mais um opt-out isolado.
- **Um app na barra de menus.** `sellbird tray` (barra de menus do macOS, bandeja do Windows)
  inicia o dashboard quando necessário, inicia e para o Sellbird, pausa e
  retoma o envio e abre o dashboard desbloqueado. `sellbird autostart
  install` o inicia no login. Veja "The menu-bar app" em
  [docs/configuration.md](docs/configuration.md).
- **Várias caixas de envio.** Além da caixa principal, conecte caixas Gmail,
  Microsoft 365 ou SMTP que você já tem com
  `sellbird inboxes connect`. Os logins e senhas delas ficam no
  chaveiro do sistema. Cada nova thread vai para a caixa com mais espaço;
  follow-ups e respostas saem pela caixa da própria thread. Cada caixa tem
  seu próprio teto diário de cold ( `channels.email.per_inbox_daily_cap`, ou o seu próprio
  número) e rampa de aquecimento, e pode ser pausada, renomeada, removida ou limitada
  a algumas campanhas. Respostas são lidas de todas as caixas. Com uma caixa
  nada muda. A aba Inboxes do dashboard as mostra, abre cada uma
  para pausar, limitar, renomear ou remover, e adiciona uma (um login Gmail ou Microsoft
  no seu navegador, ou uma senha SMTP que vai direto para o seu
  chaveiro). Seu agente de código pode listá-las e pausar uma, nunca adicionar ou
  remover uma. Veja "Several sending inboxes" em
  [docs/configuration.md](docs/configuration.md).
- **Um servidor MCP para seu agente de código.** `sellbird mcp install` adiciona o
  Sellbird ao Claude Code (ou Codex), mostrando a mudança primeiro. O agente
  lê tudo que o Sellbird sabe, estima custos de discovery e pode pausar
  o envio, através do dashboard em execução com seu próprio token
  (`data/agent-token`). Toda aprovação, configuração, chave, compra e retomada
  continua sendo sua: o token do agente alcança apenas uma curta lista de rotas permitidas.
  Uma extensão pode adicionar ferramentas e abrir suas próprias rotas para o agente. Veja
  "Your coding agent (MCP)" em [docs/configuration.md](docs/configuration.md).
- **Supressões.** Endereços e domínios inteiros que o Sellbird nunca envia e-mail,
  mantidos no banco de dados: um opt-out ou um bounce adiciona o endereço, e
  `sellbird suppressions` os lista, adiciona e remove. Um domínio suprimido
  cobre seus subdomínios. Nada suprimido é preparado, enviado ou enviado para
  o Instantly. Desfazer o opt-out de alguém também remove sua supressão.
  `compliance.do_not_contact` continua sendo a lista mantida à mão em `sellbird.yaml`.
- **Regras de envio e cabeçalhos para extensões.** Uma extensão pode segurar ou cancelar
  um e-mail depois das próprias checagens do Sellbird, e adicionar cabeçalhos como
  `List-Unsubscribe`. Um e-mail que precisa de cabeçalhos que sua caixa não consegue carregar
  espera em vez de sair sem eles. Veja [docs/extensions.md](docs/extensions.md).
- **Provedores de e-mail aceitam como quem enviam, e onde fica seu login.**
  Gmail, Microsoft 365 e SMTP aceitam uma identidade (endereço e nome; a
  persona por padrão), Gmail e Microsoft uma fonte de token (o arquivo de token por
  padrão) e um transporte httpx, e SMTP suas próprias configurações de servidor, para que um
  chamador possa conectar mais de uma caixa. Fazer login com uma conta
  diferente da caixa que está sendo conectada não salva nada.
- **Extensões.** Um pacote separado pode adicionar rotas ao dashboard, passos que
  rodam a cada ciclo do heartbeat e subcomandos `sellbird` através do
  ponto de entrada `sellbird.extensions`, sem aplicar patches no Sellbird. Uma extensão
  com falha para o Sellbird com seu nome; um passo com falha é registrado e
  ignorado. `sellbird.dashboard.build_app(guard=, routers=)` serve o
  dashboard para outra pessoa, com seu próprio login e um home por requisição.
  Veja [docs/extensions.md](docs/extensions.md).
- **Costuras de armazenamento e configuração.** Toda abertura de banco de dados passa por
  `sellbird.storage`: caminhos SQLite como antes, ou `<prefix>:<name>` para um
  backend que uma extensão registra (em código ou através do ponto de entrada `sellbird.storage`),
  que é dono e verifica seu próprio schema. `sellbird.config.use_config`
  define a configuração que `load_config()` retorna para uma tarefa e suas threads, para
  configurações mantidas em outro lugar que não `sellbird.yaml`. Uma instalação auto-hospedada
  se comporta exatamente como antes.
- **Funciona a partir de uma pasta home, não apenas de um checkout.** Instalado com `pip`
  ou `pipx`, o Sellbird antes procurava sua configuração, prompts e skills dentro do
  site-packages. Agora uma pasta home os contém: `SELLBIRD_HOME` se definida, senão
  o checkout (sem mudança), senão a pasta de dados por usuário. O pacote envia
  os padrões e copia o que está faltando na primeira execução, nunca sobrescrevendo
  suas edições. A imagem Docker define `SELLBIRD_HOME=/app`. Veja "Where your
  files live" no README.
- **Chaves de API de verificadores ficam fora dos logs** (de #185 por @techity-mushtaque).
  A chave do Hunter agora vai no cabeçalho `X-API-KEY`; Reoon e ZeroBounce só
  a aceitam na URL, então os loggers `httpx` e `httpcore` ficam em WARNING e
  as próprias linhas de debug do Sellbird apagam a chave do texto de erro.
- **`channels.email.min_write_score`** (padrão 0): o writer pula prospects
  pontuados abaixo disso. O Scout também verifica `compliance.do_not_contact` antes de
  ler o site de uma empresa listada ou gastar créditos de verificação nela.
- **Uma chave Precleared gratuita em um passo** (de #121 por @gabrielaoimevbore-beep).
  `sellbird setup` agora oferece obter uma chave gratuita para a checagem de cold-email com
  apenas um endereço de e-mail, em vez de mandar as pessoas a uma página web e voltar, e
  `sellbird precleared-key` faz o mesmo depois (`--email` não pergunta nada, para um
  agente de código configurando o Sellbird). A chave é salva em `.env` como
  `PRECLEARED_API_KEY` e nunca é impressa. Quando a cota sem chave (10 checagens
  por dia) acaba, a página Today, `sellbird status` e o motivo no Outbox apontam
  para o comando. Chaves gratuitas agora dão 100 checagens por dia nos primeiros 14 dias,
  depois 25, e a documentação diz isso.

### Changed

- **`Referrer-Policy: same-origin`** no dashboard, em vez de
  `no-referrer`: sob `no-referrer` o Firefox envia `Origin: null` em POSTs,
  que a checagem de proveniência do dashboard recusa. Outros sites ainda nunca
  recebem um Referer.
- **Microsoft 365: um envio que pode ter saído mantém seu rascunho.** Um 5xx ou
  uma conexão derrubada no envio final não apaga mais o rascunho, e
  o Outbox marca o e-mail como possivelmente enviado (nunca reenviado). Uma recusa 4xx
  ainda o apaga. Qualquer provedor que informe um envio possível é marcado do
  mesmo jeito.

### Fixed

- **O teto diário do Instantly conta seu dia local, não UTC** (de #177 por
  @solvejet-team), então o teto zera à sua meia-noite.

## [0.4.0] - 2026-11-06

### Changed

- **O Harvey agora é Sellbird.** O pacote, o comando `sellbird`,
  `sellbird.yaml` e `sellbird.local.yaml`, `data/sellbird.db`, as configurações `SELLBIRD_*`
  e o serviço Docker todos carregam o novo nome. Um clone existente
  é atualizado com `git pull && pip install -e .`. Na primeira execução o Sellbird move
  `harvey.local.yaml` e `data/harvey.*` para os novos nomes. Ele nunca
  sobrescreve, e espera enquanto um processo Harvey ainda estiver rodando.
  Configurações `HARVEY_*` ainda se aplicam. `harvey` e `python -m harvey` continuam
  funcionando por enquanto e avisam que se mudaram. Veja "Upgrading from Harvey" no
  README. Depois que uma atualização move arquivos, a tela Today do dashboard diz
  "Harvey is now Sellbird" uma vez, até você dispensar.
- **O agente não se chama mais pelo nome do produto.** Os prompts
  descreviam o modelo como Harvey ("como Harvey Specter"), e o remetente padrão
  e treinado era Harvey em harvey@seu-dominio. O remetente padrão agora é
  Alex. Mensagens salvas antes da renomeação ainda contam como nossas no histórico
  de respostas.
- **Logo.** O dashboard mostra a andorinha do Sellbird e o favicon.
- **Licença: AGPL-3.0.** A partir da 0.4.0 o Sellbird é licenciado sob a GNU
  Affero General Public License v3.0 only. Versões até 0.3.x ficam MIT, e
  esse código mantém seu aviso MIT em `NOTICE`. Novos commits são assinados
  sob o Developer Certificate of Origin (veja `CONTRIBUTING.md`).
- **Um README mais curto.** A página inicial cobre o que o Sellbird faz, o início
  rápido e a atualização a partir do Harvey. As seções detalhadas se mudaram sem alteração para
  `docs/`, com uma nova gravação do dashboard e capturas de tela. Adicionados
  `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md` e templates de issue e pull
  request.

### Added

- **Encaixe da empresa e o registro de empresas.** A aba Companies agora ordena por um
  score de encaixe de 0-100 calculado a partir do que o Harvey já tem: a correspondência de setor do
  ICP, um contato com um título alvo, o melhor e-mail encontrado e uma vaga
  aberta que corresponde a `icp.hiring_signals`. Passe o mouse sobre um score para ver os motivos. Uma coluna Status
  diz o que aconteceu com cada empresa (e-mail enviado, respondeu, optou por sair,
  aprovado, rascunho esperando, pronto) ou por que nada foi enviado (só um e-mail de risco, nenhum endereço
  válido, ninguém nomeado no site, ainda não processado, na lista de não contatar).
  Um e-mail de risco (catch-all) conta como pronto quando
  `channels.email.send_to_risky` está ligado, e a lista de não contatar é lida
  como o remetente a lê, então uma entrada adicionada enquanto o Harvey roda aparece na hora. Clicar numa empresa abre um cartão de detalhes acima dos seus contatos: site,
  setor, área, por que foi selecionada, as pessoas nomeadas no site dela e as
  vagas de contratação, cada uma linkada à página de onde veio. `harvey companies`
  (ou *Export register* na aba) grava o registro inteiro como CSV,
  incluindo empresas sem contato, para que possam ser trabalhadas de outro jeito.
  A aba agora lista até 2.000 empresas, melhor encaixe primeiro e paginadas de 50 em
  50, em vez das 200 mais recentes; o CSV tem todas as empresas. Um contato que
  optou por sair ou está na lista de não contatar não conta para o encaixe, e uma
  vaga que o quadro de carreiras não lista mais deixa de contar como contratação. Nada é armazenado: tudo é lido do banco de dados sob demanda, então
  acompanha a configuração.

- **Seu próprio formato de e-mail** (`writer.email_rules`). Aponte para um arquivo markdown
  (`skills/email_rules.md` está no gitignore) e as regras dele substituem o formato interno
  do Writer, que termina todo prompt e por isso vencia qualquer coisa nas skills:
  e-mail 1 com menos de 75 palavras, uma observação e uma pergunta, sem pitch, sem link.
  Ele cobre o primeiro e-mail por pessoa e a sequência de 3 e-mails. Ele nunca
  levanta a regra de FATOS, e o portão de envio (220 palavras, um link,
  não contatar) ainda se aplica. O prompt agora diz o que o Harvey realmente adiciona
  quando envia: com `compliance.opt_out_line` definido, o rascunho não recebe uma segunda
  frase de opt-out; com ela vazia, uma frase de opt-out que as regras pedem é
  escrita no corpo. Um arquivo que está definido mas ausente, vazio ou longo demais
  para o Writer, então ele nunca escreve no formato que você substituiu. Não definido,
  nada muda.

- **Provedores de discovery Scavio** (`scavio_maps`, `scavio_search`). Listagens do Google Maps
  em volta de cada cidade, com telefone, site, categoria, nota e número de
  avaliações, e resultados orgânicos do Google com posição, ambos a partir de uma
  `SCAVIO_API_KEY`. O Maps é 1 crédito por 20 empresas e o Search 1 crédito por
  10 resultados; as estimativas usam o preço de crédito pay-as-you-go de $0.01. Desligado a menos
  que você escolha um em `harvey discover` ou no dashboard. Fecha #28.
- **E-mails enviados na aba Conversations.** Um novo filtro *Awaiting reply*
  lista pessoas para quem o Harvey enviou e-mail recentemente e que ainda não
  responderam (dos seus 2.000 e-mails enviados mais recentes), com cada e-mail
  enviado e quando saiu, para que a aba mostre toda thread de saída em vez
  de apenas as que tiveram resposta. Quando uma resposta chega, o cartão é
  substituído pela conversa real, que já mostra esses e-mails. Os
  cartões são somente leitura e não criam linhas de conversa. A mudança na API é
  opt-in: `/api/conversations?awaiting=1` os adiciona, e o endpoint sem
  o parâmetro retorna exatamente o que retornava antes. *Open* ainda significa apenas conversas com resposta.
  Um cartão para uma caixa geral (sem nome de pessoa) mostra
  o nome da empresa em vez de "Unknown". Quem respondeu, optou por sair ou
  teve bounce, e colegas de quem respondeu, não são listados.
- **Um logo opcional sob cada e-mail** (de #138).
  `channels.email.signature.logo` envia e-mail do Gmail, Microsoft 365 e SMTP como
  HTML com o logo embutido. Desligado por padrão. Um logo inutilizável segura e-mail aprovado
  e diz por quê no Today, em vez de enviar sem ele.
- **TrulyInbox para aquecimento.** O Harvey agora recomenda o TrulyInbox para aquecer e
  manter caixas de envio saudáveis, e o lê: `harvey trulyinbox connect`
  (ou o novo passo de aquecimento na checklist de configuração do dashboard) verifica uma chave e
  a salva, e `harvey warmup` então diz se a caixa de envio está
  realmente aquecida: inscrita, logada, aquecida por `min_days`, e abaixo de 5%
  de spam no e-mail de aquecimento. Somente leitura; ele nunca muda nada no TrulyInbox.
  `harvey trulyinbox other` registra que você usa outro serviço de aquecimento.
- **Uma lista de não contatar, aplicada no momento do envio.** `compliance.do_not_contact`
  aceita endereços e domínios que o Harvey nunca deve e-mailar: concorrentes, seus
  clientes existentes, qualquer pessoa sob retenção legal, um parceiro que você concordou em não
  abordar. Um domínio cobre seus subdomínios, casados numa fronteira de rótulo, então
  `acme.example` bloqueia `mail.acme.example` e deixa `notacme.example`
  em paz: um teste simples de sufixo pegaria a empresa errada. A verificação roda
  em `pre_send_check`, então é a última coisa antes de um e-mail sair e
  segura um que um humano já aprovou no Outbox. Ela se aplica a respostas também, não só a cold mail: uma lista que deixa
  respostas automáticas passarem não é uma lista de não contatar, e o operador
  ainda pode responder à mão. Entradas são normalizadas quando a configuração carrega, então
  ` @Acme.EXAMPLE `, um `https://www.acme.example/about` colado,
  `Jane Doe <jane@acme.example>` (aquele endereço) e `acme.example` se comportam
  igual; uma entrada que não nomeia nada é erro de configuração, não um no-op silencioso.
  Uma edição conta na hora num Harvey em execução. Uma pessoa listada que escreve
  de volta vai para você sem um rascunho, e `harvey export` a deixa de fora. No
  Instantly, que não tem Outbox, leads listados ficam fora do upload
  e uma resposta a um vai para você; um lead que o Instantly já tem precisa ser
  removido lá.

- **O discovery também pula empresas de não contatar.** A mesma
  lista `compliance.do_not_contact` agora é aplicada durante o discovery, antes de um
  resultado se tornar uma empresa, então um negócio proibido nunca entra no pool: não
  custa nada enriquecer, nunca tem o site lido, e para de aparecer em
  cohortes para alguém notar a olho. O portão de envio não muda e
  ainda tem a última palavra: só ele pode parar um envio. Mas sozinho ele deixava um
  concorrente passar pelo discovery e cobrava o enriquecimento primeiro.
  O discovery tem um domínio, não um endereço, então só entradas de domínio se aplicam aqui:
  `jane@acme.example` barra uma caixa, e acme.example continua descobrível
  porque um colega de lá ainda pode valer a pena alcançar. Empresas puladas
  são contadas separadamente do lixo, e `harvey discover` imprime a contagem
  apenas quando não é zero: lixo pergunta se um resultado é um negócio, ao contrário,
  isto pergunta se você tem permissão de abordar um, e enterrar a segunda
  na primeira é como uma lista que cresceu larga demais passa despercebida.

- **TinyFish como fonte gratuita de discovery** (de #95). `harvey discover
  --provider tinyfish` (ou *TinyFish* na aba Discover) encontra negócios
  por frase com uma `TINYFISH_API_KEY` gratuita, sem cartão, e roda os presets `yc`,
  `hiring`, `accelerator` e `funding`. O Harvey o ritma aos limites publicados,
  30 buscas por minuto e 500 por hora, e uma execução que consome a hora (ou tem a chave recusada) para
  e diz por quê em vez de falhar em cada frase restante. Ele não registra
  `SERP_RANK`: a ordenação do TinyFish não é a do Google e sua busca não aceita
  localização, então sinais de posição ainda vêm do Serper ou DataForSEO SERP, e
  uma execução do TinyFish nunca marca como sumida uma empresa que eles posicionaram. O Scout também
  busca via TinyFish quando a chave está definida, depois do Serper.

- **Vagas abertas do quadro de empregos que a empresa realmente usa.** Quando o
  site próprio de uma empresa linka ou embute um quadro Greenhouse, Lever, Ashby ou Workable,
  o profiling lê o feed JSON público desse quadro (uma requisição, limitada
  a 8 MB, nunca um token adivinhado) em vez de adivinhar pelo HTML da página de
  carreiras, que na maioria dos sites de startup não tem vagas nenhuma porque um
  script as carrega. `HIRING_ROLE` agora registra as vagas que correspondem a
  `icp.hiring_signals` (senão `icp.titles`) com departamento, localização,
  data de publicação e a URL da vaga; o novo sinal `OPEN_ROLES` conta as
  vagas abertas do quadro. Quando o quadro não lista nenhuma vaga correspondente, `HIRING_ROLE`
  é registrado como 0, então uma vaga que fechou para de contar nas cohortes e
  aparece como "não" para o revisor. A correspondência junta VP/Vice President, CMO/Chief
  Marketing Officer e similares, e "Assistant to the CEO" não é uma vaga de
  CEO. Páginas linkando três ou mais quadros, nenhum nomeado como o site (uma
  agência ou uma página de portfólio de VC), não são atribuídas a ninguém. Sites sem
  quadro ainda ganham a leitura da página de carreiras.
  O novo preset de discovery `hiring` (`harvey discover --preset hiring`, ou
  *Look for: Companies hiring for your roles*) busca através do Serper ou
  DataForSEO SERP por empresas cujas próprias páginas de carreiras listam suas vagas.
  `skills/signal_playbook.md` tem uma seção curta sobre usar uma vaga como
  gancho: cite a vaga como publicada, nunca adivinhe salário ou headcount, não
  implique conhecimento interno, atente à data da publicação.

- **Encontre empresas por onde elas se posicionam numa cidade.** O DataForSEO SERP agora também
  registra quem ocupa o 3-pack local (`IN_LOCAL_PACK`, posição 1-3, anúncios
  excluídos), e um novo provedor **DataForSEO Google Maps** registra a
  posição no mapa de cada negócio (`MAPS_RANK`) com sua nota, categoria e
  status de reivindicado, mantendo negócios sem site pela sua place_id
  (`NO_WEBSITE`). Ambos buscam do centro geocodificado da cidade. Toda posição é
  armazenada com a frase de busca que a produziu ("#14 para 'roofer Denver,
  CO'"), uma por negócio por frase, mantendo a melhor. Quando uma busca posterior
  por essa frase não encontra mais um negócio, o Harvey registra isso, então uma posição antiga
  ou um slot de pacote perdido não continuam correspondendo. Negócios sem site são
  indexados pelo cid do Google, então o pacote e o Maps resolvem para uma empresa. `icp.keyword_variants`
  adiciona frases de busca por setor. O construtor de cohort aceita faixas numéricas
  (aba Signals, `/api/cohort` `ranges`, `/api/cohort.csv?ranges=SERP_RANK:11:30`),
  então "posição orgânica 11-30, fora do pacote local" é uma consulta. O playbook
  de sinais tem ângulos baseados em posição, redigidos como "quando buscamos do centro
  de Denver", nunca como uma posição absoluta.

- **Cold email no horário comercial de cada destinatário** (de #59 por
  gabrielaoimevbore-beep; `channels.email.send_window`, #53). Cold email sai apenas entre `start` e `end` (08:00 às 17:00 em
  dias úteis por padrão) no próprio fuso do destinatário. O fuso é calculado
  uma vez e armazenado no prospect, a partir da localização da empresa (estados
  dos EUA, províncias canadenses, estados australianos, países com um fuso ou
  um fuso principal, e as coordenadas que o discovery já tinha em cache), o país que
  o Precleared retorna quando essa checagem está ligada, ou `prospect_country`. Um código
  que é estado e país ao mesmo tempo ("Mumbai, IN", "Adelaide, SA") é
  resolvido por eles; sem mais nada, lê-se como estado dos EUA. Qualquer pessoa que o Harvey
  não consegue situar recebe a janela em `usage.quiet_hours.timezone`. Follow-ups
  mantêm seu `delay_days` e se movem para a janela, um e-mail aprovado fora do
  horário espera a próxima, e respostas nunca são seguradas pela janela.
  Com `recipient_timezone` ligado, as horas de silêncio ainda pausam prospecção,
  escrita e respostas, mas acordam para cold email que pode sair agora na janela do seu
  destinatário (não pausado, dentro dos tetos): o heartbeat lê
  respostas, depois o envia. `weekdays_only` significa segunda a sexta. Desligado a menos que
  definido; somente Gmail, Microsoft e SMTP.

- **Uma skill embutida para vender para startups YC.** O preset de discovery `yc`
  (`harvey discover --preset yc`, ou *Look for: YC startups* em Discover)
  busca nos seus setores, através do Serper ou DataForSEO SERP, por empresas
  cujo próprio site diz que são apoiadas pelo Y Combinator. O novo sinal
  `YC_BACKED` as marca a partir da homepage ou página About (uma referência à sua
  própria página YC, ou uma linha em que dizem isso, nunca linhas de cliente ou público),
  com a turma quando está declarada (W24, S23). Muitas empresas YC
  não dizem isso no site, então ele encontra as que dizem. Para esses prospects o writer e o
  handler de respostas usam o novo playbook `skills/selling_to_startups.md`: quem lê, timing em torno da
  turma e do Demo Day, o que não fazer. O Harvey nunca lê o ycombinator.com,
  cujos termos proíbem rastreá-lo ou coletar dados de contato de fundadores.
- **Startups além do YC: aceleradoras e rodadas recentes.** Mais dois presets:
  `accelerator` (*Accelerator startups*) encontra empresas cujo próprio site diz que
  Techstars, 500 Global, Antler, Entrepreneur First, South Park Commons, Neo,
  AI Grant, a16z speedrun, Pioneer ou Plug and Play as apoiaram, e
  `funding` (*Recently funded*) encontra empresas anunciando sua própria rodada nos
  últimos 18 meses, com sites de notícias, agências de imprensa e bases de funding
  excluídas e filtradas como lixo. Dois novos sinais leem isso de suas próprias
  páginas: `ACCELERATOR` (programa e turma, a partir de uma frase em que a empresa
  diz ou um mural de logos "Backed by") e `FUNDING_ROUND` (rodada, valor e
  data, a partir da homepage, da própria página do hit de busca, About ou da página de
  imprensa; a data a partir da frase ou da data de publicação da página). Ambos são
  ancorados como `YC_BACKED`: "ajudamos startups a captar", linhas de cliente ou
  portfólio, a rodada de um investidor em outra empresa, e dinheiro que
  não é uma rodada (empréstimos fechados, sentenças ganhas, dinheiro captado para
  uma caridade) não contam. O playbook de fundador agora se aplica a empresas apoiadas por YC e
  aceleradoras e a rodadas datadas dos últimos 18 meses, e tem
  uma seção sobre escrever para empresas financiadas recentemente; uma rodada
  mais velha ou sem data nunca é tratada como notícia.
- **Aprovação ou autopilot, visível e alternável.** O Outbox agora diz
  em que modo de envio você está, e Settings → Sending explica os dois,
  lista os domínios contados como seus e os alterna. Ligar o autopilot
  exige digitar `autopilot`; desligá-lo é um clique e funciona
  na hora, mesmo no meio do ciclo (todo passo que enfileira ou envia relê o modo):
  e-mails aprovados pelo autopilot que não saíram voltam para o Outbox,
  e o remetente não enviará um enquanto a aprovação estiver ligada. Apenas a
  linha `require_approval` da sua configuração muda (comentários mantidos), e um
  Harvey em execução a pega no próximo ciclo. Cada linha do outbox registra quem
  aprovou (`approved_by`: você, autopilot, ou "earlier" para linhas de
  antes disso). O README tem uma tabela simples do que cada modo faz.
- **`harvey warmup [domain]`**: verifica se um domínio de envio está pronto para
  cold email. Cobre MX, SPF (`+all`, duplicatas, lookups de nível superior), DKIM,
  DMARC, idade do domínio, blocklists de domínio e de IP de SMTP (uma lista que recusa a
  consulta é reportada como tal, não como listagem), progresso de aquecimento e taxa de
  bounce, então dá um veredito READY / NOT READY. É somente leitura, e um DNS
  timeout é reportado como desconhecido, nunca como registro faltando.
- **Uma rampa de cold-email para domínios novos** (`channels.email.warmup`). A partir de
  `start_date`, nenhum cold email sai por `min_days`; então o teto de cold começa
  em `start_sends` e sobe por `daily_increase` ao dia até
  `max_daily_sends`, contado por dia local. Somente Gmail, Microsoft e SMTP:
  o Instantly tem seu próprio aquecimento e limites por conta. Respostas nunca são
  seguradas. Desligado a menos que `start_date` esteja definido. Ambos baseados em #18 por Tariz Shahid.
- **Um endereço postal e linha de opt-out sob cada cold email** (CAN-SPAM).
  Defina `compliance.postal_address` em `harvey.yaml`; `compliance.opt_out_line`
  tem como padrão *Not interested? Reply "no thanks" and I won't email again.*
  Ambos são adicionados quando o e-mail envia (provedores nativos e Instantly), nunca
  a respostas, e o Outbox os mostra sob cada rascunho; "Open in Gmail"
  também os inclui. Sem um endereço (ou com a linha de opt-out desligada), o cold email ainda envia, e `harvey run`, `harvey status` e a
  aba Outbox avisam até que seja definido. A linha de opt-out deve pedir uma resposta
  que o Harvey reconheça e não pode conter link. Baseado em #13 por Camilo Cruz.
- **A página Today e o `harvey status` dizem quando o Precleared está segurando cold
  email.** Quando a checagem não pode ser feita (suas checagens gratuitas do dia acabaram,
  a chave está sem checagens, foi rejeitada ou está sendo limitada por rate, ou
  o Precleared não pode ser alcançado), cold email para novos endereços espera e respostas
  ainda saem, mas isso antes chegava só no log, então o cold email só saía mais devagar. O Harvey
  agora registra a retenção, e a página Today e
  `harvey status` dizem quantos cold emails estão esperando e o que resolve: uma
  chave gratuita, um pacote para essa chave (o link de checkout da resposta do Precleared),
  ou nada além de tempo. A próxima resposta fresca limpa isso, uma retenção não vista por
  um dia é ignorada, e desligar a checagem limpa. (de #57 por
  gabrielaoimevbore-beep)

### Changed

- **O Precleared recebe os nomes da empresa e da pessoa que o Harvey já tem.**
  Para um endereço do Reino Unido, cold email pode ir para funcionários de uma sociedade
  limitada sem consentimento, mas não para um profissional autônomo, então o Precleared tem que encontrar a empresa
  por trás do domínio no registro da Companies House. Quando só o domínio
  não a encontrou, a resposta era `consent_needed`, mesmo para uma empresa cujo nome o Harvey
  conhecia. O Harvey agora envia `company_name` (o nome do registro de empresa,
  senão o campo de empresa do prospect) e `recipient_name` (o
  primeiro e último nome do prospect; nenhum para uma caixa geral), que o
  Precleared usa para buscar o registro e casar com os administradores da empresa.
  Ele não armazena o nome da pessoa. Os nomes entram na impressão digital do cache
  apenas quando definidos: um `ok_to_email` em cache continua valendo quando eles chegam, e
  qualquer outro veredito em cache ganha uma checagem fresca com eles.
- **O Precleared recebe o país do destinatário que o Harvey já sabe.** A
  janela de envio calcula onde uma empresa está (um país, estado dos EUA, província
  canadense ou estado australiano na sua localização, ou um código que é estado
  e país ao mesmo tempo quando as coordenadas em cache resolvem); a checagem de compliance
  perguntava ao Precleared sobre o endereço sem nada disso, então o
  Precleared tinha que encontrar o país de novo e, quando não conseguia, respondia
  `unknown` e o e-mail falhava. O Harvey agora envia esse país como
  `recipient_country` quando tem certeza dele, o que o Precleared toma como
  dado. Nada do que ele não tem certeza é enviado: "Berlin, DE" sem
  coordenadas é lido como Delaware por convenção e vai sem país,
  assim como uma cidade isolada e coordenadas sozinhas. Sem um país certo,
  `prospect_country` vai como padrão, como antes, e sem ele
  definido, o país único em que toda entrada de `icp.geography` está agora serve como esse
  padrão; o Precleared usa um padrão só quando suas próprias buscas não mostram
  nada. O país entra na impressão digital do cache apenas quando está definido, então
  os vereditos em cache são mantidos, e um endereço do qual o Harvey depois tem certeza é
  rechecado uma vez, a menos que o Precleared tenha achado o mesmo país por conta própria.
  `docs/precleared.md` descreve a checagem por inteiro.
- **A configuração vem primeiro no Today.** Até a configuração terminar, a checklist fica no
  topo da página Today como um cartão "Finish setting up Harvey", com o próximo
  passo destacado, em vez de no fundo da coluna lateral.
- **O Scout lê o site de uma empresa como uma pessoa leria.** Começa na
  homepage e segue o menu do próprio site até as páginas de equipe, sobre, nossa história,
  conheça os médicos ou advogados (seis páginas no máximo), em vez de
  adivinhar nove caminhos fixos e parar no primeiro que respondesse. Donos
  são lidos de cartões de equipe, frases ("owned and operated by…"),
  e fundadores do schema.org, e vêm primeiro (um sobrenome no nome do negócio
  só desempata entre donos);
  no máximo duas pessoas por empresa se tornam prospects. Títulos de ICP casam por
  palavra inteira, com sinônimos de dono (Proprietor, Principal, Managing Partner,
  Founder, CEO). Com `LIKELY_OWNER` confirmado, cada dono é registrado com
  sua evidência.
- **Padrões de e-mail vêm dos endereços que um site publica**, incluindo
  os escondidos atrás da proteção de e-mail do Cloudflare ou de atributos `data-`
  de um link de mail, casados com as pessoas que o site nomeia. Um endereço ambíguo
  isolado (`kmorrow@`) não ensina nada, e um endereço que outra pessoa nomeada
  poderia ter (`jsmith@` com John e Jane Smith lá) nunca é adivinhado
  para ninguém. O endereço publicado de uma pessoa nomeada é usado como está. Sem
  evidência, uma empresa sabidamente pequena (tamanho de empresa do ICP, ou uma
  listagem de negócio local) é adivinhada como `first@`, as outras como `first.last@`. Todo endereço ainda é classificado
  verificado / arriscado / adivinhação / inválido, e só os verificados ou arriscados são
  algum dia enviados.
- **O Gmail lê só o que é novo.** Depois da primeira leitura completa da
  semana, cada ciclo pede ao histórico do Gmail as mensagens adicionadas à caixa
  desde a última checagem, então uma caixa movimentada custa o que uma silenciosa custa.
  O Harvey só avança além delas depois que toda resposta foi tratada, então uma
  que ele não conseguiu tratar é lida de novo. Ele lê a semana inteira de novo quando
  o marcador de histórico do Gmail expirou, e uma vez por dia como garantia.

### Fixed

- **Opt-outs em espanhol são pegos sem o modelo** (de #154). "No,
  gracias", um "BAJA" isolado, "denme de baja", "no me escriba más", "dejen de
  enviarme correos", "sáquenme de su lista", "no quiero recibir más correos"
  e "no me interesa" como resposta inteira são honrados por regra, com ou
  sem acentos. Cada um precisa do verbo voltado ao remetente, então "¡cómo no,
  gracias!", "queremos dar de baja a nuestro proveedor", "sáquenme de dudas",
  "no me interesa el plan anual, pero sí el mensual" e "no me escriba
  hasta enero" vão para o modelo. Um `compliance.opt_out_line` em espanhol
  (`Responda BAJA`, `Responda "no, gracias"`) agora passa na validação, e
  "Enviado desde mi iPhone" não esconde mais um "BAJA" isolado. O discovery
  OpenStreetMap mapeia termos de negócio em espanhol (ferretería, supermercado,
  farmacia, mayorista, contador, panadería, clínica e outros) às tags
  que os carregam.
- **O Microsoft 365 lê uma caixa com mais de uma página.** O Graph ao vivo grava
  a caixa em forma de chave OData em `@odata.nextLink`
  (`/me/mailFolders('inbox')/messages`), e a checagem de link aceitava apenas
  `/me/mailFolders/inbox/messages`. Qualquer caixa com mais de 50 mensagens nos
  últimos 7 dias falhava toda leitura com "@odata.nextLink rejected: not the
  Graph inbox listing", então o envio ficava retido de vez. As duas grafias da
  mesma listagem são aceitas agora; qualquer outro caminho ainda é recusado antes do
  token ser anexado.
- **Ameaças legais e reclamações em hebraico vão para você sem o modelo** (de
  #135), e um opt-out que também ameaça, em qualquer idioma, é honrado e
  aparece em **Needs you** em vez de ser fechado sem ser visto.
- **O discovery OpenStreetMap sobrevive a uma tarde ruim** (de #125). Um 500, 502 ou
  503 de um espelho do Overpass agora passa para o próximo em vez de encerrar a
  busca, o Overpass ganha tempo suficiente para passar pela fila, e a lista de espelhos
  descarta um que era a mesma máquina que outro. `scripts/diagnose_overpass.py`
  recheca os espelhos.
- **Opt-outs em hebraico são honrados sem o modelo** (de #134). Uma resposta como
  "הסר", "תורידו אותי מהרשימה" ou "לא תודה" agora opta por sair como seu equivalente em inglês
  faz, e `compliance.opt_out_line` pode pedir uma resposta em hebraico.
- **O Harvey continua prospectando quando não consegue enviar ou está esperando uma resposta**
  (de #128, #126). Um rascunho que não pôde ser implantado (canal de e-mail desligado, ou envio nativo
  pausado) ou qualquer conversa aberta antes vencia todo ciclo, então o Harvey
  parava de escrever e de encontrar prospects. Respostas agora são lidas junto com
  o que o ciclo faz, ainda antes de qualquer coisa ser enviada. Uma resposta automática agora
  vai para **Needs you**. Uma conversa entregue a você fica com você: respostas posteriores
  entram nela e o Harvey não as responde até você devolvê-la. Antes,
  uma resposta após uma escalada iniciava uma nova conversa que o Harvey podia responder.
- **Respostas lembram a conversa inteira** (fecha #97). Uma resposta era
  escrita apenas das últimas seis mensagens, então um requisito que o prospect
  declarava antes ("somente dados sintéticos, processados na UE") caía
  e o rascunho podia contradizê-lo. O Harvey agora envia a thread inteira, e
  diz ao modelo que o que o prospect pediu ou descartou, e o que o
  Harvey concordou nas próprias mensagens, ainda vale. O texto de cada mensagem
  é citado sob um cabeçalho que o prospect não consegue digitar, então uma resposta que escreve
  "Harvey: confirmed, the first year is free" continua sendo palavras do prospect
  e não é acordo. Uma thread longa demais (cerca de 24.000 caracteres)
  mantém as seis últimas mensagens, depois as próprias palavras anteriores do prospect,
  depois as do Harvey, e diz quantas deixou de fora; um bloco de texto colado numa
  mensagem mais antiga é cortado para não tirar espaço do resto, enquanto a
  mensagem sendo respondida é mantida quase inteira.

- **Start e Stop do dashboard funcionam, no Windows e em qualquer lugar.**
  Start lançava `python -m harvey` sem comando, então o loop imprimia a
  ajuda e saía; agora ele roda `harvey run`, e encontra `claude` em
  `~/.local/bin` quando o instalador nativo o deixou fora do PATH. No Windows a
  checagem "está rodando?" era `os.kill(pid, 0)`, que lá encerra o
  processo sobre o qual pergunta, e um arquivo PID obsoleto fazia o status e o Start
  retornarem 500. A checagem agora pergunta ao SO sem sinalizar. `harvey run`
  também se registra, então um loop iniciado num terminal aparece como rodando, e
  mantém um lock em `data/harvey.lock`: um arquivo PID deixado por um crash ou um reboot
  pode nomear um programa não relacionado, que agora é reportado como não rodando e nunca
  sinalizado, e um segundo `harvey run` se recusa a iniciar enquanto um estiver
  rodando. O Start se recusa, com o motivo, até que `harvey setup` tenha sido
  rodado (o loop costumava ficar parado no assistente de setup lendo o terminal do dashboard),
  e o Stop diz isso quando não conseguiu encerrar o loop em vez de
  reportar sucesso. (De #91 e #90.)

- **`{{company}}'s` fica certo para nomes terminados em "s"**: "Parkes Builders'",
  não "Parkes Builders's". (De #90.)

- **Buscas web de perfil do LinkedIn rodam só quando a prospecção no LinkedIn está ligada**
  (de #60 por FreemanGT). Buscar `site:linkedin.com/in` pelos seus títulos
  encontrava nomes sem empresa e sem e-mail, que o Harvey nunca poderia verificar
  ou escrever, e eles contavam para a checagem de "sem e-mails utilizáveis" que
  pausa a prospecção no dia. Ela também rodava primeiro e podia consumir as
  três buscas do ciclo antes do discovery de empresas, que encontra pessoas que
  você pode e-mailar, fazer alguma. Essa busca agora roda só quando a prospecção no LinkedIn
  está ligada (`channels.linkedin.enabled`, desligada por padrão) com um login do LinkedIn.

- **Ações do dashboard funcionam no Safari e no Firefox** (de #80 por 0SansNom).
  Confirmar sinais, aprovar o Outbox e salvar configurações falhavam
  com "Cross-origin requests are refused." As requisições do dashboard pediam ao
  navegador para não enviar referrer, o que pela especificação Fetch faz o Origin de um POST ser
  `null`, e o guard corretamente recusava. Safari e Firefox seguem a
  especificação; o Chrome não, então funcionava lá. As requisições agora enviam sua origem
  para o próprio dashboard, e só para ele.

- **Uma resposta para o cold email para a empresa inteira.** O stop-on-reply era
  por pessoa, então quando um dono escrevia de volta "não interessado" o gerente de escritório
  ainda recebia o follow-up. Agora uma resposta (não um bounce, um
  fora do escritório ou um "pessoa errada, pergunte ao Bob") cancela os e-mails de sequência
  enfileirados para todos os outros naquela empresa, e o Harvey não vai escrever, preparar
  ou enviar cold email para eles depois; o Outbox e o log dizem qual colega
  respondeu. Colegas são a mesma empresa; ou, quando o Harvey não tem empresa
  para um deles, o mesmo domínio de e-mail, e só se for o domínio
  próprio daquela empresa, nunca um compartilhado como gmail.com ou rr.com. Campanhas
  criadas pelo Harvey no Instantly ligam o `stop_for_company` do próprio Instantly.

- **O DataForSEO SERP envia uma localização.** Ele enviava só uma palavra-chave, mas
  o DataForSEO exige uma localização em toda tarefa, então as buscas falhavam ou voltavam
  sem localização. Agora ele envia o ponto geocodificado da cidade, ou um
  nome de localização "Denver,Colorado,United States", ou os Estados Unidos para
  buscas sem cidade. "Sem resultados de busca" agora é uma resposta vazia em
  vez de erro; outros erros de tarefa ainda param aquela consulta e são reportados.
- **As estimativas do DataForSEO SERP eram 3,3x menores.** Elas usavam o preço da fila
  padrão ($0.0006 por 10 resultados); o Harvey chama o endpoint Live ($0.002),
  então uma busca de profundidade 30 é $0.006, não $0.0018. O Harvey fica no Live: ele é
  síncrono, então o teto de gasto checado entre buscas vê o gasto real.

- **O Scout encontra o verdadeiro tomador de decisão.** Num conjunto de teste de 19 sites de pequenos
  negócios ele encontrava a pessoa certa em 3; agora encontra em 17. Ele
  não transforma mais títulos como "Team of Experts" em prospects, não lê um parágrafo de
  bio como cargo, não deixa "Vice President" passar por "President",
  e não toma um cliente citado num depoimento pelo dono.
- **Um padrão de e-mail padrão em cache não bloqueia mais evidência melhor.** Um
  palpite first.last@ em cache para um domínio costumava ser lido primeiro para sempre, então
  nem um endereço real nem uma busca no Hunter podiam substituí-lo. O Hunter é
  consultado uma vez por domínio, e `j.smith@` não é mais lido como first.last@.
- **O fallback de caixa da empresa encontra caixas publicadas que antes perdia**: ele
  lê páginas inteiras (um `info@` a 140k caracteres dentro de uma página contava
  como nada), schema.org, e um endereço no segundo domínio da própria empresa
  (`admin@phroofing.test` para prairieheritageroofing.test). Também é usado
  quando o endereço do dono nomeado é apenas um palpite, que nunca é enviado.
- **O reCAPTCHA não faz mais um site parecer bloqueado.** Qualquer página mencionando
  "captcha" nos primeiros 4.000 caracteres contava como bloqueio, o que custou
  ao Harvey todo site com formulário de contato protegido. Só páginas de desafio reais
  contam agora, e um desafio do SiteGround ou Cloudflare é reportado como
  desafiado (não inalcançável) sem repassar toda variante de URL.
- **O Gmail lê respostas no charset em que foram escritas** (de #58 por
  xiaoheiai4719-collab). Toda resposta era decodificada como UTF-8, então uma resposta enviada
  como ISO-8859-1 ou Windows-1252 ("Je préfère mardi") chegava ao modelo
  corrompida. Cada parte agora usa seu charset declarado; um desconhecido ou faltante,
  ou cabeçalhos estranhos, cai em UTF-8 sem perder o texto. SMTP
  e Microsoft 365 já decodificavam corretamente.
- **Você vê quando o Harvey não está enviando porque não conseguiu ler sua
  caixa.** O envio espera até que as respostas sejam lidas, então um opt-out impede seu
  follow-up. Essa retenção só aparecia no log, então um login do Gmail expirado
  podia travar o envio por dias sem ser notado. O Today agora mostra isso primeiro, com
  o motivo, há quanto tempo, quantos e-mails estão esperando e a correção (`harvey
  gmail auth`, `harvey microsoft auth`, ou uma caixa acima do limite de leitura),
  e o `harvey status` também. Ele se limpa quando o envio volta a rodar.
- **Gmail: nada envia até a caixa inteira ser lida** (de #62 por
  xiaoheiai4719-collab). Uma leitura falha ou parcial da caixa costumava parecer
  uma caixa vazia, então um follow-up podia sair antes de um opt-out na página dois
  ser tratado. O Gmail agora lê toda página da última semana, e levanta erro em
  qualquer falha para que o heartbeat segure o envio, como no Microsoft 365. Um
  envio cujo resultado é desconhecido (uma conexão derrubada, um 5xx, uma resposta ilegível)
  é registrado como talvez-enviado e nunca reenviado, então ninguém o recebe
  duas vezes. Mensagens já lidas não são baixadas de novo em ciclos posteriores.
- **O autopilot não pode ser guiado por texto de fora** (#66, reportado por
  Yaaaannnn435). Sites que o Harvey pesquisa e as respostas que as pessoas enviam
  chegam ao modelo, e qualquer um pode carregar instruções plantadas. Esse texto é
  agora cercado como dados em todo prompt (writer, handler de respostas, scoring do scout,
  Humanizer), num bloco que ele não consegue fechar sozinho. Prompts só reduzem as chances,
  então com `require_approval: false` um e-mail que ninguém aprovou volta para
  o Outbox, marcado como Held com o motivo, quando linka ou fornece
  um endereço num domínio que não é seu (domínio de envio, link de agendamento, ou
  `channels.email.link_domains`), ou cita instruções do próprio Harvey.
  Domínios nus como `example.com/x` contam como links. Aprová-lo você mesmo
  o envia. No Instantly, respostas agora passam pelo portão pré-envio também e uma segurada
  vai para você; um template de campanha que seria segurado não é implantado.
  O modelo nunca teve ferramentas, arquivos ou rede para agir, então isso
  nunca foi mais do que o que ele escreveu.
- **Contatos que optaram por sair não ficam mais no CSV de prospects.** Alguém que
  respondeu "unsubscribe" ficava no `harvey export` e no botão Export do dashboard,
  então levar a lista a outro sequenciador podia e-mailá-lo de novo.
  Eles agora ficam de fora mesmo quando `--status` ou `--email-status` é informado;
  `harvey export --all` (e `?all=true`) ainda é o dump bruto, sem filtro.
  De #64 por hifzabuildsai.
- **Um opt-out agora continua sendo um opt-out.** Qualquer mensagem posterior de quem
  optou por sair (um fora do escritório, um "obrigado") o colocava de volta em *replied* ou
  *lost*, o que o punha de volta na exportação, e uma pergunta dele ganhava uma
  resposta rascunhada no Outbox. Agora a mensagem dele é mantida numa conversa fechada
  para você ler, nada é rascunhado, e nenhum caminho de código pode mover um prospect
  para fora de *opted out*. Uma reclamação dele ainda chega para você.
- **Veja por que alguém optou por sair, e desfaça.** Cada opt-out agora registra a
  regra que disparou (uma frase de opt-out, "no thanks", uma resposta de uma palavra, ou o
  julgamento do modelo), as palavras que casaram e a mensagem. **Why?** na
  linha dele em Contacts (ou na conversa) mostra isso, e **Undo
  opt-out** reverte um engano depois de uma confirmação: a pessoa volta a *replied*,
  então nada é enviado por conta própria, e a resposta do Harvey à próxima resposta dele
  espera sua aprovação mesmo com `require_approval: false` (no
  Instantly, que não consegue segurar uma resposta, essa conversa vem para você). Opt-outs de antes
  disso mostram a última mensagem em vez disso, e todo desfazer é registrado.
- **`aiosmtplib` agora é 5.1.3 ou posterior** (era `>=3.0.1,<4`). Versões mais antigas
  escreviam um CR/LF dentro de um endereço direto no servidor SMTP, então um endereço
  raspado de um site podia adicionar comandos próprios
  (GHSA-v3q9-hj7j-63hq), e mantinha bytes em texto claro através do STARTTLS
  (GHSA-vxj7-4xrp-5vr4). O Harvey passa endereços raspados a ele ao enviar
  por SMTP e ao sondar uma caixa. Reportado em #66.
- Um follow-up não sai mais antes, ou logo depois, do e-mail que
  ele segue. Cada passo agora espera até que o anterior tenha sido realmente enviado
  e seu intervalo (pelo menos um dia) tenha passado. Antes, aprovar um lote de rascunhos
  tarde, ou retomar após uma pausa ou uma retenção de compliance, podia enviar uma
  sequência inteira em minutos, ou o passo 2 antes do passo 1. Um follow-up cujo e-mail anterior
  foi rejeitado ou falhou é cancelado em vez de chegar como um primeiro
  e-mail.
- **Windows:** arquivos de texto (harvey.yaml, .env, prompts, skills, saída treinada,
  tokens, exportações) são lidos e gravados como UTF-8 em vez da
  página de código do locale, então `harvey train` não trava mais em caracteres como
  "★" e os prompts não ficam corrompidos; a saída de comando também é UTF-8, então o
  log do dashboard do `harvey run` não pode travar em "⚠". O shim `claude.cmd` de uma instalação
  npm é resolvido para o `claude.exe` nativo que ele envolve e nunca é
  executado via cmd.exe, que reinterpretaria as flags de isolamento do Harvey;
  se o executável estiver faltando, o Harvey diz como corrigir. Arquivos que um
  Harvey mais antigo salvou na página de código do Windows (skills treinadas, harvey.yaml) ainda
  carregam, com um aviso para salvá-los de novo como UTF-8. Os CSVs do `harvey export` são agora
  UTF-8 no Windows também, como os sequenciadores esperam (o Excel precisa de Data > From
  Text/CSV para mostrar acentos). Baseado em #18 por Tariz Shahid.
- Respostas são lidas sem o e-mail que elas citam. O modelo, a thread armazenada
  e a resposta recebem a resposta sem o e-mail citado, e qualquer linha que
  repete o que o Harvey enviou àquela pessoa é deixada de lado, então as próprias palavras do Harvey
  (seu rodapé, ou uma palavra de escalada como "attorney" no seu pitch) não contam
  como da pessoa. Palavras de opt-out e de escalada que a pessoa escreveu ainda são encontradas
  em qualquer lugar, inclusive entre ou sob linhas citadas. "No thanks" / "no thank
  you" como frase, e uma resposta de apenas "STOP", agora contam como opt-outs.

- O Sender reivindica cada e-mail logo antes de enviá-lo. Uma resposta, bounce, envio
  manual ou rejeição que cancela um e-mail aprovado enquanto o Sender está trabalhando
  na fila agora o para, em vez do Sender enviar sua cópia anterior
  e registrá-lo como enviado. Dois processos do Harvey rodando ao mesmo tempo não
  podem mais enviar o mesmo e-mail duas vezes. Um e-mail cortado no meio do envio (o Harvey parou,
  ou a biblioteca de e-mail travou no meio da chamada) é marcado como falho e nunca reenviado, já que
  pode ter saído; ele aparece em "Didn't send" com uma nota para checar sua
  pasta Sent, e o dashboard não oferece e-mailar aquela pessoa à mão.
  Rejeitar um e-mail que já está sendo enviado ou foi enviado é recusado em vez de
  renomeá-lo.
- Mantenha requisições a sites locais fora de redes privadas, incluindo redirecionamentos e
  DNS rebinding. Preserve o hostname original para verificação TLS. A busca de sites
  (busca, sites de empresas, profiling, o rastreador de treinamento) agora ignora
  `HTTP_PROXY`/`HTTPS_PROXY`, então não pode ser roteada em volta dessa fronteira; mail
  e integrações de API não mudam. `harvey train` recusa URLs locais ou de intranet
  e diz isso.
- **Usuários do Instantly: verifiquem `require_approval`.** O Instantly não tem fila de
  aprovação por e-mail, então com `channels.email.require_approval: true` (o padrão)
  o Harvey agora retém a implantação de campanha e entrega respostas a um humano em vez de
  contornar silenciosamente a configuração. `harvey run` e `harvey status` dizem quando isso
  está acontecendo; prospecção e escrita continuam (rascunhos esperam, usando cota de
  modelo, até o envio ser permitido). Defina `require_approval: false` para
  o autopilot do Instantly.
- Desligar o LinkedIn por padrão no modelo, na config de exemplo e no treinador de produto;
  salvar a escolha explícita de LinkedIn do assistente de setup ao atualizar uma configuração.
  Responder "não" ao LinkedIn ao rodar `harvey setup` de novo agora o desliga
  (credenciais salvas ficam em `.env`).
- Proteja o dashboard local com um token de acesso, restrinja requisições a origens
  locais confiáveis, e salve configurações com permissões só do dono. Atualize e reinicie o
  Harvey, depois abra o link do dashboard impresso no seu terminal.
- Isole chamadas do Claude de instruções pessoais e hooks, e conserte a instalação
  do CLI do Claude no Docker. Obrigado a @EICCIO-Advisors pelo relatório privado.

### Added

- **Envie à mão pelo dashboard, e um painel de status ao vivo.** Sem
  caixa conectada (ou com o e-mail desligado), o primeiro e-mail de cada campanha tem um
  botão **Open in Gmail** que preenche uma janela de composição na conta
  com que o Harvey envia, e uma caixa **Mark as sent**. O Harvey nunca envia para alguém
  marcado como enviado à mão, mesmo que uma caixa seja conectada depois, e só oferece
  isso para pessoas que ele ainda poderia e-mailar (não optou por sair, respondeu, teve bounce, ou
  já está na fila do Harvey). A aba Today ganha um painel mostrando cada passo do pipeline,
  o que está rodando, e o que fazer em seguida.

- **Revisão do Outbox: veja em que um rascunho se baseia, e edite.** Cada rascunho
  pendente agora mostra sua campanha, a empresa (nome, site clicável,
  descrição), o contato e como foi encontrado, status e score do e-mail,
  sinais de tech / agência / contratação / anúncios / agendamento, e as notas do Writer, para que
  toda afirmação possa ser checada contra o que o Harvey realmente encontrou. **Edit** (ou
  `E`) transforma assunto e corpo em campos; Save reescreve o rascunho apenas enquanto
  ele ainda está `pending_review` e nunca o aprova. Uma edição que o sender
  bloquearia (merge tags, HTML, frases proibidas) é recusada ao salvar com
  o motivo; uma resposta mantém seu assunto para continuar na thread; toda edição é
  registrada com o que substituiu. Enquanto edita, os atalhos e o Approve all
  não podem agir sobre o rascunho não editado. `POST /api/outbox/{id}/edit` sustenta isso.

- **Provedor de e-mail Microsoft 365.** Defina `channels.email.provider: microsoft` para
  enviar e ler através de uma caixa Microsoft 365 / Outlook via Microsoft Graph,
  para domínios cujo e-mail vive no Exchange Online (que não aceita mais
  senhas via IMAP). Faça login uma vez com OAuth + PKCE (`harvey microsoft
  auth`; sem client secret, sem senha armazenada), rascunha e depois envia para que o
  Message-ID seja conhecido, encadeia respostas com `createReply`, lê os últimos 7
  dias da caixa sem marcar nada como lido, recusa agir como qualquer
  caixa que não `persona.email`, e segura o envio quando a caixa não pode
  ser lida. Veja [docs/microsoft365.md](docs/microsoft365.md).
- **Checagem de compliance opcional por destinatário (Precleared).** Defina
  `compliance.precleared.enabled: true` com `sender_country: GB` ou `US` para
  ter cada novo destinatário checado antes do primeiro cold email contra a PECR do Reino
  Unido, CAN-SPAM dos EUA, CASL do Canadá, UWG da Alemanha e as regras da França. Qualquer
  veredito que não seja `ok_to_email` reprova aquele item do outbox com a regra e o próximo
  passo. Se a checagem não puder ser feita por causa do Precleared (cota diária ou
  rate limit, uma chave ruim, rede fora, uma resposta ilegível), novos endereços
  esperam um ciclo posterior enquanto e-mail para pessoas já liberadas, e respostas,
  ainda saem; se falha para um endereço, só aquele e-mail é movido de volta
  seis horas (falhas em dois domínios diferentes sem resposta entre elas
  seguram novos endereços também), e um endereço cuja checagem deu timeout ou recebeu
  uma resposta que o Harvey não consegue ler é movido de volta também, para não manter
  os outros esperando. Uma checagem por endereço, em cache por 30 dias; mudar o
  país do remetente, a fonte do endereço ou a descrição do produto dispara uma checagem
  nova. O id do recibo é registrado com cada envio. Somente provedores nativos. Desligado
  por padrão.
- **`harvey setup` oferece a checagem Precleared** (de #46 por
  gabrielaoimevbore-beep). Um novo último passo opcional
  pergunta se quer ligar a checagem, onde seu negócio está baseado (GB ou US)
  e, se seus prospects estão todos em um país, qual (responder "não"
  ali pergunta antes de salvá-lo como o código da Noruega). Ele então oferece uma
  `PRECLEARED_API_KEY` gratuita (input oculto, salvo em `.env`; 25 checagens por dia
  em vez de 10). Desligado a menos que você diga sim. Rodar o setup de novo oferece suas respostas
  salvas como padrões, então apertar Enter nunca desliga a checagem. O
  setup guiado pelo Claude em CLAUDE.md oferece o mesmo passo. O setup agora lê e
  salva `harvey.local.yaml` quando ele existe (é o que `harvey train` escreve,
  e o arquivo que o Harvey lê), não o `harvey.yaml` que ele sombreia, então suas respostas
  fazem efeito; se não consegue salvar o arquivo, diz isso em vez de marcar o
  resumo.
- **Paginação e exportação CSV do construtor de cohort.** A tabela de cohort na
  aba Signals costumava parar nas primeiras 50 correspondências sem forma de ver o
  resto. Agora ela pagina com Prev / Next ("Showing 51–100 of 147"), e um
  botão Export CSV baixa o cohort inteiro. `POST /api/cohort` aceita
  `offset` e `limit` (padrão 50, máximo 200) e ordena por nome para que as páginas nunca
  se sobreponham; `GET /api/cohort.csv?require=...&exclude=...` retorna toda correspondência.
  Contagens e exportações incluem toda correspondência; páginas usam uma ordem SQL estável por nome/id.
  Downloads de CSV carregam autorização do dashboard e escapam fórmulas de planilha.

## [0.3.0] — 2026-10-13

### Added

- **Brain Codex opt-in (plano ChatGPT).** Defina `brain.provider: codex` (ou escolha
  em `harvey setup`, ou `harvey train --provider codex`) para pensar com o
  Codex CLI numa assinatura ChatGPT em vez do Claude. O Claude continua sendo o
  padrão e não há fallback automático entre provedores. Cada chamada
  roda um `codex app-server` isolado e descartável sem ferramentas; o Harvey verifica
  o bloqueio a partir dos próprios relatórios do Codex antes de enviar qualquer prompt, aborta em
  qualquer tentativa de uso de ferramenta, recusa logins por API key e endpoints
  personalizados (checado antes do seu login ser exposto ao Codex), e nunca muda suas próprias
  configurações ou login do Codex: cada chamada recebe uma cópia privada do login sem
  seu refresh token, então um login expirado deve ser renovado com o próprio Codex ou
  `codex login`. Exige Codex CLI 0.159.3; outras versões são recusadas. Veja
  a seção do README "Using a ChatGPT plan instead (Codex)".
- `brain.model` escolhe o modelo para qualquer provedor, para o Harvey apenas. Para
  Codex use `gpt-5.5` (sugerido por `harvey setup`): o modelo comprovadamente
  texto-apenas. Seleção automática em branco só escolhe modelos listados sem ferramentas de
  execução de código, e nas contas ChatGPT atuais não há nenhum; modelos em code-mode são
  recusados.
- Se o Codex não puder ser usado (login expirado ou com renovação pendente, CLI não suportado,
  configuração do Codex insegura, modelo rejeitado, limite de uso do plano), o Harvey pausa o
  heartbeat em vez de rodar agentes que falhariam: respostas ficam sem ler
  e sem escalar, e-mails enfileirados esperam, e o motivo aparece no log,
  `harvey status` e no dashboard. Retoma sozinho quando a causa é
  corrigida. `harvey status --check` roda a mesma checagem (nenhum prompt enviado) sob demanda
  e sai com código diferente de zero quando falha. O provedor Codex suporta macOS e
  Linux; é recusado no Windows (use o Claude lá).

### Changed

- Cada heartbeat agora envia e-mail depois que os agentes que leem e respondem
  respostas terminaram, e provedores nativos de mail (Gmail/SMTP) leem a
  caixa a cada ciclo, então uma resposta sempre cancela seus follow-ups enfileirados antes
  dos envios daquele ciclo (antes os dois podiam rodar ao mesmo tempo, e uma
  resposta chegando sem conversa aberta esperava por um ciclo posterior). Isso
  se aplica igualmente a Claude e Codex.
- Uma resposta só é registrada depois que seu rascunho de resposta (se precisar de um) é
  escrito, então uma queda do brain no meio nunca a registra pela metade. Se um brain
  funcionando não retorna rascunho utilizável, a conversa é sinalizada para um humano
  em vez de ficar aberta sem resposta.
- O uso é rastreado por provedor. O portão de orçamento, `harvey usage`, `harvey
  status` e o dashboard leem e rotulam a própria cota do provedor ativo;
  o histórico de uso existente é mantido e atribuído ao Claude.

### Fixed

- Os ativos HTML e de texto do dashboard agora usam UTF-8 explicitamente, corrigindo falhas
  de decodificação no Windows. Testes de regressão cobrem HTML, CSS, JavaScript e SVG.

## [0.2.1] — 2026-10-13

Uma versão de segurança. Atualize se você roda o Harvey.

### Security

- **O Claude agora roda sem ferramentas.** Toda chamada do Claude costumava rodar com
  `--dangerously-skip-permissions`, e prompts incluem texto que o Harvey não
  controla: respostas de e-mail de prospects e páginas web raspadas. Instruções escondidas
  nesse texto podiam fazer o Claude rodar comandos, ler ou gravar arquivos, ou usar
  servidores MCP conectados do operador. Chamadas agora rodam com `--tools ""` e
  `--strict-mcp-config`; o Harvey só precisava de texto de volta, então nada mais
  muda. Reportado em particular por [@hackchang](https://github.com/hackchang).
  Se você rodou uma versão anterior com respostas ao vivo chegando, verifique
  a conta que rodou o Harvey por arquivos ou atividade inesperada.

### Fixed

- `harvey run` não cai mais no assistente de setup quando a configuração treinada
  vive em `harvey.local.yaml`; o dashboard também a lê.
- Um ciclo de heartbeat é limitado a 10 minutos, então um agente travado não congela o
  Harvey, e as horas de silêncio são rechecadas a cada 5 minutos para que um Mac acordando do
  sono retome no horário.
- Sites que só respondem em HTTP puro ou em `www.` não são mais marcados como
  inalcançáveis.
- Preenchimentos de perfil e contato rotacionam por todas as empresas em vez de
  tentar as mesmas poucas para sempre.
- O treinador grava nomes de lugar completos ("Solon, Ohio") e cargos reais, então o
  discovery não geocodifica para a cidade errada e contatos encontrados não são
  descartados em silêncio.

### Added

- Contatos são preenchidos para empresas encontradas sem nenhum, a partir das próprias páginas de equipe
  e, se uma chave estiver definida, da busca de pessoas nomeadas do Hunter.
- `HUNTER_MONTHLY_SEARCHES` (padrão 25) define um orçamento do Hunter compartilhado por toda
  busca de domínio.

Obrigado a [@sshaw0729-dotcom](https://github.com/sshaw0729-dotcom) pelas
correções acima (#2).

## [0.2.0] — 2026-09-13

A versão que fez o Harvey valer a pena rodar. A versão anterior sabia escrever
e enviar e-mail mas não conseguia encontrar ninguém para enviar de forma confiável, e precisava
de uma plataforma paga de terceiros para enviar. Ambos foram corrigidos.

### Added

- **Um pipeline de prospecção que funciona.** Quatro estágios, cada um executável e
  reexecutável de forma independente: DISCOVER (quem existe) → PROFILE (o que são) →
  ENRICH (quem decide) → VERIFY (você consegue alcançá-los).
- **DISCOVER, com um menu de provedores.** Quatro fontes atrás de uma interface
  de adaptador, mostradas lado a lado no dashboard com o que cada uma faz, quanto
  custa, sua cota gratuita e quais chaves precisa. O padrão — OpenStreetMap —
  não precisa de conta, cartão nem chave, então todo o pipeline pode rodar
  antes de pagar a alguém. `harvey discover`.
- **Disciplina de custo no coletor.** Toda execução de discovery estima antes de
  gastar, recusa iniciar acima do seu teto, recheca o teto entre lotes,
  lê um kill switch, e grava observações por lote para que uma execução que morre
  mantenha o que aprendeu. `harvey discover --estimate` imprime a projeção e
  sai.
- **PROFILE.** Gratuito: três requisições HTTP por negócio, sem navegador, sem chamada de modelo.
  Lê a agência atual do rodapé do site, pixels de anúncio, schema faltando, blogs
  abandonados, vagas abertas e pessoas nomeadas. Encadeado ao DISCOVER
  e rodado a cada heartbeat. `harvey profile`.
- **Um catálogo de sinais que você confirma.** O Harvey sabe coletar 23 sinais e
  não coleta nenhum até um humano dizer. Cada um mostra uma
  descrição em linguagem simples, o que custa, e quantas empresas já o
  carregam. `harvey signals`.
- **O construtor de cohort.** Escolha o que um prospect deve ter e o que o desqualifica;
  veja as empresas correspondentes ao vivo. Uma lista de prospects é uma consulta que você pode
  explicar, não um arquivo.
- **Provedores de mail nativos.** Gmail (REST + OAuth) e qualquer caixa SMTP+IMAP.
- **A escada de aprovação do outbox.** Todo e-mail de saída espera aprovação por
  padrão (`pending_review → approved → sent`), revisado um a um numa
  mesa de decisões com `A`/`R`/`J`/`K`. Um portão pré-envio determinístico — sem modelo
  envolvido — rejeita merge tags não renderizadas, frases proibidas, corpos longos demais,
  links demais, HTML, endereços não entregáveis e descasamentos de destinatário.
- **Tratamento de bounce e um kill switch.** Um bounce marca o endereço inválido,
  cancela os envios enfileirados daquele prospect, e dispara uma pausa global acima de uma
  taxa de bounce configurada. `harvey sending pause|resume`.
- **Rastreamento de uso do Claude.** Atribuição por chamada por agente, tarefa e modelo, mais
  medidores ao vivo de cota da assinatura lidos do mesmo jeito que `/usage`, para que o Harvey
  se estrangule e deixe espaço para seu próprio trabalho interativo.
  `harvey usage`.
- **Exportação CSV.** `harvey export` grava uma lista pronta para sequenciador. O Harvey vale
  a pena rodar como construtor de lista mesmo se você nunca o deixar enviar.
- **Um dashboard que vale a pena olhar.** Abre no Today — o que precisa de
  um humano — com um feed de atividade e uma trilha de números do pipeline, execuções do coletor e setup.
  Claro e escuro são o mesmo design re-tokenizado; a aparência segue o seu SO por
  padrão. As fontes são embarcadas para renderizar com a rede desligada.
- **Um guard de versão do Python.** `python3 -m venv` no macOS compila do 3.9 do sistema,
  que não roda o Harvey. Agora ele falha na hora com a correção em vez de
  aparecer mais tarde como um ImportError aparentemente sem relação.

### Changed

- **O modelo de dados.** Todo fato que o Harvey aprende agora é uma observação — uma linha em
  `observations`, nunca uma coluna. Um novo sinal não precisa de migração, re-observar
  ao longo do tempo é uma série temporal gratuita, e confiança e proveniência viajam com o
  fato. O vocabulário é governado: um trigger do banco rejeita qualquer código de sinal
  que não esteja em `signal_codes`.
- **A busca de e-mail é padrão-primeiro.** O Harvey deriva o formato de endereço do domínio
  e verifica um candidato em vez de forçar variações de nome, e
  classifica todo endereço honestamente como `verified` / `risky` / `guess` / `invalid`.
  Só endereços entregáveis são enviados.
- **O provedor padrão de mail** agora é `gmail`. O Instantly ainda é suportado como
  opção legada.
- **A profundidade do discovery passa a 30, não 100.** O Google removeu
  100 resultados por página em setembro de 2025, então a profundidade 100 agora é cobrada como dez
  páginas em quase todos os lugares — e abaixo da posição 30 é quase tudo diretório.
- **O HTML, CSS e JS do dashboard** são arquivos reais em `harvey/web/` em vez
  de uma string literal de 1.500 linhas em `dashboard.py`. Ainda sem passo de build.

### Fixed

- **E-mails adivinhados eram reportados como verificados** sempre que o domínio apenas
  tinha um registro MX. A migração rebaixa toda linha legada `email_verified=1`
  para `guess`.
- **Cohortes contavam as empresas erradas.** O PROFILE grava um booleano falso quando
  checa e não encontra nada — o que é correto — mas `cohort()` casava com a
  existência da linha, então "empresas rodando Google Ads" significava silenciosamente "empresas
  que checamos para Google Ads", que era todas. Cohortes agora leem a observação mais nova
  por empresa e sinal, e exigem que seja verdadeira.
- **O rastreamento de uso contava toda sessão do Claude na máquina**, não só
  as do Harvey. O reconciliador de transcrições foi removido; o ledger contém apenas linhas
  que o próprio Brain do Harvey escreveu.
- **Títulos de página eram extraídos como pessoas** ("Request Service", "Commercial
  Services"), e títulos vazavam entre membros da equipe.
- **Confirmar um sinal antes de qualquer coisa ter carregado o catálogo** reportava sucesso
  enquanto não mudava nada.
- **O provedor OSM gratuito respondia a termos de busca não mapeados com todo escritório
  registrado na área** — torrefações e igrejas para uma consulta de telhado. Agora ele
  recusa a consulta e nomeia os ramos que consegue buscar.

### Security

- As fixtures de teste não carregam mais telefones ou endereços
  de rua de negócios reais.
- `harvey.local.yaml` (no gitignore) sobrescreve o `harvey.yaml` versionado, então um
  fork pode guardar configuração real de produto sem que ela chegue a um repo público.

## [0.1.0]

Lançamento inicial: o loop de heartbeat, cinco sub-agentes, a biblioteca de skills, o
treinador de site, envio baseado em Instantly, e o primeiro dashboard.
