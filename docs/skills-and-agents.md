# Skills e sub-agentes

## A biblioteca de skills

O conhecimento de vendas do Sellbird fica em `skills/` como **Markdown simples que você
pode editar**. Não há fine-tuning, nem vector store, nem etapa de recuperação. Antes de
um agente rodar, as skills de que ele precisa são concatenadas direto no prompt dele.
Mude um arquivo e o próximo heartbeat se comporta diferente — sem reinício, sem mudança
de código.

Esta é a principal forma de moldar o Sellbird. Se os e-mails são agressivos demais, edite
`email_frameworks.md`. Se ele trata mal uma objeção específica, edite
`objection_handling.md` e adicione a resposta que você realmente daria.

**Seu próprio formato de e-mail.** Diga o que as skills disserem, o Writer termina todo
prompt com um formato nativo: e-mail 1 com menos de 75 palavras, uma observação e uma
pergunta, sem pitch, sem link. Se seu primeiro e-mail precisa fazer mais (dizer quem você
é, quanto custa, linkar para uma página de cadastro), escreva suas regras em um arquivo
markdown e aponte `writer.email_rules` para ele:

```yaml
writer:
  email_rules: "skills/email_rules.md"   # gitignored
```

O arquivo substitui o formato nativo para o primeiro e-mail individual e para a sequência
de 3 e-mails, e vence o `email_frameworks.md` e as regras de estilo do prompt onde eles
divergirem. Ele não pode revogar a regra de FATOS (nada sobre um prospect é inventado), e
o bloqueio de envio continua valendo: no máximo 220 palavras e um link por e-mail, e a
lista de não contatar. Se `compliance.opt_out_line` estiver definido, o Sellbird o
adiciona sob cada e-mail frio e instrui o Writer a não escrever um segundo; deixe-o vazio
e suas regras podem colocar uma frase de opt-out no corpo (o Sellbird ainda avisa, já que
não consegue verificar sua frase). As verificações nativas de frases de opt-out do
Sellbird cobrem inglês, hebraico, espanhol e francês; o modelo ainda lê toda resposta em
busca de um pedido de parada, em qualquer idioma. Um arquivo definido mas ausente, vazio
ou com mais de 20.000 caracteres para o Writer até ser corrigido, em vez de rascunhar no
formato que você substituiu.

### O que vem junto

**`email_frameworks.md`** — 301 linhas, o arquivo mais importante do repositório. Abre com
a única regra que importa: *escreva como uma pessoa real enviando um e-mail real.* Contém
uma lista de banimento rígida contra marcas de IA (sem "I hope this finds you well", sem
"I wanted to reach out", sem "circling back"), regras de conformidade que se sobrepõem a
toda regra de estilo abaixo delas, dados de taxa de resposta de 2026 sobre tamanho e
cadência e por que o rastreamento de links prejudica você, e cinco frameworks — **AIDA,
PAS, BAB, QVC, 3Ps** — com regras de seleção para quando cada um se encaixa.

**`signal_playbook.md`** — Como transformar um sinal na primeira linha de um e-mail. Qual
sinal vence quando uma empresa tem vários. Como referenciar algo que você observou sem
soar como se tivesse rodado uma varredura nela.

**`objection_handling.md`** — O laço **LAARC** (Listen → Acknowledge → Assess → Respond →
Confirm) com respostas trabalhadas nas quatro famílias de objeção: orçamento, autoridade,
necessidade, prazo. A linha de raciocínio é que você não está "superando" uma objeção,
está descobrindo qual é a preocupação real.

**`lead_qualification.md`** — **BANT** para a primeira triagem, pontuação de ICP de 1 a 10
para priorização, **MEDDIC** para qualquer coisa complexa. Inclui critérios explícitos de
desqualificação, que importam mais que os de qualificação.

**`sales_methodology.md`** — A filosofia operacional: o laço ABC, como uma conversa deve
fluir entre estágios, calibração de tom e as linhas éticas que o Sellbird não cruza.

**`offer_strategy.md`** — A escada de ofertas por nível de engajamento e a regra que a
governa: *nunca lidere com uma oferta, nunca faça pitch em um e-mail frio.* O primeiro
contato existe para começar uma conversa. Ofertas só saem depois de interesse genuíno.

**`prospecting_tactics.md`** — Operadores de busca, mineração de sites de empresas,
eventos-gatilho, caminhos de indicação. Encontrar pessoas sem pagar por um banco de dados.

**`account_navigation.md`** — Empresas versus contatos, regras de multithreading, em qual
porta bater primeiro quando uma empresa tem várias.

**`linkedin_outreach.md`** — Sequências de conexão e limites de taxa, abrindo com a seção
de risco com que deveria abrir: automatizar o LinkedIn viola os ToS deles, nunca use uma
identidade falsa, e se alguém perguntar se isto é automatizado, diga que sim na hora.

**Geradas para o seu produto por `sellbird train <url>`:**

- **`product_knowledge.md`** — o que você vende, os benefícios, preços, casos de uso, a dor
  que você resolve, gatilhos de compra
- **`competitive_intel.md`** — battle cards por concorrente, ângulos de diferenciação,
  caminhos de migração

*(Ambos são gitignored. Seu posicionamento e preços não deveriam cair em um repositório
público por acidente.)*

### Qual agente recebe o quê

Definido em `sellbird/brain.py` — edite o mapa para mudar isso.

| Skill | Scout | Writer | Handler | Sender | LinkedIn |
|---|:-:|:-:|:-:|:-:|:-:|
| `prospecting_tactics` | ● | | | | ● |
| `lead_qualification` | ● | | | | |
| `account_navigation` | ● | | | | |
| `signal_playbook` | ● | ● | | | |
| `email_frameworks` | | ● | | ● | |
| `sales_methodology` | | ● | ● | | |
| `offer_strategy` | | ● | ● | | |
| `objection_handling` | | | ● | | |
| `linkedin_outreach` | | | | | ● |
| `product_knowledge` | ● | ● | ● | ● | ● |
| `competitive_intel` | | ● | ● | | |

Adicionando uma skill: escreva o arquivo, adicione o nome dele a `skill_map` em
`sellbird/brain.py`. Esse é todo o processo.

---

## Os sub-agentes

O Sellbird parece um agente só. Por baixo são cinco, cada um carregado com skills
diferentes.

| Agente | O que ele faz |
|---|---|
| **Scout** | Pontua e personaliza o que os coletores encontraram. O Python faz a busca e a resolução de e-mails; o modelo selecionado é usado só onde julgamento é realmente necessário — e é isso que mantém o custo em tokens sadio. |
| **Writer** | Gera sequências de 3 e-mails. E-mail 1 com menos de 75 palavras, e-mail 2 com menos de 75, e-mail 3 com menos de 40. Lista de banimento rígida contra linguagem que soa a IA. |
| **Sender** | Renderiza variáveis de merge por prospect e coloca cada e-mail na caixa de saída com um horário de envio. Esvazia os itens vencidos e aprovados com ritmo humano, respeitando o teto diário e a parada por resposta: uma resposta de qualquer pessoa de uma empresa para a sequência para todos ali. |
| **Handler** | Consulta respostas, remove duplicatas, classifica a intenção, avança o estágio da conversa e enfileira respostas pela mesma escada de aprovação. Detecta bounces, marca o endereço como inválido, cancela os envios enfileirados daquele prospect e aciona um kill switch global acima de um limite de taxa de bounce. |
| **Analyst** | Roda em ciclos ociosos. Estatísticas do pipeline, desempenho de campanhas, distribuição de intenção, o que realmente está funcionando. |

Estágios de conversa: `initial_outreach → engaged → qualifying → presenting → negotiating → closing → closed_won / closed_lost`
