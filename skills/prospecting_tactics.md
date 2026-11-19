# Táticas de Prospecção Faça-Você-Mesmo

O playbook do Sellbird para encontrar leads sem ferramentas caras como Apollo, ZoomInfo ou Clearbit.

---

## Estratégia 1: Google Dorking

### Encontrar Perfis no LinkedIn
```
site:linkedin.com/in "VP Marketing" "SaaS" "San Francisco"
site:linkedin.com/in "Head of Growth" "marketing agency"
site:linkedin.com/in "{{title}}" "{{industry}}" "{{location}}"
```

### Encontrar Páginas de Equipe das Empresas
```
site:{{domain}} "team" OR "about" OR "leadership"
"{{company name}}" "team" "{{title}}"
```

### Encontrar Empresas de um Setor
```
"{{industry}}" "Series A" OR "Series B" site:crunchbase.com
"{{industry}}" company "{{location}}" "employees" site:linkedin.com/company
```

### Encontrar Padrões de E-mail
```
"@{{domain}}" email
site:{{domain}} "contact" OR "email" OR "@"
"{{first_name}} {{last_name}}" "{{company}}" email
```

---

## Estratégia 2: Busca no LinkedIn

### Operadores de Busca de Pessoas
- **Cargo**: Busque "VP Marketing" para encontrar correspondências exatas de cargo
- **Empresa**: Filtre pela empresa atual
- **Localização**: Filtre por região geográfica
- **Setor**: Filtre pelas categorias de setor do LinkedIn
- **Conexões**: conexões de 2º grau têm taxas de aceite mais altas

### Sales Navigator (se disponível)
- Busca booleana: "VP Marketing" AND "SaaS" NOT "consultant"
- Buscas salvas com alertas para novas correspondências
- Listas de leads para abordagem organizada

### Sem Sales Navigator
- Use a busca básica do LinkedIn com combinações de palavras-chave
- Navegue por "Pessoas Também Vistas" em perfis relevantes
- Confira as páginas das empresas → aba "Pessoas" para funcionários
- Pesquise dentro de Grupos relevantes do LinkedIn

---

## Estratégia 3: Raspagem do Site da Empresa

### Páginas de Equipe/Sobre
A maioria das empresas lista a liderança em páginas /team, /about, /about-us, /our-team, /people, /leadership.

**Extraia:**
- Nome + cargo dos cards de equipe
- Às vezes e-mail ou links de LinkedIn listados diretamente
- Indicador do porte da empresa pelo número de membros da equipe

### Vagas de Emprego
- Empresas contratando para cargos que seu produto apoia = prospects de alta intenção
- Confira as páginas /careers, /jobs
- Confira também os quadros de vagas: Indeed, LinkedIn Jobs, Wellfound (para startups)

### Descoberta de Stack de Tecnologia
- **BuiltWith/Wappalyzer**: Identifique as ferramentas atuais deles
- Útil para: "I see you're using {{competitor}} — here's how we compare"
- Extensões de navegador gratuitas disponíveis

---

## Estratégia 4: Descoberta do Padrão de E-mail

### Formatos de E-mail Comuns (em ordem de prevalência)
1. `first.last@domain.com` (mais comum)
2. `first@domain.com`
3. `firstlast@domain.com`
4. `flast@domain.com` (inicial do nome + sobrenome)
5. `firstl@domain.com`
6. `f.last@domain.com`
7. `last.first@domain.com`
8. `first_last@domain.com`
9. `first-last@domain.com`

### Métodos de Verificação (Grátis)
1. **Checagem de registro MX**: Verifique se o domínio aceita e-mail (consulta DNS)
2. **SMTP RCPT TO**: Pergunte ao servidor de e-mail se o endereço existe
3. **Camada gratuita do Hunter.io**: 25 buscas/mês + 50 verificações/mês
4. **Formato de e-mail a partir de endereços conhecidos**: Se você conhece o e-mail de uma pessoa em uma empresa, o padrão vale para todo mundo

### Domínios Catch-All
Alguns domínios aceitam todos os endereços (catch-all). A verificação SMTP não funciona para eles. Confie no padrão + verificação do domínio.

---

## Estratégia 5: Eventos-Gatilho

Sinais de timing de alto valor que indicam que um prospect pode estar pronto para comprar:

1. **Nova contratação em cargo relevante** — estão montando a função que você apoia
2. **Captação recente** — têm orçamento para gastar
3. **Lançamento de produto novo** — precisam de apoio de marketing/growth
4. **Vaga aberta na área do seu produto** — estão investindo na área
5. **Concorrente usando seu produto** — ângulo de prova social
6. **Expansão da empresa** — equipes em crescimento precisam de ferramentas novas
7. **Troca de liderança** — novos líderes trazem ferramentas novas
8. **Mudança de stack de tecnologia** — estão avaliando alternativas

### Onde encontrar eventos-gatilho (grátis)
- Alertas do Google News para empresas-alvo
- LinkedIn: siga as empresas-alvo para receber atualizações
- Crunchbase (camada gratuita): anúncios de captação
- Blogs das empresas e páginas de press release
- Quadros de vagas: novas vagas em departamentos relevantes

---

## Estratégia 6: Mineração de Indicações

Quando um prospect diz "não sou a pessoa certa":
1. Pergunte quem É a pessoa certa (nome + cargo)
2. Pergunte se ele estaria aberto a fazer uma apresentação
3. Se não houver apresentação, use o nome dele como prova social: "{{name}} on your team suggested I reach out..."

Quando um negócio fecha:
1. Peça indicações para empresas semelhantes
2. Pergunte se conhecem pares em outras empresas com desafios semelhantes
3. LinkedIn: confira as conexões deles em busca de correspondências com o ICP

---

## Cotas Diárias de Prospecção

Para construção sustentável de pipeline:
- **Pesquisa**: 20-30 empresas por dia
- **Novos prospects identificados**: 10-15 por dia
- **E-mails verificados**: 10-15 por dia
- **Total de prospects adicionados ao banco**: 10-15 por dia
- **Controle de qualidade**: Pontue cada prospect antes de adicioná-lo à abordagem
