# Sinais e o pipeline de prospecção

## Você confirma o que ele procura

Esta é a parte que faz o Sellbird diferente de uma caixa-preta, e ela é deliberadamente impossível de pular.

O Sellbird sabe coletar **29 sinais** sobre uma empresa. Ele não coleta nenhum deles até você dizer. Na primeira execução ele *propõe* o catálogo; você confirma, pula ou rejeita cada um no dashboard ou pelo terminal:

```bash
sellbird signals                       # revisar o catálogo
sellbird signals --confirm free        # tudo que não custa nada (26 deles)
sellbird signals --confirm SERP_RANK   # um pago, adotado explicitamente
```

Todo sinal mostra o que é em linguagem simples, **quanto custa** e quantas empresas já o possuem.

| | Sinal | O que ele te diz |
|---|---|---|
| **Discovery** | `SERP_RANK` | Onde eles ranqueiam para sua própria busca principal, guardado com a frase de busca. As posições 11–30 são o ponto ideal: visíveis o bastante para estarem tentando, e perdendo. |
| | `IN_LOCAL_PACK` / `MAPS_RANK` | Se eles ocupam um dos três slots de mapa acima dos resultados, e onde ficam no Google Maps. |
| | `NO_WEBSITE` | Eles têm uma listagem e um telefone, e não têm site. Se você vende sites, é o sinal de maior intenção que existe. |
| | `UNCLAIMED_LISTING` | Ninguém reivindicou o Google Business Profile deles. |
| | `REVIEW_RATING` / `REVIEW_COUNT` | Bons mas invisíveis, ou visíveis mas sofrendo. |
| **Profile** | `INCUMBENT_AGENCY` | Quem tem a conta hoje, creditado no próprio rodapé deles. Cada detecção monta um cadastro que você pode trabalhar como um portfólio inteiro de clientes. |
| | `RUNNING_GOOGLE_ADS` / `RUNNING_META_ADS` | Eles estão gastando em aquisição *hoje*. O sinal de orçamento mais forte disponível de graça. |
| | `NO_ONLINE_BOOKING` | Os leads têm que ligar, então a demanda fora do horário se perde. |
| | `NO_SCHEMA_MARKUP` | Uma lacuna de SEO concreta e verificável que você pode citar num e-mail. |
| | `BLOG_STALE` | Marketing de conteúdo começou e foi abandonado. |
| | `SITE_PAGE_COUNT`, `TECH_STACK`, `BLOCKS_AI_CRAWLERS` | Tamanho, plataforma, visibilidade em busca por IA. |
| | `HIRING_ROLE` / `OPEN_ROLES` | Para que estão contratando, e quantas vagas estão abertas. Quando o site deles linka um board do Greenhouse, Lever, Ashby ou Workable, o Sellbird lê o feed público desse board (uma requisição): vagas que correspondem a `icp.hiring_signals` (senão `icp.titles`), com departamento, local, data de publicação e a URL da vaga; quando o board não lista nenhuma, ele registra "não contratando" para que uma vaga fechada deixe de contar. Caso contrário, ele lê a página de carreiras. Defina `hiring_signals` como os cargos que significam que estão comprando: o fallback `titles` nomeia quem você contata por e-mail, então "CEO" só casa com uma vaga de CEO (nunca "Assistant to the CEO"), que raramente é o sinal que você quer. |
| | `YC_BACKED`, `ACCELERATOR`, `FUNDING_ROUND` | Uma startup, como o próprio site deles diz: YC ou outro acelerador (com a turma ou coorte), ou uma rodada que anunciaram (série, valor, data). |
| **People** | `CONTACT_FOUND`, `DECISION_MAKER_TITLE`, `LIKELY_OWNER`, `REGISTRY_VERIFIED` | Quem decide, e se é dono do negócio. |
| **Contact** | `EMAIL_PATTERN`, `EMAIL_STATUS`, `CONTACT_FORM_URL` | Se você realmente consegue chegar a eles. |

### Então uma coorte é uma consulta, não uma lista

Depois que os sinais são confirmados, o construtor de coortes do dashboard os transforma num conjunto-alvo — escolha o que um bom prospect **precisa ter**, o que o **desqualifica**, e uma **faixa** para sinais numéricos (rank orgânico 11 a 30), e ele conta as correspondências ao vivo:

```
Tem uma agência de marketing  AND  roda Google Ads  AND NOT  já tem agendamento online
→ 23 empresas
```

Isso é uma campanha com um motivo por trás. Você sabe exatamente por que cada uma dessas 23 está na lista, e o e-mail que o Sellbird escreve para elas também.

---

## O pipeline de prospecção

Quatro estágios. Cada um roda de forma independente, roda de novo com segurança e declara seu custo.

### 1. DISCOVER — quem existe

O único estágio que gasta dinheiro, então ele sempre estima primeiro e nunca chama nada até você mandar.

```bash
sellbird discover --providers   # o menu, com preços reais
sellbird discover --estimate    # gasto projetado, depois sai
sellbird discover               # vá
```

| Fonte | Custo | Plano gratuito | Melhor para |
|---|---|---|---|
| **OpenStreetMap** *(padrão)* | grátis | ilimitado, sem conta | Testar o pipeline inteiro antes de pagar a alguém. A cobertura é rasa para negócios sem ponto físico: o OSM mapeia imóveis, então setores inteiros quase não estão presentes (menos de 2.000 telhadores e menos de 2.300 encanadores em todos os EUA). O Sellbird diz isso na interface em vez de entregar de menos em silêncio. |
| **TinyFish** | grátis | 30 buscas por minuto, 500 por hora, sem cartão | Encontrar negócios por frase (incluindo os presets de startup e de contratação) sem custo. Não registra rank de busca: a ordenação dele não é a do Google e ele não aceita localização, então use Serper ou DataForSEO SERP para sinais de rank. |
| **DataForSEO Business Listings** | US$ 0,372 / 1.000 | US$ 1 de crédito | Setores locais, clínicas, prestadores. Telefone, domínio, avaliação, status de reivindicação — e ele pode filtrar por negócios **sem site nenhum**. |
| **DataForSEO SERP** | US$ 0,006 / busca com profundidade 30 (Live, US$ 0,002 por 10 resultados) | US$ 1 de crédito + sandbox grátis | Rank orgânico como sinal de compra, mais quem ocupa o 3-pack local, buscado do centro da cidade. |
| **DataForSEO Google Maps** | US$ 0,002 / busca (até 100 resultados) | US$ 1 de crédito + sandbox grátis | Rank no mapa, avaliação, categoria e status de reivindicação, incluindo negócios sem site. |
| **Serper** | ~US$ 0,30–1,00 / 1.000 | 2.500 grátis, sem cartão | O pago mais fácil de testar. |
| **Scavio Google Maps** | US$ 0,01 / página (até 20 listagens) | 50 créditos, sem cartão | Listagens do Google Maps em torno de cada cidade: telefone, site, categoria, avaliação e reviews, incluindo negócios sem site. |
| **Scavio Google Search** | ~US$ 0,03 / busca com profundidade 30 | os mesmos 50 créditos | Rank como sinal, com a mesma chave do Scavio Google Maps. |

**Vendendo para startups?** O Sellbird tem uma skill de startup embutida, feita de três
partes:

- **As buscas** (cada uma uma busca na web, então Serper ou DataForSEO SERP):

  | Preset | Encontra | Sinal |
  |---|---|---|
  | `yc` (*YC startups*) | Empresas cujo próprio site diz que são apoiadas pela Y Combinator | `YC_BACKED`, com a turma (W24, S23) |
  | `accelerator` (*Accelerator startups*) | As apoiadas pela Techstars, 500 Global, Antler, Entrepreneur First, South Park Commons, Neo, AI Grant, a16z speedrun ou Plug and Play (duas buscas por setor; o sinal também lê a Pioneer) | `ACCELERATOR`, com o programa e a coorte ("Techstars 2024") |
  | `funding` (*Recently funded*) | Empresas anunciando a própria rodada ("we raised", "announces $X Series A") nos últimos 18 meses, excluindo sites de notícias e bases de dados de funding | `FUNDING_ROUND`: série, valor e data |

  `sellbird discover --preset accelerator --provider serper`, ou o menu *Procurar por*
  na aba Descobrir.
- **Os sinais:** ligue-os na aba Sinais. Eles leem a homepage e a
  página About (e, no caso de uma rodada, a página que a busca encontrou no próprio site
  e a página de imprensa ou notícias) em busca de uma linha em que a empresa diz isso sobre si
  ("we went through Y Combinator", "Acme (Techstars '24)", "we raised a $4M
  seed round"), uma parede de logos "Backed by", ou um link para a própria página YC
  dela. Menções de cliente e audiência ("trusted by YC-backed startups", "we help founders raise
  their seed round") não contam. Muitas startups nunca dizem isso no site, então
  estes encontram as que dizem; um acerto de preset YC ou de acelerador também conta como sim.
  A data de uma rodada vem da própria cláusula, ou da data de publicação de um
  post de imprensa, notícia ou blog. Dinheiro que não é uma rodada (empréstimos fechados, veredictos
  ganhos, dinheiro arrecadado para uma caridade, a rodada de um investidor em outra empresa)
  não conta.
- **A redação:** o writer e o handler de respostas usam
  `skills/selling_to_startups.md`, um playbook para escrever a fundadores com uma
  seção sobre empresas que acabaram de captar, para empresas apoiadas por YC e aceleradoras
  e para rodadas datadas nos últimos 18 meses. Uma rodada mais antiga ou sem
  data sozinha não traz o playbook, e nunca é escrita como notícia.

O Sellbird nunca lê ycombinator.com, os diretórios das aceleradoras, Crunchbase,
PitchBook ou LinkedIn, cujos termos proíbem raspar; tudo vem dos
próprios sites das empresas e do seu provedor de busca.

**Procurando empresas contratando um cargo?** `sellbird discover --preset hiring
--provider serper` (ou *Procurar por: Empresas contratando para suas vagas*) busca
nos seus setores por empresas cujas próprias páginas de carreiras listam um dos seus
cargos `icp.hiring_signals` (senão `icp.titles`). Boards hospedados e sites de emprego
ficam de fora da busca, já que a página de um board nomeia um board, não um site
para perfilar. Confirme `HIRING_ROLE` e o profiling lê o board para o qual o site deles
leva e registra a vaga; o acerto da busca sozinho não registra nada.

As cidades se geocodificam sozinhas (em cache para sempre, uma consulta cada). Diretórios, agregadores e instituições são filtrados por padrão, não por blocklist — `en.wikipedia.org` e `biz.yelp.com` nunca entram.

> **Profundidade 20–30, não 100.** O Google removeu os 100 resultados por página em setembro de 2025, então profundidade 100 agora é cobrada como dez páginas em quase todo lugar. Abaixo do rank 30 é quase tudo diretório de qualquer forma.

### 2. PROFILE — o que eles são

**Grátis.** Três requisições HTTP por empresa. Sem navegador, sem chamada ao modelo. Este é o estágio de maior valor por esforço de todo o sistema, porque produz os fatos que tornam um e-mail específico.

Requisições de site do Scout, do Profile e do crawler de treinamento local são limitadas
a destinos HTTP(S) públicos. Toda resposta DNS e redirecionamento é conferido; endereços
locais, privados, link-local e de metadados são rejeitados. As conexões usam um
IP validado, preservando a identidade TLS do site. Esses clientes de site
ignoram proxies de ambiente, então o roteamento por proxy não consegue contornar essa fronteira.

Homepage, `robots.txt`, `sitemap.xml`, mais as páginas de equipe e de carreiras quando existem — depois regex sobre o HTML já em mãos. Sai a agência incumbente, os pixels de anúncio, o schema ausente, o blog abandonado, as vagas abertas, os humanos nomeados.

A detecção de agência é a que se acumula. Quase toda agência se credita no rodapé, e o Sellbird pontua o texto: *"Powered by"* / *"Website by"* → 0,9 de confiança; Um link descritivo sem rótulo → 0,75; um link sem rótulo → 0,35 — mas um link sem rótulo é **não registrado**. Uma incumbente errada num e-mail é pior que dizer nada.

### 3. ENRICH — quem decide

O dono, a partir do próprio site da empresa. O Sellbird lê a homepage e segue o menu do próprio site até as páginas onde as pessoas são nomeadas — equipe, sobre, nossa história, conheça os dentistas, advogados, contato — no máximo seis páginas, pulando links que voltam para a homepage. Nessas páginas ele lê:

- **cards e listas**: um nome com um cargo abaixo, mesmo quando o cargo está só a um `<br>` de distância dentro de um span;
- **frases**: "owned and operated by Gary Pruitt", "led today by President Ilan Brooks", "Ines Varga started Countwise";
- **schema.org**: as próprias entradas `founder` e `employee` da empresa (o autor de um post de blog não é funcionário);
- **o nome na porta**: quando duas pessoas têm cargos de dono, vem primeiro quem tem o sobrenome no nome do negócio. Um sobrenome sozinho nunca faz de ninguém o dono: Linda Smith, Office Manager, na Smith & Sons não é uma.

Donos vêm primeiro, e no máximo duas pessoas por empresa se tornam prospects. Títulos feitos de palavras comuns ("Team of Experts"), clientes citados em depoimentos ou tweets ("Founder at Quillnest"), diretores de outras organizações ("KTR President Vic Hale"), donos antigos ou falecidos ("Past President", "the late Harold Smith") e slogans não são pessoas. Os cargos casam com seu ICP por palavra inteira: "Vice President" não conta como "President" a menos que você o liste, e Proprietor, Principal, Managing Partner, Founder e CEO contam como dono. Com `LIKELY_OWNER` confirmado, cada dono é registrado como uma observação com a evidência que o indica.

Quando o site de uma empresa não nomeia ninguém, ou nomeia um dono cujo endereço é só um palpite, e o Sellbird ainda não tem contato ali — comum em setores pequenos —, ele também usa um endereço geral que a empresa imprime nas próprias páginas (apenas caixas gerais como `owner@`, `office@`, `info@` ou `hello@`, nunca o endereço pessoal de alguém). O Sellbird lê páginas inteiras em busca dele, incluindo schema.org e endereços escondidos de scrapers, e aceita um endereço em outro domínio apenas quando aquele domínio leva ao site da própria empresa. Ele nunca é adivinhado, é verificado como qualquer outro endereço, e esses e-mails saúdam a equipe da empresa em vez de um primeiro nome.

Um site atrás de um desafio de bot (o "sgcaptcha" da SiteGround, o "Just a moment…" da Cloudflare) é relatado como desafiado, não inacessível, e não é tentado de novo.

### 4. VERIFY — você consegue chegar a eles

O Sellbird aprende o **padrão de endereço** de cada empresa e verifica um candidato, em vez de tentar por força bruta variações de nome. Qualquer endereço que o site publique pode ensiná-lo: `nvale@` ao lado de Nora Vale é `{first initial}{last}`, e `j.smith@` é uma inicial e um sobrenome. Um endereço solto sem ponto que nenhuma pessoa nomeada tem (`kmorrow@`: Kmorrow, ou K. Morrow?) é ambíguo e não ensina nada. Um endereço que duas pessoas nomeadas poderiam ter (`jsmith@` quando John e Jane Smith trabalham ali) é só evidência de formato, e o Sellbird nunca adivinha ou verifica um endereço que outra pessoa nomeada poderia ter: um verificador confirmaria a caixa *dela*. Ele decodifica os truques usuais de ocultação (Cloudflare email protection, os atributos `data-user`/`data-domain` de um link de e-mail, `name [at] domain [dot] com`) e nunca inventa um endereço a partir de texto comum. O endereço publicado pela própria pessoa é usado como está. Sem nenhuma evidência, ele chuta `first.last@`, ou `first@` quando algo além do site diz que a empresa é pequena (o tamanho de empresa do seu ICP, ou uma listagem de negócio local como fonte). Um palpite em cache nunca impede que um endereço real ou uma consulta ao Hunter o substitua, e o Hunter é consultado uma vez por domínio (um timeout ou limite de taxa não conta). O probing SMTP bruto não é viável a partir de um laptop — a porta 25 de saída costuma estar bloqueada, e o Google Workspace e o Microsoft 365 aceitam tudo de um IP desconhecido.

Todo endereço é marcado com honestidade: `verified` / `risky` (catch-all) / `guess` / `invalid`. **Só os entregáveis são enviados.** Um palpite nunca é tratado como acerto.

> O Sellbird vale a pena rodar mesmo que você nunca o deixe enviar. `sellbird export` grava um CSV pronto para sequenciador de tudo o que ele encontrou.
