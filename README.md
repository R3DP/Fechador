<p align="center">
  <a href="https://sellbird.ai">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="docs/brand/sellbird-wordmark-white.svg">
      <img src="docs/brand/sellbird-wordmark.svg" alt="Sellbird" width="300">
    </picture>
  </a>
</p>

<p align="center"><strong>A plataforma de prospecção open source que roda no seu plano Claude ou ChatGPT.</strong></p>

<p align="center">
O Sellbird encontra empresas que precisam do que você vende, encontra a pessoa que decide, confere o endereço de e-mail dela, escreve um e-mail frio personalizado para cada uma, envia e cuida das respostas.
Roda na sua própria máquina e, por padrão, nada sai até você aprovar.
</p>

<p align="center">
  <a href="https://x.com/sellbirdagent"><img alt="Siga @sellbirdagent no X" src="https://img.shields.io/badge/follow-%40sellbirdagent-000000?logo=x&logoColor=white"></a>
  <a href="https://github.com/ethanplusai/sellbird/stargazers"><img alt="Estrelas no GitHub" src="https://img.shields.io/github/stars/ethanplusai/sellbird?style=flat&logo=github&label=stars&color=244b62&cacheSeconds=3600"></a>
  <a href="https://github.com/ethanplusai/sellbird/actions/workflows/tests.yml"><img alt="Testes" src="https://github.com/ethanplusai/sellbird/actions/workflows/tests.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="Licença: AGPL-3.0" src="https://img.shields.io/badge/license-AGPL--3.0-244b62"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-244b62?logo=python&logoColor=white">
  <a href="https://sellbird.ai"><img alt="Hospedado em sellbird.ai" src="https://img.shields.io/badge/hosted-sellbird.ai-244b62"></a>
  <a href="https://sellbird.ai/harvey/"><img alt="Antes, Harvey" src="https://img.shields.io/badge/formerly-Harvey-8aa0ad"></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/303676?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-303676" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/303676" alt="ethanplusai%2Fsellbird | Trendshift" width="250" height="55"/></a>
</p>

> **[O Harvey agora é Sellbird.](https://sellbird.ai/harvey/)** Mesmo projeto, mesmo histórico, nome novo. Já usa o Harvey? Sua configuração continua valendo: veja [Atualizando a partir do Harvey](#atualizando-a-partir-do-harvey).

**Novidades de versões, funcionalidades e o roadmap saem primeiro no X: [siga @sellbirdagent](https://x.com/sellbirdagent).**

**Prefere não rodar você mesmo? [sellbird.ai](https://sellbird.ai) é a versão hospedada, com domínios de envio, caixas de entrada e aquecimento configurados para você. Está em acesso antecipado.**

![Dashboard do Sellbird: a tela Hoje, uma conversa que precisa de você, aprovando uma resposta redigida na Caixa de saída, os sinais a confirmar, a busca de contatos e, por fim, o modo escuro](docs/dashboard.gif)

<sub>Os dados da demonstração são inventados: a "Bookwell" vende agendamento online para empresas de telhado, consultórios odontológicos e lojas de HVAC, em domínios `.test`.</sub>

## O que ele faz

O Sellbird é um pipeline que você pode rodar de ponta a ponta ou parar em qualquer etapa.

| | O que acontece | Mais |
|---|---|---|
| **Encontra empresas** | Busca empresas que combinam com o seu cliente: grátis no OpenStreetMap ou em uma fonte paga que você escolher. Toda busca paga mostra o custo antes de rodar. | [Descoberta](docs/signals-and-pipeline.md#1-discover--who-exists) |
| **Entende por que comprariam** | Lê o site de cada empresa em busca dos sinais de compra que você confirmou, como não ter agendamento online, estar anunciando ou estar contratando para um cargo. Nenhuma chamada de modelo, nenhum custo. | [Sinais](docs/signals-and-pipeline.md) |
| **Encontra quem decide** | Encontra o dono ou gerente nomeado nas próprias páginas da empresa, no máximo duas pessoas por empresa. | [Enriquecer](docs/signals-and-pipeline.md#3-enrich--who-decides) |
| **Confere o endereço** | Descobre o padrão de e-mail da empresa e verifica um endereço. Todo endereço é marcado como verificado, arriscado, suposição ou inválido, e só os entregáveis são usados para envio. | [Verificar](docs/signals-and-pipeline.md#4-verify--can-you-reach-them) |
| **Escreve e envia** | Escreve uma sequência curta para cada pessoa com base no que encontrou e envia pela sua caixa do Gmail, Microsoft 365 ou SMTP, dentro do seu limite diário e do horário comercial deles. | [Envio](docs/approval-and-sending.md) |
| **Cuida das respostas** | Lê toda resposta, redige uma resposta, separa as respostas automáticas, respeita as recusas na hora e entrega a você tudo o que não deveria responder sozinho. | [Dashboard](docs/dashboard.md) |

Só quer a lista? Pare depois da verificação e rode `sellbird export` para um CSV pronto para sequenciador com tudo o que encontrou.

```
$ sellbird run

============================================================
Sellbird is online.
============================================================
Checking pipeline state...
Decision: write_campaign (3 new prospects with no drafts)
  handler   → Elena Park, Harbor Dental Studio     interested, answer drafted
  handler   → Priya Nair, Highline Roofing         objection, answer drafted
  writer    → 2-email sequence: Phoenix HVAC hiring a dispatcher
  outbox    → 5 emails waiting for your approval
Cycle complete. Sleeping for 15 minutes.
```

## Sem conta de API de modelo

O Sellbird pensa pelo CLI do Claude Code no seu plano Claude Pro ou Max, ou pelo Codex em um plano ChatGPT. Não há chave de API nem cobrança por token, e o Sellbird se limita para deixar espaço para o seu próprio trabalho.

| | |
|---|---|
| Claude Pro ou Max, ou um plano ChatGPT com Codex | a assinatura que você já tem |
| Encontrar empresas | **$0** na fonte padrão, ou cerca de $0,37 por 1.000 na fonte paga mais barata |
| Ler os sites delas | **$0**: três requisições HTTP por site, nenhuma chamada de modelo |
| Escrever e enviar | sua assinatura e uma caixa de e-mail (cerca de $7 por mês no Google Workspace) |
| Ferramentas de prospecção | **Nenhuma.** Nada de Apollo, ZoomInfo, Clearbit ou Clay. |

Como o ciclo, o orçamento e o isolamento funcionam: [Como o Sellbird funciona](docs/how-it-works.md).

## Início rápido

Você precisa de:

- **Python 3.11 ou mais recente.** O macOS vem com o 3.9, então rode `brew install python@3.13` primeiro se `python3 --version` mostrar isso.
- **Claude Pro ou Max** com o CLI conectado (`claude login`), ou um **plano ChatGPT com o Codex CLI** ([configuração do Codex](docs/codex.md)).
- **Uma caixa de e-mail para enviar**, de preferência Google Workspace em um domínio de envio separado. [Microsoft 365](docs/microsoft365.md) e SMTP também funcionam.
- **Aquecimento nessa caixa de e-mail.** Recomendamos o [TrulyInbox](https://trulyinbox.com/?via=sellbird): ele aquece uma caixa nova antes do e-mail frio e a mantém fora do spam depois, e o Sellbird lê a taxa de entrega na caixa para avisar quando você estiver pronto.

### Deixe o Claude configurar

```bash
git clone https://github.com/ethanplusai/sellbird.git
cd sellbird
claude
```

Depois diga **"configure o Sellbird para mim"**. O `CLAUDE.md` do repositório transforma o Claude Code no guia de configuração: ele verifica onde você está, instala o que falta, pergunta o que precisa e treina o Sellbird no seu produto.

### Ou faça você mesmo

```bash
# 1. Instale. Use python3.13, não python3: no macOS o python3 puro é 3.9.
python3.13 -m venv .venv && source .venv/bin/activate && pip install -e .

# 2. Adicione as credenciais. Cada variável está documentada no próprio arquivo.
cp .env.example .env && $EDITOR .env

# 3. Aprenda seu produto a partir do seu site (grava sellbird.local.yaml).
sellbird train https://your-company.com

# 4. Confirme o que faz um bom prospect.
sellbird signals --confirm free

# 5. Encontre empresas. A fonte padrão é grátis e não precisa de conta.
sellbird discover

# 6. Abra o dashboard e inicie o ciclo.
sellbird dashboard          # imprime um link privado para http://127.0.0.1:5555
sellbird run
```

No Linux você também pode [rodar com Docker](docs/docker.md).

## Nada é enviado sem você

Todo e-mail de saída espera na Caixa de saída pela sua aprovação até você ligar o piloto automático por conta própria. Antes de qualquer coisa sair, uma checagem de pré-envio, sem modelo envolvido, rejeita tags de mesclagem não preenchidas, frases proibidas, e-mails longos demais, links extras e endereços não entregáveis. O piloto automático ainda segura qualquer e-mail que aponte para um domínio que não é seu ou cite instruções do próprio Sellbird. `sellbird sending pause` para tudo de uma vez.

Detalhes: [Aprovação e envio](docs/approval-and-sending.md) e [Legal e entregabilidade](docs/deliverability.md).

## Atualizando a partir do Harvey

O Harvey foi renomeado para Sellbird na 0.4.0. Sua configuração, seus dados e o login do dashboard continuam valendo:

```bash
git pull
pip install -e .        # uma vez, para ter o novo comando `sellbird`
sellbird dashboard
```

- Na primeira execução, o Sellbird renomeia `harvey.local.yaml` para `sellbird.local.yaml` e `data/harvey.db` (e o respectivo log) para `data/sellbird.*`. Ele nunca sobrescreve um arquivo que já existe com o novo nome e espera se um processo do Harvey ainda estiver rodando a partir da pasta. Pare esse processo antes.
- Variáveis de ambiente `HARVEY_*` ainda funcionam quando a `SELLBIRD_*` equivalente não está definida; renomeie-as quando for conveniente.
- O comando `harvey` e `python -m harvey` ainda funcionam por enquanto e avisam que mudaram de lugar. Serão removidos em uma versão futura.
- Se você editou o `harvey.yaml` versionado diretamente, o `git pull` para com "your local changes would be overwritten". Rode `git stash`, `git pull` e depois `git stash pop`. O Git leva suas edições para o `sellbird.yaml`. Se ele acusar conflito ali, mantenha suas linhas, apague os marcadores de conflito e rode `git stash drop`. Melhor ainda, coloque suas configurações em `sellbird.local.yaml`, que o Git nunca toca.
- Docker: o serviço agora se chama `sellbird`. Rode `docker compose down`, `git pull`, `docker compose build` e depois `docker compose up -d`. `HARVEY_UID`/`HARVEY_GID` ainda são lidos.

Links para `github.com/ethanplusai/harvey` continuam funcionando: o GitHub redireciona para cá.

## Onde ficam seus arquivos

Sua configuração, seu conhecimento e seus dados ficam em uma pasta home. Qual, vence a primeira correspondência:

1. `SELLBIRD_HOME`, se você definir (a imagem Docker a define como `/app`).
2. Um checkout: a própria pasta do checkout, como antes.
3. Caso contrário, para um pacote instalado (`pip` ou `pipx`), sua pasta de dados do usuário:

| | Pasta home |
|---|---|
| macOS | `~/Library/Application Support/sellbird` |
| Windows | `%APPDATA%\sellbird` |
| Linux | `~/.local/share/sellbird` (ou `$XDG_DATA_HOME/sellbird`) |

Dentro dela ficam `sellbird.yaml` (e `sellbird.local.yaml` depois que você treinar), `.env`,
`prompts/` e `skills/`, tudo seu para editar. Um pacote instalado copia os padrões na
primeira execução e nunca os sobrescreve, então suas edições sobrevivem às atualizações. `data/` guarda o
banco de dados, os logs e o token do dashboard.

## Documentação

| Guia | O que tem |
|---|---|
| [Como o Sellbird funciona](docs/how-it-works.md) | O ciclo de heartbeat, o orçamento da assinatura, a estrutura do projeto e as ideias por trás |
| [Sinais e o pipeline de prospecção](docs/signals-and-pipeline.md) | Os 29 sinais, as coortes e as etapas de descoberta, perfil, enriquecimento e verificação |
| [Skills e sub-agentes](docs/skills-and-agents.md) | Os playbooks de vendas editáveis e qual agente usa qual |
| [Aprovação e envio](docs/approval-and-sending.md) | A Caixa de saída, o piloto automático, o horário comercial e as assinaturas de e-mail |
| [O dashboard e os dados](docs/dashboard.md) | Todas as telas, como funciona o login e como os dados são armazenados |
| [Configuração e comandos](docs/configuration.md) | `.env`, `sellbird.yaml` e todos os comandos |
| [Extensões](docs/extensions.md) | Adicionar rotas, etapas de heartbeat e comandos a partir de um pacote separado |
| [Usando um plano ChatGPT (Codex)](docs/codex.md) | Rodar no Codex em vez do Claude |
| [Legal e entregabilidade](docs/deliverability.md) | As regras sob as quais você envia e o aquecimento |
| [Microsoft 365](docs/microsoft365.md) · [Precleared](docs/precleared.md) | Guias de configuração de provedores |
| [Docker](docs/docker.md) · [Solução de problemas](docs/troubleshooting.md) · [Roadmap](docs/roadmap.md) | Rodar, corrigir e o que vem a seguir |

## Contribuindo

Pull requests são bem-vindos. Leia o [CONTRIBUTING.md](CONTRIBUTING.md) primeiro: ele trata de manter dados de contato reais fora do repositório, e-mail de teste e sign-off dos commits. Encontrou um problema de segurança? Siga o [SECURITY.md](SECURITY.md) em vez de abrir uma issue.

Veja o [CHANGELOG.md](CHANGELOG.md) para o que mudou em cada versão e [siga @sellbirdagent no X](https://x.com/sellbirdagent) para saber das novidades primeiro.

## Licença

O Sellbird é licenciado sob a [GNU Affero General Public License v3.0](LICENSE). As versões do Harvey até a 0.3.x foram lançadas sob MIT, e esse código mantém seu aviso MIT em [NOTICE](NOTICE).

Os links do TrulyInbox neste projeto são links de afiliado: o mantenedor pode receber uma comissão, sem custo extra para você.
