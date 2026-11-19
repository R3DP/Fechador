# Skills

Skills são arquivos Markdown editáveis que dão ao Sellbird conhecimento fundamental de vendas. Cada agente carrega as skills de que precisa antes de tomar decisões.

## Como as Skills Funcionam

Quando um agente roda, ele chama `brain.load_skills_for_agent("agent_name")`, que concatena os arquivos de skill relevantes e os injeta no prompt. Isso significa que você pode mudar o comportamento do Sellbird editando esses arquivos — sem precisar mudar código.

## Mapa Skill → Agente

| Skill | Scout | Writer | Handler | Sender | LinkedIn |
|-------|-------|--------|---------|--------|----------|
| `prospecting_tactics.md` | x | | | | x |
| `lead_qualification.md` | x | | | | |
| `account_navigation.md` | x | | | | |
| `signal_playbook.md` | x | x | | | |
| `email_frameworks.md` | | x | | x | |
| `sales_methodology.md` | | x | x | | |
| `offer_strategy.md` | | x | x | | |
| `objection_handling.md` | | | x | | |
| `linkedin_outreach.md` | | | | | x |
| `product_knowledge.md` | x | x | x | x | x |
| `competitive_intel.md` | | x | x | | |
| `selling_to_startups.md` | | x* | x* | | |

\* Só para prospects cuja empresa é uma startup segundo o próprio site dela (o sinal `YC_BACKED` ou `ACCELERATOR`, ou um `FUNDING_ROUND` dos últimos 18 meses), não carregada para todo mundo.

## Skills Embutidas

- **`prospecting_tactics.md`** — consultas de Google dorking, raspagem do site da empresa, eventos-gatilho, mineração de indicações
- **`lead_qualification.md`** — triagem BANT, pontuação de ICP, framework MEDDIC, critérios de desqualificação
- **`account_navigation.md`** — tratamento de múltiplos contatos, estratégia de ponto de entrada, regras de multi-threading
- **`selling_to_startups.md`** — como escrever para fundadores em estágio inicial: quem lê, timing em torno de uma turma de YC ou aceleradora e do Demo Day, como escrever para empresas que acabaram de captar (e quando uma captação é velha demais para mencionar), o que não fazer, como lidar com as respostas deles. Usada automaticamente para prospects apoiados por YC, apoiados por aceleradora e com captação recente.
- **`signal_playbook.md`** — transformar sinais de compra (contratação, stack de tecnologia, captação) na primeira linha do e-mail; qual sinal vence quando há vários; usar uma vaga de emprego como gancho sem adivinhar nem sugerir conhecimento interno
- **`email_frameworks.md`** — regras de copywriting de e-mail frio, padrões de IA proibidos, dados de taxa de resposta de 2026 (tamanho, CTAs de oferta, cadência, sem rastreamento), a sequência de 3 e-mails (Observação, Ângulo, Rompimento), linhas de assunto, personalização
- **`sales_methodology.md`** — Loop ABC, fluxo de conversa, calibração de tom, diretrizes éticas
- **`offer_strategy.md`** — escada de ofertas por nível de engajamento, mecânica de fechamento, regras de timing
- **`objection_handling.md`** — framework LAARC, 4 categorias de objeção com respostas
- **`linkedin_outreach.md`** — sequências de conexão, modelos de mensagem, limites de taxa

## Skills Geradas Automaticamente

Estas são criadas por `sellbird train <url>` e são específicas do seu produto:

- **`product_knowledge.md`** — funcionalidades, benefícios, preços, casos de uso, dores, gatilhos de compra
- **`competitive_intel.md`** — battle cards para cada concorrente, ângulos de diferenciação, caminhos de migração

## Adicionando ou Editando Skills

1. Edite qualquer arquivo `.md` neste diretório
2. As mudanças passam a valer no próximo ciclo de heartbeat (sem precisar reiniciar)
3. Para adicionar uma nova skill, crie o arquivo e o adicione ao `skill_map` em `sellbird/brain.py`
