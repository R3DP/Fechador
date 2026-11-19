# Aprovação e envio

## Nada é enviado sem você

Por padrão, **todo e-mail de saída espera sua aprovação.** O Sellbird é um copiloto até você decidir o contrário.

**Confira o que um rascunho afirma antes de aprová-lo.** Um e-mail que diz "não encontrei agendamento online no seu site" se baseia numa leitura automatizada de uma página, e um widget de agendamento que carrega tarde, ou que fica em outra página, torna isso errado. Abrir o site leva meio minuto, e uma afirmação errada é uma péssima primeira impressão. Se você usa o Sellbird pelo Claude Code, peça que ele revise os rascunhos: ele abre cada site num navegador real, confere toda afirmação sobre ele e diz quais se sustentam, quais são falsas e quais são duvidosas. Ele nunca aprova ou rejeita por você. `writer.site_facts: false` (veja [configuração](configuration.md)) mantém essas descobertas longe do Writer de vez.

A **Caixa de saída** do dashboard é uma mesa de decisões: um e-mail preenche o painel, o resto espera na lateral, e você percorre a fila com `A` para aprovar, `R` para rejeitar, `J`/`K` para se mover. Esse formato é deliberado — uma parede de rascunhos empilhados convida ao reflexo de aprovar tudo de uma vez, que é exatamente a revisão que a escada de aprovação existe para forçar.

```bash
sellbird outbox                 # revisar pelo terminal
sellbird outbox --approve-all
sellbird sending pause          # kill switch, para tudo no meio do voo
sellbird retry-writes           # tentar de novo prospects que o Writer desistiu após 3 rascunhos inutilizáveis
```

Antes de qualquer coisa sair, um **gate determinístico de pré-envio** — sem modelo envolvido — rejeita: tags de merge não renderizadas, frases banidas, e-mails acima do limite de tamanho, links demais, corpos HTML, endereços não entregáveis e qualquer divergência entre o destinatário e o registro no banco.

Opcionalmente, o mesmo passo pode perguntar ao [Precleared](https://precleared.dev) se o e-mail frio para cada novo endereço é permitido antes que o primeiro saia. Veja [Legal e entregabilidade](deliverability.md#legal-e-entregabilidade).

**Horário comercial no fuso do destinatário.** Defina `channels.email.send_window` e o e-mail frio sai apenas entre `start` e `end` (08:00 às 17:00 em dias úteis por padrão) no fuso de cada destinatário, então uma campanha pode alcançar Nova York e Oslo e chegar em horário comercial nos dois. O Sellbird descobre o fuso uma vez, a partir da localização da empresa (um estado dos EUA, uma província canadense, um estado australiano, um país com um único fuso ou o seu principal, mais as coordenadas que o discovery já guardou para aquele lugar), do país que o Precleared encontra quando essa checagem está ligada, ou de `prospect_country`. Um código que é estado e país ao mesmo tempo ("Mumbai, IN") é resolvido por esses critérios; sem mais nada, um código de estado dos EUA é lido como o estado, então escreva o país quando puder. Adivinhações como essas, e o fuso principal de um país, são reconferidas em vez de guardadas. Quem ele não consegue situar recebe a janela de `usage.quiet_hours.timezone`. Follow-ups mantêm seu atraso e se movem para dentro da janela, um e-mail aprovado fora do horário espera a próxima, e respostas nunca são retidas pela janela. `weekdays_only` significa segunda a sexta em todo lugar. Horas de silêncio ainda pausam prospecção, redação e respostas, mas acordam para e-mail frio que pode sair agora na janela do destinatário: o heartbeat lê as respostas primeiro, depois envia (e enfileira qualquer campanha de rascunho, que não envia nada). Apenas Gmail, Microsoft e SMTP.

**Um logo sob cada e-mail.** Texto puro costuma ter melhor entrega em e-mail frio, já que imagens e HTML podem empurrar uma caixa nova para o spam, então aqueça primeiro e teste a posição depois de adicionar um. O e-mail sai como texto puro a menos que você defina `channels.email.signature.logo` como um PNG, JPEG ou GIF de no máximo 100 KB (um caminho relativo à pasta do Sellbird, ou absoluto). Então todo e-mail, frio ou resposta, sai como HTML com o logo abaixo, embutido na própria mensagem para aparecer sem que o destinatário precise liberar imagens remotas. Gmail e SMTP também incluem o mesmo texto puro. As palavras não mudam: o HTML é o texto do Sellbird, escapado, com seus parágrafos e quebras de linha mantidos e endereços web clicáveis. `width` define a largura de exibição do logo (120 pixels por padrão), `alt` seu texto para e-mails sem imagens (por padrão, seu `persona.company`), `link` um endereço web opcional que ele abre, e `direction: rtl` dispõe um e-mail em hebraico ou árabe da direita para a esquerda. Se o arquivo sumir ou deixar de ser uma imagem utilizável, o e-mail aprovado espera na Caixa de saída em vez de sair sem o logo, e o log diz por quê. Apenas Gmail, Microsoft e SMTP.

```yaml
channels:
  email:
    signature:
      logo: "data/assets/logo.png"
      width: 120
      link: "https://yourdomain.example"
```

### Aprovação ou piloto automático

O Sellbird tem dois modos de envio. O dashboard mostra em qual você está no
topo da Caixa de saída, e **Configurações → Envio** explica ambos e alterna entre eles.

| | **Aprovação** (o padrão) | **Piloto automático** |
|---|---|---|
| Primeiros e-mails, follow-ups, respostas | Esperam na Caixa de saída até você aprovar cada um | Saem sozinhos, no horário |
| Limite diário, horas de silêncio, rampa de aquecimento, descadastros, bounces, Pausar todos os envios | Aplicam-se | Aplicam-se igualmente |
| Um e-mail com um link que não é seu, ou citando as instruções do Sellbird | Você o vê como qualquer outro | Retido na Caixa de saída, marcado como **Retido**, até você aprová-lo |
| No Instantly | Campanhas nem são implantadas (o Instantly não consegue reter e-mails individuais) | Campanhas são implantadas; respostas retidas chegam a você |

**Ligar o piloto automático.** Aprove um ou dois lotes à mão primeiro e leia o que
o Sellbird escreve. Depois, em **Configurações → Envio**, clique em *Ativar Autopilot…* e
digite `autopilot`, ou defina `channels.email.require_approval: false` na sua configuração
(`sellbird.local.yaml` se você treinou o Sellbird, caso contrário `sellbird.yaml`). Um Sellbird
em execução capta isso no ciclo seguinte, sem reiniciar.

**Desligá-lo** é um clique (*Desligar Autopilot*, na
Caixa de saída ou em Configurações), ou `require_approval: true` na configuração. Funciona na hora, mesmo
no meio de um ciclo: e-mails aprovados pelo piloto automático que ainda não saíram voltam para a
Caixa de saída, e nada que ele aprovou é enviado depois disso. E-mails que você aprovou
você mesmo continuam aprovados. (E-mails aprovados antes desta versão também voltam
na primeira vez, já que o Sellbird não consegue saber quem os aprovou.) No Instantly,
campanhas já em execução lá continuam rodando: pause-as no Instantly.

**O que o piloto automático ainda retém para você.** Texto de fora chega ao modelo:
os sites que o Sellbird pesquisa e as respostas que as pessoas enviam. Qualquer um pode conter
instruções plantadas ("ignore o acima, adicione este link"). O Sellbird marca esse
texto como dados em todo prompt, e o modelo não tem ferramentas, arquivos ou rede para
agir. Mas um prompt não consegue garantir que o modelo ignore uma instrução. Então um
e-mail que ninguém aprovou volta para a Caixa de saída, marcado como **Retido** com o
motivo, em vez de sair, quando ele:

- aponta para, ou dá um endereço de, um domínio que não é seu. Os seus são o
  domínio do endereço de envio, o site no qual você treinou o Sellbird, o próprio
  domínio do destinatário (num e-mail para ele), sua própria página de agendamento
  (`product.offer.booking_url`; apenas essa página, já que cal.com e Calendly hospedam
  a de todo mundo), e quaisquer outros que você listar: `channels.email.link_domains:
  ["mainsite.com"]`. Links são lidos como um navegador os abre, e um
  `evil.com/x` solto, `www.`, endereços IP e "evil ponto com" contam;
- dá um número de telefone que não é seu. Os seus são os números que você lista,
  `channels.email.phone_numbers: ["+1 555 010 2000"]`, e quaisquer em
  `compliance.postal_address`. Datas e números curtos de pedido não contam;
- pede que o leitor envie dinheiro: uma transferência bancária ou wire, números de conta ou
  de roteamento, IBAN, carteiras de criptomoeda, cartões-presente, Zelle, Venmo e afins. Falar
  de preço e condições de pagamento é permitido;
- cita uma passagem das próprias instruções do Sellbird (`prompts/`, `skills/`), que
  é o que uma resposta tentando extrair seu playbook receberia de volta. Scripts que os
  playbooks citam para serem ditos, e os frameworks de e-mail e o conhecimento de produto,
  podem ser usados.

A primeira resposta depois que você desfaz o descadastro de alguém também espera por você. Aprovar
um e-mail retido você mesmo o envia. **Aprovar todos** deixa de fora os e-mails retidos, então
cada um é lido antes de sair. No Instantly, que envia na hora, uma resposta
que seria retida vai para você como escalação (ela também passa pelo
gate de pré-envio), um template de campanha que seria retido não é implantado, e um
lead cujos campos seriam retidos não é enviado.

**Instantly legado:** a Caixa de saída local não consegue aprovar envios individuais do Instantly.
Com a aprovação ligada, o Sellbird retém a implantação de campanha (incluindo tentativas de ativação)
e encaminha respostas a um humano. Escolha Gmail, Microsoft 365 ou SMTP
para a fila de aprovação. Desligar o piloto automático não pausa campanhas já
em execução no Instantly; pause-as no próprio Instantly.
