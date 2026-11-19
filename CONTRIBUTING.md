# Como contribuir com o Sellbird

Para quem altera este repositório e abre pull requests e, sobretudo,
para agentes de código (Claude Code, Codex, Cursor, Aider). O `CLAUDE.md` é diferente:
ele orienta quem está *usando* o Sellbird. Este arquivo trata de contribuir com ele.

## Nada de dados de contato reais, em nenhum lugar em que sejam publicados

Este repositório é público. O trabalho do Sellbird é encontrar pessoas reais em empresas
reais, então testá-lo revela nomes, endereços e telefones reais. Esses dados ficam na
sua máquina. Um pull request já listou os endereços de trabalho de treze pessoas reais,
com seus nomes e empregadores, na descrição e nas fixtures de teste, e limpar isso
exigiu reescrever a branch.

**Nunca coloque nada disto em um commit, teste, fixture, comentário, docstring,
documento, entrada de changelog, mensagem de commit, título de PR, descrição de PR,
comentário de PR, revisão ou issue:**

- o nome, e-mail, telefone ou endereço de rua de uma pessoa real;
- uma empresa real encontrada durante os testes: nome, domínio, URL do site ou
  localização, inclusive dentro de HTML copiado do site dela;
- qualquer coisa tirada de `data/sellbird.db`, de uma exportação de usuário, de um item
  do Outbox, de uma resposta ou de uma execução de teste ao vivo.

**Faça assim em vez disso:**

- Escreva as fixtures à mão com empresas e pessoas fictícias. Use os nomes
  reservados onde o código os aceita: `example.com`, `example.net`,
  `example.org` e os domínios de topo `.example`, `.test` e `.invalid`.
  Placeholders no estilo `acme.com` servem. Pessoas inventadas ganham nomes
  inventados genéricos.
- Quando um teste precisa de marcação que quebrou em um site real, reconstrua a estrutura
  que quebrou (um `<br>` dentro de um span, o formato de uma frase, um bloco schema.org)
  com conteúdo fictício. Não recorte uma cópia da página real.
- Relate verificações ao vivo apenas como contagens e tipos: "encontrei o
  decisor em 17 de 19 sites de pequenas empresas (telhados, dentistas, escritórios de
  advocacia)". Não uma tabela por site, não os endereços encontrados, não os domínios
  testados. Mantenha os resultados detalhados no seu diretório de rascunho local.
- Fornecedores e infraestrutura podem ser nomeados, porque não são contatos:
  Google, Cloudflare, Hunter, Instantly, DataForSEO, Greenhouse e assim por diante.
  Empresas nomeadas só por fatos públicos de produto (cujo formato de job board foi
  testado) também podem. Os funcionários delas não.

**Antes de dar push ou abrir um PR**, confira o diff e a descrição que você vai
publicar em busca de endereços:

```bash
git diff origin/main | grep '^+' | grep -oE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}' | sort -u
```

Todo resultado deve ser um placeholder. Se um não for, corrija antes do push. Depois que
algo é enviado a um repositório público, apagá-lo depois não o remove:
commits antigos continuam acessíveis pelo hash e as descrições de PR mantêm um histórico
de edições.

## E-mail de teste e de verificação

Todo e-mail de teste ou de verificação vai para um endereço que é seu, criado para
esse propósito. Nunca para um endereço de um banco de dados, de uma exportação, de uma
resposta ou de uma fixture. Os testes nunca enviam e-mail real: use os provedores
falsos em `tests/`.

## Lançamentos (mantenedores)

Toda nota de versão no GitHub começa com esta linha, para quem acompanha as versões saber onde vão os anúncios:

```markdown
> **Siga [@sellbirdagent](https://x.com/sellbirdagent) no X** para novidades de versões, funcionalidades e o roadmap.
```

Anuncie a versão no X primeiro e depois vincule essa publicação nas notas de versão.

## Licença e sign-off

O Sellbird é licenciado sob a GNU Affero General Public License v3.0 apenas
(veja `LICENSE`). Código das versões do Harvey licenciadas em MIT (0.3.x e
anteriores) mantém seu aviso MIT em `NOTICE`.

Ao contribuir, você concorda que sua contribuição é licenciada sob a
licença do projeto. Assine todo commit para atestar que você o escreveu ou tem
o direito de enviá-lo, sob o
[Developer Certificate of Origin](https://developercertificate.org/):

```sh
git commit -s -m "Descreva a mudança"
```

Isso adiciona uma linha `Signed-off-by: Seu Nome <voce@example.com>`. Use o nome e o
e-mail com que você faz commit; um endereço noreply do GitHub serve.
