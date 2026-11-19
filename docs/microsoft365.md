# Enviar de uma caixa Microsoft 365

O Sellbird pode enviar e ler e-mail por uma caixa Microsoft 365 / Outlook
(Exchange Online) usando o Microsoft Graph. Use quando o e-mail do seu domínio de envio
fica no Microsoft 365.

## Por que não SMTP + IMAP?

O Exchange Online não aceita mais senha para IMAP, e o SMTP AUTH vem desligado
por padrão na maioria dos tenants. O provedor `smtp` às vezes ainda consegue enviar, mas
não consegue ler a caixa de entrada. O Sellbird precisa ler respostas para interromper sequências, honrar
descadastros e captar bounces. Se ele consegue enviar mas não ler, continua mandando e-mail
para pessoas que já responderam.

O provedor `microsoft` faz login com OAuth (authorization code + PKCE)
em vez disso. O Sellbird nunca armazena senha ou client secret.

## Configuração

### 1. Registrar um app no Entra ID

Em [entra.microsoft.com](https://entra.microsoft.com), vá em
**Applications → App registrations → New registration**:

| Campo | Valor |
|---|---|
| Name | `Sellbird` |
| Supported account types | *Accounts in this organizational directory only* |
| Redirect URI, platform | **Public client/native (mobile & desktop)** |
| Redirect URI, value | `http://localhost:8766` |

No **Overview** do app, copie o **Application (client) ID** e o
**Directory (tenant) ID**.

Não crie um client secret. O Sellbird é um cliente público.

### 2. Configurar o Sellbird

`.env`:

```
M365_CLIENT_ID=<Application (client) ID>
M365_TENANT_ID=<Directory (tenant) ID>
```

`sellbird.yaml` (ou `sellbird.local.yaml`):

```yaml
persona:
  email: "you@yourdomain.com"   # must be the mailbox you sign in with
channels:
  email:
    provider: "microsoft"
```

### 3. Entrar uma vez

```bash
sellbird microsoft auth   # opens the browser; sign in as persona.email
sellbird microsoft test   # → ✓ Connected as you@yourdomain.com
```

O Sellbird pede quatro permissões **delegadas**:

| Permissão | Por que é necessária |
|---|---|
| `Mail.ReadWrite` | ler respostas e criar rascunhos (encadeamento de respostas) |
| `Mail.Send` | enviá-las |
| `User.Read` | conferir a qual caixa o token pertence |
| `offline_access` | continuar funcionando sem entrar de novo |

O refresh token é armazenado em `data/m365_token.json` (no gitignore). No macOS
e Linux o arquivo tem modo 600 (somente o dono). O Windows não tem esses bits de modo:
o arquivo é protegido apenas pelas permissões de acesso (ACLs) da pasta
em que o Sellbird vive, então mantenha o Sellbird numa pasta que só você possa ler.
A Microsoft o rotaciona a cada uso, e o Sellbird salva o novo a cada vez.

### Se você vir "Need admin approval"

Seu tenant não deixa os usuários consentirem em apps por conta própria. Um admin precisa
aprovar o app uma vez:

1. No Entra, abra **App registrations → Sellbird → API permissions**. Adicione as
   quatro permissões delegadas do Microsoft Graph acima e clique em
   **Grant admin consent**.
2. Rode `sellbird microsoft auth` de novo e entre como a **caixa de envio**,
   não como o admin. O Sellbird sempre age como quem entra.

Para garantir que ninguém mais no tenant possa usar o app, vá em
**Enterprise applications → Sellbird**:

1. **Users and groups**: atribua apenas a caixa de envio.
2. **Properties**: defina **Assignment required?** como **Yes**. Faça isso depois do
   passo 1, ou a caixa de envio também fica bloqueada.

## Como se comporta

- **Envio.** O Sellbird cria um rascunho e então o envia, para que o
  `Message-ID` RFC do e-mail seja conhecido. Bounces e respostas são casados por ele. Os corpos
  são texto puro, a menos que `channels.email.signature.logo` esteja definido: então o
  corpo é HTML e o logo é adicionado ao rascunho como anexo inline
  antes do envio. A assinatura do próprio Outlook não é adicionada ao e-mail enviado
  pelo Graph, então esta é a forma de colocar um logo sob o e-mail do Sellbird.
- **Respostas são encadeadas.** O Sellbird responde com `createReply` sobre a
  própria mensagem do prospect, então `In-Reply-To` e `References` ficam corretos. Se
  essa mensagem foi apagada, a resposta sai como um e-mail novo.
- **Sua caixa de entrada fica intocada.** A cada ciclo, o Sellbird lê os últimos 7 dias da
  caixa de entrada, do mais novo para o mais antigo, tudo (página por página), e pula o seu próprio e-mail. Ele nunca marca nada como
  lido, move ou apaga. Ele mantém seu próprio registro do que
  já tratou.
- **Só age como a caixa certa.** Se a caixa conectada não for
  `persona.email`, toda leitura e envio é recusado com uma mensagem dizendo isso.
  Isso pega o erro comum de entrar como o admin que aprovou
  o app.
- **Falhas retêm o envio.** Se a caixa de entrada não puder ser lida (login expirado,
  queda do Graph, throttling), o ciclo não envia nada. Uma resposta que ninguém leu
  não pôde ter parado seus follow-ups. O throttling do Graph (429/503 com um curto
  `Retry-After`) é tentado uma vez de novo. Uma leitura que falha no meio
  conta como leitura falha: o Sellbird nunca age sobre parte da caixa de entrada.
- **Rascunhos não enviados são limpos.** Se um envio falha, seu rascunho é apagado
  para não ficar na sua pasta Rascunhos.
- **O nome do remetente é o da caixa.** O e-mail sai sob o nome de exibição
  da caixa no Microsoft 365, não o `persona.name`.

## Solução de problemas

| Sintoma | Correção |
|---|---|
| `Timed out waiting for the browser round-trip` | O navegador nunca voltou para `localhost:8766`. Verifique se nada mais usa a porta, e que o redirect URI é `http://localhost:8766` em *Mobile and desktop applications* (não em *Web*). |
| `AADSTS50011` (redirect URI mismatch) | Igual ao acima: a URI e sua plataforma precisam coincidir exatamente. |
| `Need admin approval` | Veja [Se você vir "Need admin approval"](#se-você-vir-need-admin-approval). |
| `signed in as X, but persona.email is Y` | Rode `sellbird microsoft auth` de novo e escolha a conta certa. Use "Use another account" se o navegador já estiver logado como outra pessoa. |
| `token refresh rejected` | O login expirou (90 dias sem uso) ou foi revogado. Rode `sellbird microsoft auth` de novo. |

Para revogar o acesso do Sellbird, vá em
[myaccount.microsoft.com](https://myaccount.microsoft.com) → **Apps**, ou
apague o registro do app. Depois apague `data/m365_token.json`.

## Notas de entregabilidade

- **Ative o DKIM** para seu domínio no Microsoft Defender (Email
  authentication → DKIM). Sem isso, o e-mail do Exchange Online não é
  assinado com o seu domínio.
- **Cuidado com o tenant.** O Exchange Online vigia o spam de saída do tenant
  inteiro. Se você o compartilha com uma organização, a reputação de envio dela
  depende da sua: mantenha `max_daily_sends` baixo e `require_approval: true`.

## Para desenvolvedores

| Arquivo | O que é |
|---|---|
| `sellbird/integrations/microsoft.py` | `MicrosoftProvider` (um `MailProvider`) e `run_auth_flow` |
| `sellbird/integrations/mail_provider.py` | Registra `microsoft` em `NATIVE_PROVIDERS` e `get_mail_provider` |
| `sellbird/cli.py` | `sellbird microsoft auth\|test` |
| `tests/test_microsoft.py` | Graph e login simulados com `httpx.MockTransport`; sem rede |

`get_replies` **levanta** `GraphError` quando a caixa de entrada não pode ser lida, em vez
de retornar `[]`. O handler transforma isso numa leitura falha, e o
heartbeat retém o envio. Ele retorna a janela inteira de 7 dias ou nada:

- **Cada página.** `limit` é apenas o tamanho da página (`$top`). O Sellbird segue
  `@odata.nextLink` até o Graph parar de enviá-lo, usando o link exatamente
  como dado, sem readicionar os parâmetros da primeira requisição ou tocar em
  `$skip`, como a Microsoft pede. Mensagens repetidas entre páginas (e-mail novo
  desloca `$skip` no meio da leitura) são retornadas uma vez.
- **Links são conferidos antes de o token ser anexado.** Um `nextLink` precisa ser
  `https://graph.microsoft.com` (porta padrão), no caminho
  `/v1.0/me/mailFolders/inbox/messages` ou sua forma de chave OData
  `/v1.0/me/mailFolders('inbox')/messages` (que o Graph ao vivo retorna), com
  uma query, e sem credenciais,
  fragmento, barra invertida ou caracteres de controle. Um link que repete uma página anterior
  é um loop. De qualquer forma a leitura falha sem enviar a requisição.
- **Limitado.** Mais de `MAX_INBOX_PAGES` (40) páginas, ou seja, 2.000 mensagens
  numa semana no tamanho de página padrão, falha a leitura em vez de truncar.
- **Dados malformados falham.** Qualquer resposta do Graph precisa ser um objeto JSON; apenas
  `202`/`204` (envio, exclusão) podem vir vazios. Uma página cujo `value` esteja ausente
  ou não seja uma lista, ou uma mensagem com formato errado (sem `id`, `from` ou
  `body` não objeto, campos que não são string, headers que não são lista) levanta erro. Uma
  mensagem sem endereço de remetente é pulada, como antes.

Limitações: uma caixa com mais de 2.000 mensagens na caixa de entrada em 7 dias retém
o envio a cada ciclo até o volume cair (aumente `MAX_INBOX_PAGES` ou o
tamanho da página). Se o Graph alguma vez retornar um `nextLink` em outro formato (digamos
`/users/{id}/...`), as leituras falham fechadas até a checagem ser ampliada. E-mail que
chega enquanto as páginas estão sendo lidas pode deslocar `$skip` e uma mensagem ser
perdida naquele ciclo; o próximo ciclo a lê, já que a janela é de 7 dias.

O servidor de callback em loopback escuta em `127.0.0.1` e em `::1`, porque
`localhost` resolve para ambos e os navegadores divergem sobre qual tentam.
