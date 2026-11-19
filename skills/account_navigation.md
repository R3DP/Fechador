# Account Navigation: Trabalhando com Múltiplos Contatos em Uma Empresa

## Empresas vs Contatos

Uma empresa é uma conta. Um contato é uma pessoa nessa empresa. Uma empresa pode ter muitos contatos. O Sellbird deve sempre criar primeiro o perfil da empresa e depois anexar os contatos a ele.

## Perfis de Empresa

Toda empresa que o Sellbird pesquisa deve ter:
- **Name**: O nome real da empresa
- **Domain**: O domínio do site dela (ex.: acme.com)
- **Website**: URL completa
- **Description**: O que a empresa faz (1-2 frases)
- **Industry**: Setor principal
- **Company size**: Faixa de funcionários
- **Location**: Cidade/região da sede
- **Source**: Como o Sellbird a encontrou (google, linkedin, website scrape)
- **Source URL**: A URL exata onde o Sellbird encontrou a informação

O Sellbird deve extrair isso do site da empresa, da página da empresa no LinkedIn ou dos resultados do Google. Não adivinhe. Se você não consegue verificar um campo, deixe em branco.

## Perfis de Contato

Todo contato deve ter no mínimo:
- **First name**: Obrigatório. Deve ser real, verificado.
- **Last name**: Obrigatório. Deve ser real, verificado.
- **Title**: Obrigatório. Deve ser o cargo atual real dele.
- **Company**: Vinculado ao perfil da empresa.

Campos opcionais (preencher só se verificável):
- **Email**: Inclua apenas se verificado por checagem MX/SMTP ou encontrado no site da empresa. Marque email_verified = true só se confirmado.
- **Phone**: Muito difícil de encontrar. Inclua apenas se listado publicamente (site da empresa, perfil no LinkedIn). Marque phone_verified = true só se confirmado. NÃO adivinhe números de telefone.
- **LinkedIn URL**: Inclua se encontrado.
- **Seniority**: c_suite, vp, director, manager, individual. Deduza do cargo.
- **Department**: Sales, marketing, engineering, operations, etc. Deduza do cargo.

### Regras de Qualidade de Dados
1. Nunca fabrique informação de contato. Se você não consegue verificar, não inclua.
2. Padrões de e-mail (first.last@domain.com) só são válidos após verificação SMTP.
3. Um contato sem e-mail verificado ainda pode ser valioso para abordagem no LinkedIn.
4. Sempre registre onde você encontrou cada informação (source + source_url).

## Quem Contatar em uma Empresa

### A Matriz de Ponto de Entrada

Nem todos os contatos são iguais. Quem você aborda primeiro depende do tipo de negócio:

| Tipo de Negócio | Primeiro Contato | Segundo Contato | Evitar Primeiro |
|-----------|--------------|----------------|-------------|
| **Compra pequena** (<$500/mês) | Usuário final / gerente | O chefe dele | C-level (sênior demais) |
| **Mid-market** ($500-5k/mês) | Diretor / VP | Gerente que usaria | Contribuidores individuais |
| **Enterprise** ($5k+/mês) | VP / C-level | Defensor (gerente que vai advogar) | Funcionários júnior |

### Multi-Threading: Trabalhando Múltiplos Contatos

Quando o Sellbird encontra múltiplos contatos em uma empresa:

1. **Comece com um.** Nunca envie e-mail para várias pessoas da mesma empresa simultaneamente. Parece spam e elas vão comparar anotações.

2. **Comece no nível certo.** Escolha a pessoa com mais probabilidade de:
   - Sentir a dor que seu produto resolve
   - Ter autoridade para avaliar soluções
   - Realmente ler e responder e-mail

3. **Suba ou desça conforme a resposta:**
   - Sem resposta do gerente? Tente o VP.
   - O VP diz "fale com meu time"? Envie e-mail ao gerente e cite o VP.
   - O gerente se interessou? Pergunte se ele gostaria de incluir o chefe.

4. **Espere entre contatos.** Se você envia e-mail para a Pessoa A na Acme, espere pelo menos 5 dias úteis antes de enviar e-mail para a Pessoa B na Acme. Trate a empresa como uma conta, não como contatos individuais.

5. **Compartilhe contexto entre contatos.** Se a Pessoa A respondeu, o Sellbird deve saber disso ao escrever para a Pessoa B. "Your colleague Sarah mentioned she's evaluating options" é poderoso.

### Detecção de Senioridade

Deduza a senioridade do cargo:

- **C-Suite**: CEO, CTO, CFO, CMO, COO, CRO, "Chief __"
- **VP**: VP, Vice President, SVP, EVP, "Head of __"
- **Director**: Director, Senior Director, "Director of __"
- **Manager**: Manager, Senior Manager, Team Lead, "Manager of __"
- **Individual**: Analyst, Specialist, Coordinator, Associate, Engineer

### Quando Parar

Pare de contatar uma empresa se:
- 3 contatos diferentes receberam e-mail sem resposta
- Qualquer contato disser explicitamente "não tenho interesse" ou "pare de enviar e-mails"
- A empresa não corresponder ao ICP após mais pesquisa

## Validação por Amostra

Antes de adicionar prospects ao pipeline ativo, o Sellbird deve criar um lote de amostra de 5-10 perfis de empresa + contato e apresentá-los ao usuário para revisão. Isso garante:

1. Que o direcionamento do ICP está correto (setores certos, portes de empresa certos)
2. Que os cargos dos contatos correspondem ao que o usuário quer
3. Que a qualidade dos dados atende às expectativas
4. Que as fontes da pesquisa são legítimas

### Fluxo da Amostra
1. O Sellbird pesquisa 5-10 empresas e seus contatos
2. Apresenta como amostra: "Here are 8 companies I found. Each has 1-2 contacts. Take a look and let me know if these are the right kind of targets."
3. O usuário revisa e dá feedback ("muito pequena", "setor errado", "perfeito", "já trabalhamos com eles")
4. O Sellbird ajusta o direcionamento com base no feedback
5. Após aprovação, o Sellbird segue com a prospecção completa

Esta etapa de amostra só acontece uma vez no início (ou quando o ICP muda). Depois que o usuário aprova a amostra, o Sellbird prospecta de forma autônoma.
