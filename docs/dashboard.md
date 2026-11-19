# O dashboard e os dados

## O dashboard

```bash
sellbird dashboard     # exibe o link para abrir, ex.: http://127.0.0.1:5555/#token=…
```

**Abrindo.** O painel pode mudar suas configurações de e-mail, aprovar a caixa de saída
e iniciar o Sellbird, então ele é trancado para você, não apenas para a sua máquina. Na
primeira inicialização ele cria um token aleatório em `data/dashboard-token` (legível só
por você) e imprime um link que o carrega depois do `#`. Abra esse link: a página mantém o
token apenas para aquela aba do navegador e o remove da barra de endereço. Uma nova aba, ou
uma aba aberta sem o link, mostra uma tela bloqueada; cole o token ali, ou rode
`sellbird dashboard --url` para imprimir o link de novo. Toda requisição à API precisa do
token como cabeçalho `Authorization: Bearer` — scripts e `curl` inclusive — e o token
nunca é aceito por cookie ou string de consulta. Apague `data/dashboard-token` e reinicie
o dashboard para substituí-lo.

> Os rótulos e nomes de grupo abaixo são os da interface em português do Brasil. As
> capturas de tela são da interface original em inglês e ainda não foram refeitas; o
> layout e os dados são os mesmos.

**Ele só escuta nesta máquina.** `--host` aceita apenas endereços loopback (`127.0.0.1`,
`::1`, `localhost`), e as requisições precisam nomear um deles no cabeçalho `Host`, o que
também impede que um nome DNS apontado para 127.0.0.1 o alcance. Requisições enviadas por
outros sites abertos no seu navegador são recusadas. Para usá-lo de outro computador,
faça um túnel em vez de expor: `ssh -L 5555:127.0.0.1:5555 your-machine`, e então abra o
link impresso localmente. O token protege contra outros usuários e outros sites, não
contra programas que já rodam com a sua própria conta de usuário, que podem ler o arquivo
de token assim como podem ler o `.env` ou o banco de dados.

**Windows:** o arquivo de token é protegido pelas permissões da pasta em que fica (seu
perfil de usuário normalmente restringe isso a você); o Sellbird não aplica modos de
arquivo POSIX ali.

HTML, CSS e JavaScript simples servidos de `sellbird/web/`. Sem etapa de build, sem
framework, sem bundler — edite `app.css` e recarregue. As fontes vêm junto, então ele
renderiza corretamente mesmo com a rede desligada.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="screenshots/today-dark.png">
  <img alt="A tela Hoje: quatro números de destaque com tendências de 14 dias, a lista de coisas esperando por você, contatos por estágio e execuções de coleta" src="screenshots/today-light.png">
</picture>

A barra lateral é agrupada pelo que você está fazendo: **Trabalho** (o que precisa de você),
**Funil** (o que o Sellbird está construindo) e **Sistema** (como ele está rodando).
Contagens ao lado de uma aba significam que há algo esperando ali.

**Trabalho**
- **Hoje** — quatro números de destaque com tendências de 14 dias (contatos encontrados,
  e-mails enviados, conversas, esperando por você), depois tudo que precisa de uma
  decisão, contatos por estágio, execuções de coletores e o que o pipeline está fazendo
  agora mesmo. A configuração aparece aqui até terminar, depois desaparece.
- **Sua empresa** — o que você vende, para quem vende, a oferta com que todo primeiro
  e-mail termina e de quem ele sai. Tudo o que o Sellbird usa para escrever.
- **Caixa de saída** — a mesa de decisões. Cada e-mail fica ao lado do que o Sellbird sabia
  quando o escreveu: a empresa, como o endereço foi encontrado e verificado, e os sinais
  em que o e-mail se baseia. `J`/`K` para navegar, `A` aprovar, `E` editar, `R` rejeitar.
- **Caixas de entrada** — os endereços de e-mail de onde o Sellbird envia. Mais caixas
  significam mais e-mails frios por dia; respostas ficam na caixa que iniciou a conversa.
- **Conversas** — cada resposta no contexto dos e-mails que levaram a ela. Conversas que
  o Sellbird passou para você (um pedido de contrato, uma resposta para a qual não tinha
  resposta segura) vêm primeiro, com **Devolver ao Sellbird**, **Fechar** e **Reabrir**.

**Funil**
- **Sinais** — o portão de confirmação e o construtor de coortes
- **Descobrir** — o menu de provedores com preços lado a lado, uma estimativa e então uma
  execução; e ainda a leitura dos sites de empresas encontradas mas ainda não vistas
- **Empresas / Contatos** — tudo que foi encontrado, pesquisável, com exportação CSV. As
  empresas são ordenadas por uma pontuação de aderência de 0 a 100 e mostram seu status
  (e-mail enviado, rascunho esperando, ou por que não foi contatada); clique em uma para
  ver o card de detalhes, ou exporte o registro completo de empresas
- **Campanhas** — cada sequência que o Sellbird escreveu, para quem vai, e feedback por
  campanha para o writer

**Sistema**
- **Atividade**, **Uso**, **Controles**, **Configurações**, **Ajuda**. **Uso** mostra os medidores
  de cota do Claude ou Codex e as contagens de tokens por agente, sem valores em dólar:
  você está numa assinatura e não é cobrado por token, então mostrar custos seria inventado.

| Caixa de saída | Conversas |
|---|---|
| <picture><source media="(prefers-color-scheme: dark)" srcset="screenshots/outbox-dark.png"><img alt="A mesa de decisões da Caixa de saída: uma resposta redigida a uma objeção, com a empresa, o contato, a verificação e os sinais ao lado" src="screenshots/outbox-light.png"></picture> | <picture><source media="(prefers-color-scheme: dark)" srcset="screenshots/conversations-dark.png"><img alt="Uma conversa que precisa de você: os dois e-mails que o Sellbird enviou e a resposta do prospect, marcados como Objeção e Precisa de você" src="screenshots/conversations-light.png"></picture> |

A cor é mantida para significado. A moldura é neutra e um único azul marca aquilo sobre o
que você pode agir. Status (esperando por você, concluído, falhou, rodando) usa o mesmo
conjunto pequeno de tons em toda aba, então "esperando por você" parece igual onde quer
que apareça. Os números são tabulares, então as colunas se alinham e um número mudando
não desloca o layout.

A aparência tem três estados: **Seguir o seu computador** (`auto`) segue o sistema
operacional e é o padrão, ou escolha **Claro** ou **Escuro** pelo botão no fim da barra
lateral. O modo escuro usa o mesmo layout com um conjunto diferente de tokens de cor.

---

## Como os dados são armazenados

SQLite em `data/sellbird.db`. Uma ideia conduz o schema:

> **Todo fato é uma linha, nunca uma coluna.**

Não `companies.has_agency`. Não `companies.rank`. Uma linha em `observations`:

```
observations(company_id, prospect_id, collector, signal_code,
             value_num, value_text, confidence, evidence_url, observed_at, run_id)
```

Quatro coisas decorrem disso, nenhuma das quais você obtém com colunas:

1. **Um novo sinal não precisa de migração.** Um coletor inventa um código e funciona.
2. **O histórico é de graça.** O mesmo sinal observado trimestralmente *é* uma série
   temporal — e "eles largaram a agência no trimestre passado" é um gatilho muito melhor
   que qualquer fato estático.
3. **Confiança e procedência viajam com o fato** em vez de se perderem na sobrescrita.
   *"Achamos que a agência deles é X, confiança 0,9, aqui está a URL."*
4. **Uma coorte é uma consulta.** A interseção de conjuntos acontece no SQL, não em código
   de aplicação sobre uma busca limitada.

O vocabulário é governado: um trigger do banco rejeita qualquer `signal_code` que não
esteja na tabela `signal_codes`, então um erro de digitação falha alto em vez de inventar
um sinal lixo em silêncio.

Outras tabelas: `companies`, `prospects`, `campaigns`, `conversations`, `outbox`,
`actions`, `runs`, `usage_events`, `email_patterns`, `settings`, `feedback`.
