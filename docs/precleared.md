# A checagem de e-mail frio (Precleared)

Antes do primeiro e-mail frio para qualquer pessoa nova, o Sellbird pode perguntar ao
[Precleared](https://precleared.dev) se o e-mail frio pode ir para aquele
endereço. A resposta depende de fatos que o endereço não mostra: um autônomo
(sole trader) do Reino Unido precisa de consentimento onde uma sociedade limitada não
precisa. O Precleared os consulta ao vivo (Companies House, o domínio, o site) e aplica as regras
do país do destinatário: Reino Unido, EUA, Canadá, Alemanha, França, Austrália,
Irlanda, Holanda, Espanha, Itália, Letônia, Emirados Árabes Unidos, Egito e Catar. O
remetente também pode estar em qualquer um desses catorze países.

Desligado por padrão. Uma checagem por endereço, para e-mail enviado pelo Gmail,
Microsoft 365 ou SMTP. Campanhas do Instantly e respostas nunca são checadas.

## Como ligar

No `sellbird.yaml`, ou no `sellbird.local.yaml` se você treinou o Sellbird (esse arquivo
ganha):

```yaml
compliance:
  precleared:
    enabled: true
    sender_country: "GB"        # GB, US, CA, DE, FR, AU, IE, NL, ES, IT, LV, AE, EG or QA
    address_source: "unknown"   # unless copied from the businesses' own sites
    prospect_country: ""        # e.g. "US" if all prospects are in one country
```

Coloque `prospect_country` entre aspas (o YAML lê um `NO` sem aspas como falso).
`sellbird setup` faz as mesmas perguntas.

## O que é enviado

Uma requisição por novo endereço: o endereço, `sender_country`,
`address_source`, `existing_customer: false`, os primeiros 200 caracteres de
`product.description`, e o país do destinatário, de uma de duas formas:

- **`recipient_country`**, quando o Sellbird tem certeza dele. É um país
  nomeado na localização da empresa ("Oslo, Norway", "London, UK"), um estado dos EUA,
  província canadense ou estado australiano nomeado ali ("Austin, TX",
  "Toronto, ON"), ou um código que é estado e país ao mesmo tempo ("Berlin, DE")
  depois que as coordenadas que o discovery guardou para aquele lugar o resolvem. O Precleared
  o toma como definitivo, então uma leitura da qual o Sellbird não tem certeza nunca é enviada: esse
  mesmo código sem coordenadas (Delaware por convenção), uma cidade sozinha,
  ou coordenadas sozinhas. Um fuso horário guardado por si só nunca estabelece o
  país, porque pode vir de dados de localização aproximados ou desatualizados.
  Coordenadas distantes das duas leituras de um código ambíguo não o resolvem.
- **`default_recipient_country`**, caso contrário, se houver um:
  `prospect_country`, ou o único país em que toda entrada de `icp.geography` está
  com certeza ("Austin, TX" e "Denver, Colorado" dão `US`; "Denver, CO"
  sozinho não dá, já que `CO` também é o código da Colômbia, a menos que
  `icp.geo_coordinates` o tenha). O Precleared usa um padrão apenas quando suas próprias
  consultas não mostram país algum.

Nunca os dois.

Também, quando o Sellbird os tem, os nomes da empresa e da pessoa:

- **`company_name`**, o nome do registro da empresa, senão o próprio
  campo de empresa do prospect.
- **`recipient_name`**, o nome e sobrenome do prospect. Uma caixa da empresa
  (info@, hello@) não tem pessoa, então nenhum nome vai com ela.

Para um destinatário do Reino Unido, o Precleared busca no registro da Companies House pelo
nome da empresa quando o domínio sozinho não encontra a empresa, e confere
o nome da pessoa contra os diretores da empresa. Uma empresa encontrada assim
conta apenas quando outras evidências a ligam ao destinatário, como um diretor
com o nome da pessoa ou o site da própria empresa nomeando-a. Sem uma
empresa, um endereço do Reino Unido não pode ser distinguido de um autônomo, então a resposta é
`consent_needed`; os nomes transformam muitos deles numa empresa confirmada.
O Precleared não armazena o nome da pessoa. Ambos são cortados nos limites do Precleared (160 e 120 caracteres).

A chave vai como header bearer. Não são enviados: o assunto, o corpo, o
cargo da pessoa, nem a localização da empresa em si (apenas o país lido
dela).

## O que cada veredito faz

- **ok_to_email.** O e-mail é enviado. O id do recibo é registrado a cada envio
  (`precleared_receipt` no log de ações).
- **consent_needed, blocked.** O item da outbox é marcado como falho, com a
  regra, sua origem e o próximo passo como motivo. Seus follow-ups são
  cancelados, e um primeiro e-mail posterior para o mesmo endereço encontra o veredito
  em cache, sem uma segunda checagem.
- **unknown.** Um fato não pôde ser estabelecido, geralmente o país do
  destinatário, às vezes um registro que respondeu devagar demais. O e-mail é retido,
  não falho: a Caixa de saída mostra o que o resolveria (defina `prospect_country`
  se seus prospects estão todos num único país, ou dê à empresa uma localização
  ou seu número de registro) e o Sellbird pergunta de novo, após seis horas na primeira
  vez e depois após um dia. A terceira resposta unknown sobre os mesmos fatos
  falha o e-mail como `consent_needed` e `blocked` fazem; uma mudança naqueles
  fatos reinicia a contagem. Nada é guardado em cache para `unknown`, então um
  endereço reenfileirado é perguntado de novo.

## Quando a checagem está parada

Se o Precleared não consegue responder (checagens gratuitas esgotadas, chave sem
checagens ou rejeitada, ou não pode ser alcançado), novas checagens esperam um ciclo
posterior. Vereditos válidos em cache continuam valendo, usando os mesmos fatos de país do destinatário
que uma checagem nova. Respostas continuam saindo. Falhas específicas de um endereço adiam
aquele e-mail em seis horas; falhas em dois domínios distintos sem uma resposta nova
pausam novas checagens. A aba Hoje e `sellbird status` dizem quantos e-mails frios
estão esperando e o que resolve. A próxima checagem respondida limpa o
aviso, e desligar a checagem também.

## Chaves e limites

| Chave | Checagens por dia |
|---|---|
| Nenhuma | 10, compartilhadas por endereço IP público |
| Chave gratuita | 25 |
| Qualquer chave nova, seus primeiros 14 dias (contados da primeira checagem) | 100 |

Além disso, uma chave usa um pacote pré-pago, e o Sellbird mostra o link de pagamento
quando um acaba. `sellbird precleared-key` obtém uma chave gratuita para seu endereço de
e-mail e a salva em `.env` como `PRECLEARED_API_KEY` sem mostrá-la;
`sellbird setup` oferece o mesmo. O Precleared recebe esse endereço para criar a
chave. Você também pode obter uma em
[precleared.dev/get-key](https://precleared.dev/get-key) e adicioná-la você mesmo.

## Cache

Um veredito definitivo é mantido por 30 dias sob `precleared:<address>`, com uma
impressão digital do país do remetente, origem do endereço, descrição do produto, o
país enviado com ele (o do destinatário quando o Sellbird tinha certeza, senão o padrão
em uso) e os nomes enviados com ele. Mude qualquer um deles e o próximo e-mail
ganha uma checagem nova. Uma sequência de três passos custa uma checagem. Um endereço do qual o Sellbird
passa a ter certeza ganha uma checagem nova, a menos que o Precleared já tivesse
encontrado esse mesmo país por conta própria, caso em que o veredito em cache permanece. Quando
os nomes chegam pela primeira vez com um endereço cujo veredito foi guardado sem eles,
um `ok_to_email` permanece, já que os nomes só ajudam o Precleared a encontrar a
empresa, e qualquer outro recebe uma checagem nova com eles. O país que o
Precleared encontrou é mantido com o veredito e alimenta a janela de envio.

## Perguntas frequentes

**Funciona com o Instantly?** Não. O Instantly implanta campanhas inteiras, então
o Sellbird não consegue reter e-mails individuais lá.

**Por que recebo unknown?** Geralmente o país do destinatário não pôde ser descoberto,
e o Sellbird também não tinha certeza dele (veja "O que é enviado"). Se seus
prospects estão todos num único país, defina `prospect_country`; cada e-mail retido é
perguntado de novo na próxima tentativa (dentro de um dia) e sai se a resposta
for então `ok_to_email`.

**Por que tantos endereços do Reino Unido voltam consent_needed?** Muitas vezes o Precleared
não conseguiu encontrar a empresa por trás do domínio no registro, então não conseguiu
descartar um autônomo. O Sellbird envia os nomes da empresa e da pessoa para ajudar;
um registro de empresa com o nome real do negócio ajuda mais.

**Posso provar que uma checagem foi feita?** Cada envio registra o id do recibo, e
o Precleared pode mostrar o recibo assinado para aquele id depois.
