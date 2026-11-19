# Rodando o Sellbird com Docker (Linux)

O Docker Compose roda o dashboard; inicie e pare o heartbeat pelo card de Ações
(Actions). A rede do host preserva a vinculação somente-loopback do dashboard em
`127.0.0.1:5555`. Esta configuração do Compose suporta Linux nativo; use a instalação
via pip acima no macOS ou Windows. Em um host Linux remoto, acesse o dashboard por um
túnel SSH em vez de expor sua porta à rede.

```bash
git clone https://github.com/ethanplusai/sellbird.git
cd sellbird

# Create the credentials file only if you do not already have one.
test -e .env || cp .env.example .env

# Run as your Linux user, never root. Set these again when rebuilding.
export SELLBIRD_UID=$(id -u) SELLBIRD_GID=$(id -g)

# Sign in to Claude on the host first; ~/.claude must already exist.
# The image ships Claude only; Codex is not included.
docker compose build
docker compose run --rm sellbird setup

docker compose up -d
docker compose logs sellbird
# Open the private unlock link printed in the logs.
```

O Compose monta o diretório do checkout em `/app`. Credenciais de configuração, os dois
arquivos YAML de configuração, a saída do treinamento, os arquivos de conhecimento e
`data/` permanecem nesse checkout quando os contêineres são recriados. A montagem de
diretório também permite gravações atômicas de configuração; não a substitua por
montagens de arquivos de configuração individuais.
O Sellbird carrega o `.env` diretamente. Reinicie o contêiner após editar as credenciais.
O checkout e o diretório de autenticação do Claude precisam ser graváveis pelo usuário
selecionado.

Para treinar depois, use `docker compose run --rm sellbird train <product-url>`;
o `sellbird.local.yaml` é salvo direto no checkout. Faça backup deste arquivo, do `.env`,
de `skills/` e de `data/` antes de mover instalações. O código em execução também vem
do checkout: reinicie após atualizá-lo e reconstrua quando as dependências ou o
Dockerfile mudarem. O contexto de build exclui dados locais e credenciais.

O dashboard escuta na 5555. Se você mudar a porta no `command` do Compose,
mude também a porta do health-check do Dockerfile e reconstrua. Pare o serviço com
`docker compose down`; os arquivos permanecem no checkout. Use uma instalação no host se
precisar do provedor Codex.
