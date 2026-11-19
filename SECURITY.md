# Política de segurança

## Relatando uma vulnerabilidade

Não abra uma issue pública para um problema de segurança. Relate em particular
pelo GitHub: neste repositório, abra **Security → Report a vulnerability**
(Segurança → Relatar uma vulnerabilidade). Só os mantenedores veem o relato.

Inclua o que você encontrou, como reproduzir e o que um atacante poderia fazer
com isso. Use dados fictícios no relato, como em [CONTRIBUTING.md](CONTRIBUTING.md):
nunca os dados de contato de uma pessoa real nem nada de um banco de dados
real do Sellbird.

Vamos confirmar o recebimento do relato em alguns dias, manter você informado
enquanto trabalhamos em uma correção e dar o crédito a você nas notas de
versão, a menos que prefira o contrário.

## Versões com suporte

As correções de segurança entram na versão mais recente em `main`. O Sellbird é
atualizado com `git pull`, então confira se o problema ainda acontece ali.

## O que está no escopo

O Sellbird roda na sua própria máquina, com suas próprias credenciais. As
fronteiras mais importantes são:

- o token de login do dashboard e seu listener restrito ao loopback
  ([docs/dashboard.md](docs/dashboard.md));
- o isolamento das chamadas de modelo, que rodam sem ferramentas
  ([docs/how-it-works.md](docs/how-it-works.md));
- as travas da Caixa de saída que impedem que instruções plantadas em sites ou
  respostas enviem e-mails que ninguém aprovou ([docs/approval-and-sending.md](docs/approval-and-sending.md)).

Um problema que exige código já rodando com a sua própria conta de usuário está
fora do escopo: esse código consegue ler o `.env` e o banco de dados diretamente.

O serviço hospedado em [sellbird.ai](https://sellbird.ai) é um produto separado;
relate problemas nele da mesma forma e diga que é sobre o serviço hospedado.
