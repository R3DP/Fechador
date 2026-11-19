# Estratégia de oferta e mecânica de fechamento

## Regra central: Conquiste o direito de pedir

Nunca lidere com uma oferta. Nunca faça pitch em um cold email. O primeiro
contato existe para começar uma conversa, não para fechar um negócio.

Ofertas só são apresentadas depois que um prospect mostrou interesse genuíno:
- Respondeu positivamente
- Fez uma pergunta sobre o produto
- Expressou uma dor que você consegue resolver
- Perguntou sobre preço ou próximos passos

Se nenhuma dessas coisas aconteceu, você ainda está na fase de "conquistar
atenção". Fique lá.

## A escada de ofertas

Nem todo prospect interessado recebe a mesma oferta. Case a oferta com o nível
de engajamento dele:

| Nível de engajamento | Sinal | Oferta |
|----------------------|-------|--------|
| **Curioso** | Fez uma pergunta, clicou num link | Responda a pergunta + CTA suave ("Happy to walk you through it if useful") |
| **Interessado** | Expressou uma dor, perguntou sobre recursos | Compartilhe um recurso ou case relevante + sugira uma call rápida |
| **Pronto** | Perguntou sobre preço, prazo ou próximos passos | Apresente a oferta específica com próximo passo claro |
| **Urgente** | Tem prazo, perdeu o fornecedor atual, está contratando | Vá rápido — apresente a oferta já, com tom de urgência |

## Construindo ofertas a partir do conhecimento do produto

Quando o Sellbird aprende sobre um produto (via crawl do site ou treino
manual), ele identifica:

1. **Oferta principal**: O que estamos vendendo, afinal? (p. ex. assinatura de software, contrato de serviço, auditoria/avaliação)
2. **Ofertas de entrada**: Formas de começar com menos compromisso (p. ex. trial grátis, piloto, auditoria grátis, sessão de estratégia)
3. **Ofertas de prova**: Formas de demonstrar valor antes de pedir dinheiro (p. ex. relatório de amostra, avaliação grátis, calculadora de ROI)

### Framework de construção de oferta

Para cada produto, determine:
- **O que recebem**: Entregável ou acesso específico (nada de "valor" vago)
- **Quanto custa**: Preço, compromisso de tempo ou "grátis"
- **O que arriscam**: Nada (trial grátis), garantia de devolução do dinheiro ou mês a mês
- **O que acontece depois**: A mecânica exata — clicar num link, responder com horários, preencher um formulário

### Exemplos de estrutura de oferta

**Produto SaaS:**
- Entrada: "We have a 14-day free trial — no credit card needed. Want me to set one up for you?"
- Principal: "Plans start at $X/mo. Want me to walk you through which tier makes sense for your team?"

**Serviço/Agência:**
- Entrada: "We usually start with a free 30-minute audit of your current setup. Worth doing?"
- Principal: "Our typical engagement starts at $X/mo. I can put together a custom scope if you share more about what you're working with."

**Consultoria:**
- Entrada: "I put together a quick analysis of [their specific situation]. Want me to send it over?"
- Principal: "We do this as a [fixed/retainer] engagement. Want to jump on a 20-minute call to see if it makes sense?"

## Mecânica de fechamento: como agendar

A forma como você pede o próximo passo importa. Sempre confirme com o usuário
qual mecânica usar:

### Opção 1: Link de agenda
Melhor quando: Alto volume, sensação self-service, o usuário tem ferramenta de agendamento.
```
"Here's my calendar if you want to grab 15 minutes: [LINK]"
```
- Use quando a configuração do produto inclui um `booking_url`
- Sempre especifique o compromisso de tempo ("15 minutes", "quick 20-min call")
- Nunca diga "book a demo" — diga "grab time" ou "jump on a call"

### Opção 2: Sugerir horários específicos
Melhor quando: Sensação mais pessoal, venda de maior toque, sem ferramenta de agenda.
```
"Would Thursday at 2pm or Friday morning work for a quick call?"
```
- Ofereça exatamente 2 ou 3 opções
- Sempre inclua dia + hora
- Mantenha a janela estreita (mesma semana)

### Opção 3: Perguntar a preferência deles
Melhor quando: Prospects enterprise, respeito à agenda deles, decisores sênior.
```
"What does your calendar look like this week for a quick 15 minutes?"
```
- Respeitoso mas ainda com limite de tempo
- Bom para C-suite, onde você não quer parecer presunçoso

### Opção 4: Próximo passo sem call
Melhor quando: O produto se vende sozinho, o prospect só precisa de acesso.
```
"Want me to set up a trial account for you? Takes 2 minutes."
```
- Para produtos self-service com trial grátis
- Pule a call se o produto consegue falar por si

## O que o Sellbird deve confirmar com o usuário

Durante o setup ou o treino, o Sellbird precisa saber:

1. **Qual é a oferta principal?** (assinatura, serviço, trial, auditoria etc.)
2. **Existe oferta de entrada?** (trial grátis, auditoria grátis, amostra etc.)
3. **Qual é o objetivo da abordagem?** (agendar uma call, iniciar um trial, conseguir uma resposta etc.)
4. **Como as reuniões devem ser agendadas?**
   - Link de agenda (informe a URL)
   - Sugerir horários
   - Perguntar a preferência deles
5. **Quem faz a reunião?** (o usuário, alguém do time de vendas, o Sellbird agenda e outra pessoa aparece)
6. **Alguma qualificação antes de agendar?** (porte da empresa, orçamento, necessidade específica)

Essas respostas vão para `sellbird.yaml` sob a configuração do produto e guiam
como o Sellbird escreve e-mails e trata respostas.

## Timing da oferta na sequência

### Sequência de cold email (3 e-mails)
- **E-mail 1**: Sem oferta. Comece uma conversa. Faça uma pergunta. Compartilhe um insight.
- **E-mail 2**: Menção suave só se fizer sentido. "We help teams like yours [do thing]. Worth a conversation?"
- **E-mail 3**: E-mail de encerramento. Um pouco mais direto mas ainda sem pitch duro. "If this isn't a priority right now, no worries. But if [pain point] comes up, I'm here."

### Tratamento de resposta (depois do interesse)
- **Primeira resposta interessada**: Reconheça, responda a pergunta e então apresente a oferta de entrada ou sugira uma call.
- **Follow-up depois do interesse**: Se a pessoa sumiu depois de mostrar interesse, um empurrãozinho gentil. Nunca mais de um.
- **Pronto para agendar**: Apresente a mecânica de fechamento específica. Seja direto. "Let's get something on the calendar."

## Regras de linguagem

**Diga:**
- "Worth a quick conversation?"
- "Happy to walk you through it"
- "Would it make sense to grab 15 minutes?"
- "Want me to send over [specific thing]?"

**Nunca diga:**
- "Book a demo" (soa como pitch de vendas)
- "Schedule a call with our team" (impessoal)
- "I'd love to show you" (enquadramento egocêntrico)
- "Let me know if you're interested" (passivo, sem próximo passo claro)
- "When are you free?" (aberto demais)

## Lidando com "Quanto custa?"

Quando um prospect pergunta sobre preço antes de você qualificá-lo:

1. Dê uma resposta real — nunca fuja da pergunta
2. Enquadre com contexto: "Plans start at $X/mo, depending on [variable]. Most teams your size are on the [tier] plan."
3. Faça a transição para a qualificação: "To give you an exact number, it'd help to know [specific question about their needs]."
4. Se existe oferta de entrada grátis, lidere com ela: "There's a free trial so you can see if it fits before committing to anything."
